# -*- coding: utf-8 -*-

"""
* Name:         workerA_run
* Description:  Worker to simulate an interactive clustering annotation subjectivity with some differences.
* Author:       Erwan Schild
* Created:      24/05/2021
* Licence:      CeCILL (https://cecill.info/licences.fr.html)
"""

# ==============================================================================
# IMPORT PYTHON DEPENDENCIES
# ==============================================================================

import json
import pickle  # noqa: S403
import os
import random
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from cognitivefactory.interactive_clustering.constraints.abstract import (
    AbstractConstraintsManager,
)
from cognitivefactory.interactive_clustering.constraints.factory import (
    managing_factory,
)
from cognitivefactory.interactive_clustering.sampling.abstract import (
    AbstractConstraintsManager
)
from cognitivefactory.interactive_clustering.sampling.factory import (
    sampling_factory
)
from cognitivefactory.interactive_clustering.sampling.clusters_based import (
    ClustersBasedConstraintsSampling
)
from cognitivefactory.interactive_clustering.clustering.abstract import (
    AbstractConstrainedClustering,
)
from cognitivefactory.interactive_clustering.clustering.factory import (
    clustering_factory,
)
from scipy.sparse import csr_matrix
from sklearn import metrics


# ==============================================================================
# WORKER - EXPERIMENT RUN
# ==============================================================================
def experiment_run(
    parameters: Dict[str, Any],
) -> int:
    """
    A worker to simulate interactive clustering experiment with some annotation errors.
    An experiment is aimed at iteratively and automatically annotated an NLP dataset with the interactive clustering methodology.
    At each iteration, the process samples data to annotate, annotates constraints on these data according to the groudtruth, then applies a constrained clustering.
    Each constraints is annotate according to the groundtruth, but some constraints are chosen to be miss-annotated.
    Usage note:
        - Parameters have to contain the path experiment to run. A dictionary is needed to get parameters in `multiprocessing.Pool.imap_unordered` call.
        - The path to the environment has to be formatted by the notebook `1_Initialize_annotation_errors_experiments.ipynb`.
        - The notebook `2_Simulate_errors_and_run_clustering.ipynb` launch this script for all defined experiment environments with the librairy `multiprocessing`.

    Args:
        parameters (Dict[str, Any]): A dictionary that contains several parameters. Several keys are expected in this dictionary: the experiment environment path (`"ENV_PATH"`), the v-measure score to reach (`"MIN_VMEASURE"`), the maximum iteration of interactive clustering (`"MAX_NB_CONSTRAINTS"`).

    Returns:
        int: Return `0` when finish.
    """

    # Parameters.
    ENV_PATH: str = str(parameters["ENV_PATH"])
    MIN_VMEASURE: Optional[float] = (
        0.95
        if (
            "MIN_VMEASURE" not in parameters.keys()
            or parameters["MIN_VMEASURE"] is None
        )
        else float(parameters["MIN_VMEASURE"])
    )
    MAX_RATE_CONSTRAINTS: Optional[float] = (
        8.0
        if (
            "MAX_RATE_CONSTRAINTS" not in parameters.keys()
            or parameters["MAX_RATE_CONSTRAINTS"] is None
        )
        else float(parameters["MAX_RATE_CONSTRAINTS"])
    )

    # If experiment was already run: skip.
    if ".done" in os.listdir(ENV_PATH):
        # End of script.
        return 0

    ### ### ### ### ###
    ### Load needed configurations and data.
    ### ### ### ### ###
    
    # Load configuration for dataset.
    with open(
        ENV_PATH + "../../../config.json", "r"
    ) as file_config_dataset:
        CONFIG_DATASET = json.load(file_config_dataset)
    
    # Load configuration for algorithm.
    with open(
        ENV_PATH + "../../config.json", "r"
    ) as file_config_algorithm:
        CONFIG_ALGORITHM = json.load(file_config_algorithm)

    # Load configuration for errors.
    with open(
        ENV_PATH + "../config.json", "r"
    ) as file_config_errors:
        CONFIG_ERRORS = json.load(file_config_errors)
    
    # Load configuration for selection.
    with open(
        ENV_PATH + "config.json", "r"
    ) as file_config_selection:
        CONFIG_SELECTION = json.load(file_config_selection)

    ### ### ### ### ###
    ### Load needed data.
    ### ### ### ### ###
    
    # Load dict of true intents.
    with open(
        ENV_PATH + "../../../dict_of_true_intents.json", "r"
    ) as file_true_intents:
        dict_of_true_intents: Dict[str, str] = json.load(file_true_intents)

    # Load dict of vectors.
    with open(ENV_PATH + "../../dict_of_vectors.pkl", "rb") as file_vectors:
        dict_of_vectors: Dict[str, csr_matrix] = pickle.load(file_vectors)  # noqa: S301
    
    # Load previous sampling.
    with open(
        ENV_PATH + "previous_sampling.json", "r"
    ) as file_previous_sampling:
        list_of_previous_sampling: List[Tuple[str, str]] = json.load(file_previous_sampling)
            
    # Get list of data IDs.
    list_of_data_IDs: List[str] = sorted(dict_of_true_intents.keys())

    ### ### ### ### ###
    ### Load work already done.
    ### ### ### ### ###

    # Load list of constraints sampled.
    with open(
        ENV_PATH + "dict_of_samplings.json", "r"
    ) as file_sampling_r:
        dict_of_samplings: Dict[str, List[Tuple[str, str]]] = json.load(file_sampling_r)

    # Load list of errors to simulate.
    with open(
        ENV_PATH + "dict_of_errors.json", "r"
    ) as file_errors_r:
        dict_of_errors: Dict[str, List[Tuple[str, str]]] = json.load(file_errors_r)

    # Load list of effective constraints in manager.
    with open(
        ENV_PATH + "dict_of_constraints_effective.json", "r"
    ) as file_constraints_r:
        dict_of_constraints_effective: Dict[str, List[Tuple[str, str]]] = json.load(file_constraints_r)
    
    # Load dict of clustering results.
    with open(
        ENV_PATH + "dict_of_clustering_results.json", "r"
    ) as file_clustering_results_r:
        dict_of_clustering_results: Dict[str, Dict[str, int]] = json.load(file_clustering_results_r)
    
    # Load dict of clustering performances.
    with open(
        ENV_PATH + "dict_of_clustering_performances.json", "r"
    ) as file_clustering_performance_r:
        dict_of_clustering_performances: Dict[str, Dict[str, float]] = json.load(file_clustering_performance_r)

    ### ### ### ### ###
    ### While (condition).
    ### ### ### ### ###
    
    # Get number of constraints handled.
    PREVIOUS_NB_CONSTRAINTS: int = (
        max(
            [
                int(previous_nb_constraints_id)
                for previous_nb_constraints_id in dict_of_clustering_performances.keys()
            ],
            default=0,
        )
    )
    PREVIOUS_NB_CONSTRAINTS_ID: str = str(PREVIOUS_NB_CONSTRAINTS).zfill(6)
        
    #
    CURRENT_NB_CONSTRAINTS = PREVIOUS_NB_CONSTRAINTS
    CURRENT_NB_CONSTRAINTS_ID = PREVIOUS_NB_CONSTRAINTS_ID
        

    # Compute constraints manager.
    constraints_manager: AbstractConstraintsManager
    constraints_manager, _ = _get_new_constraints_manager(
        list_of_data_IDs=list_of_data_IDs,
        dict_of_true_intents=dict_of_true_intents,
        list_of_sampling=dict_of_samplings[PREVIOUS_NB_CONSTRAINTS_ID],
        list_of_errors=dict_of_errors[PREVIOUS_NB_CONSTRAINTS_ID],
        with_fix=CONFIG_ERRORS["with_fix"],
    )
    
    # Compute max constraints threshold.
    MAX_NB_CONSTRAINTS: Optional[float] = (
        None 
        if (MAX_RATE_CONSTRAINTS is None)
        else (CONFIG_DATASET["size"] * MAX_RATE_CONSTRAINTS)
    )
        
    while (
        # Case 1: not completude.
        not constraints_manager.check_completude_of_constraints()
        # Case 2: less than MAX_NB_CONSTRAINTS.
        and (
            MAX_NB_CONSTRAINTS is None
            or (PREVIOUS_NB_CONSTRAINTS + CONFIG_SELECTION["constraints_step"]) <= MAX_NB_CONSTRAINTS
        )
        # Case 3: less than MIN_VMEASURE.
        and (
            MIN_VMEASURE is None
            or dict_of_clustering_performances[PREVIOUS_NB_CONSTRAINTS_ID]["v_measure"] < MIN_VMEASURE
        )
    ):
        
        ### ### ### ### ###
        ### Apply constraints sampling.
        ### ### ### ### ###
            
        # Initialze with already used constraints.
        list_of_sampling: List[Tuple[str, str]] = []
        
        # 1. Use previous sampling.
        if len(list_of_sampling) < CONFIG_SELECTION["constraints_step"]:
            list_of_sampling += list_of_previous_sampling[PREVIOUS_NB_CONSTRAINTS:(PREVIOUS_NB_CONSTRAINTS+CONFIG_SELECTION["constraints_step"])]
            
        # 2. If needed: perform a new sampling.
        if len(list_of_sampling) < CONFIG_SELECTION["constraints_step"]:
            list_of_sampling += sampling_factory(
                algorithm=CONFIG_ALGORITHM["previous_sampling"]["algorithm"],
                random_seed=CONFIG_SELECTION["random_seed"],
            ).sample(
                constraints_manager=constraints_manager,
                nb_to_select=(CONFIG_SELECTION["constraints_step"]-len(list_of_sampling)),
                clustering_result=dict_of_clustering_results[PREVIOUS_NB_CONSTRAINTS_ID],
                vectors=dict_of_vectors,
            )
        
        # 3. If still needed: perform a new sampling.
        if len(list_of_sampling) < CONFIG_SELECTION["constraints_step"]:
            list_of_sampling += ClustersBasedConstraintsSampling(
                clusters_restriction=CONFIG_SELECTION["next_sampling"]["init**kargs"]["clusters_restriction"],
                distance_restriction=CONFIG_SELECTION["next_sampling"]["init**kargs"]["distance_restriction"],
                without_added_constraints=CONFIG_SELECTION["next_sampling"]["init**kargs"]["without_added_constraints"],
                without_inferred_constraints=CONFIG_SELECTION["next_sampling"]["init**kargs"]["without_inferred_constraints"],
                random_seed=CONFIG_SELECTION["random_seed"],
            ).sample(
                constraints_manager=constraints_manager,
                nb_to_select=(CONFIG_SELECTION["constraints_step"]-len(list_of_sampling)),
                clustering_result=dict_of_clustering_results[PREVIOUS_NB_CONSTRAINTS_ID],
                vectors=dict_of_vectors,
            )
        
        # Update number of constraints handled.
        CURRENT_NB_CONSTRAINTS = PREVIOUS_NB_CONSTRAINTS + len(list_of_sampling)
        CURRENT_NB_CONSTRAINTS_ID = str(CURRENT_NB_CONSTRAINTS).zfill(6)
        
        # Update storage of list of constraints sampled.
        dict_of_samplings[CURRENT_NB_CONSTRAINTS_ID] = dict_of_samplings[PREVIOUS_NB_CONSTRAINTS_ID] + list_of_sampling
        with open(ENV_PATH + "dict_of_samplings.json", "w") as file_samplings_w:
            json.dump(dict_of_samplings, file_samplings_w)
    
        ### ### ### ### ###
        ### Choose some annotation errors.
        ### ### ### ### ###
        
        # Randomly select errors.
        random.seed(CONFIG_ERRORS["random_seed"])
        list_of_errors: List[Tuple[str, str]] = random.sample(
            list_of_sampling,
            k=int(len(list_of_sampling)*CONFIG_ERRORS["error_rate"])
        )

        # Update storage of list of errors to simulate.
        dict_of_errors[CURRENT_NB_CONSTRAINTS_ID] = dict_of_errors[PREVIOUS_NB_CONSTRAINTS_ID] + list_of_errors
        with open(ENV_PATH + "dict_of_errors.json", "w") as file_errors_w:
            json.dump(dict_of_errors, file_errors_w)
    
        ### ### ### ### ###
        ### Define the new constraints manager.
        ### ### ### ### ###
        
        # Get new constraints manager.
        list_of_effective_constraints: List[Tuple[str, str, str, bool, bool]]
        constraints_manager, list_of_effective_constraints = _get_new_constraints_manager(
            list_of_data_IDs=list_of_data_IDs,
            dict_of_true_intents=dict_of_true_intents,
            list_of_sampling=dict_of_samplings[CURRENT_NB_CONSTRAINTS_ID],
            list_of_errors=dict_of_errors[CURRENT_NB_CONSTRAINTS_ID],
            with_fix=CONFIG_ERRORS["with_fix"],
        )
        
        # Update storage of list of effective constraints in manager.
        dict_of_constraints_effective[CURRENT_NB_CONSTRAINTS_ID] = list_of_effective_constraints
        with open(ENV_PATH + "dict_of_constraints_effective.json", "w") as file_constraints_w:
            json.dump(dict_of_constraints_effective, file_constraints_w)

        ### ### ### ### ###
        ### Apply constrained clustering.
        ### ### ### ### ###
        
        # Initialize clustering model.
        clustering_model: AbstractConstrainedClustering = clustering_factory(
            algorithm=CONFIG_ALGORITHM["clustering"]["algorithm"],
            random_seed=CONFIG_ALGORITHM["clustering"]["random_seed"],
            **CONFIG_ALGORITHM["clustering"]["init**kargs"],
        )

        # Run clustering.
        clustering_result: Dict[str, int] = clustering_model.cluster(
            vectors={
                vector_id: csr_matrix(vector_value)
                for vector_id, vector_value in dict_of_vectors.items()
            },
            nb_clusters=CONFIG_ALGORITHM["clustering"]["nb_clusters"],
            constraints_manager=constraints_manager,
        )
        
        # Update storage of dict of clustering results.
        dict_of_clustering_results[CURRENT_NB_CONSTRAINTS_ID] = clustering_result
        with open(ENV_PATH + "dict_of_clustering_results.json", "w") as file_clustering_w:
            json.dump(dict_of_clustering_results, file_clustering_w)

        ### ### ### ### ###
        ### Evaluate clustering.
        ### ### ### ### ###

        # Format true intents from dict to list.
        list_of_true_intents: List[str] = [
            dict_of_true_intents[data_ID]
            for data_ID in list_of_data_IDs
        ]

        # Format predicted intents from dict to list.
        list_of_predicted_intents: List[int] = [
            clustering_result[data_ID]
            for data_ID in list_of_data_IDs
        ]

        # Compute performances.
        clustering_performances: Dict[str, float] = {}
        clustering_performances["homogeneity"] = metrics.homogeneity_score(list_of_true_intents, list_of_predicted_intents)
        clustering_performances["completeness"] = metrics.completeness_score(list_of_true_intents, list_of_predicted_intents)
        clustering_performances["v_measure"] = metrics.v_measure_score(list_of_true_intents, list_of_predicted_intents)
        clustering_performances["adjusted_rand_index"] = metrics.adjusted_rand_score(list_of_true_intents, list_of_predicted_intents)
        clustering_performances["adjusted_mutual_information"] = metrics.adjusted_mutual_info_score(list_of_true_intents, list_of_predicted_intents)

        # Update storage of dict of clustering performances.
        dict_of_clustering_performances[CURRENT_NB_CONSTRAINTS_ID] = clustering_performances
        with open(ENV_PATH + "dict_of_clustering_performances.json", "w") as file_performances_w:
            json.dump(dict_of_clustering_performances, file_performances_w)
        
        # Update number of constraints handled for next iteration.
        PREVIOUS_NB_CONSTRAINTS = CURRENT_NB_CONSTRAINTS
        PREVIOUS_NB_CONSTRAINTS_ID = CURRENT_NB_CONSTRAINTS_ID


    ### ### ### ### ###
    ### Done.
    ### ### ### ### ###
    
    # Write a ".done" file.
    with open(
        ENV_PATH + ".done", "w"
    ) as file_done:
        json.dump(
            {
                # Case 1: not completude.
                "COMPLETUDE": constraints_manager.check_completude_of_constraints(),
                # Case 2: less than MAX_NB_CONSTRAINTS.
                "MAX_NB_CONSTRAINTS": MAX_NB_CONSTRAINTS,
                "PREVIOUS_NB_CONSTRAINTS": PREVIOUS_NB_CONSTRAINTS,
                # Case 3: less than MIN_VMEASURE.
                "MIN_VMEASURE": MIN_VMEASURE,
                "V_MEASURE": dict_of_clustering_performances[CURRENT_NB_CONSTRAINTS_ID]["v_measure"]
            },
            file_done
        )
    
    # End of script.
    return 0


# ==============================================================================
# COMPUTE NEW CONSTRAINTS MANAGER
# ==============================================================================

def _get_new_constraints_manager(
    list_of_data_IDs: List[str],
    dict_of_true_intents: Dict[str, str],
    list_of_sampling: List[Tuple[str, str]],
    list_of_errors: List[Tuple[str, str]],
    with_fix: bool = True,
) -> Tuple[
    AbstractConstraintsManager,
    List[Tuple[str, str, str, bool, bool]]
]:
    """
    A function to recompute a constraints manager and return it with the list of effective annotated constraints.

    Args:
        list_of_data_IDs (List[str]) : The list of managed data IDs.
        dict_of_true_intents (Dict[str, str]): The dictionnary of true intents.
        list_of_sampling (List[Tuple[str, str]]): The list of sampling data to add in the constraints manager.
        list_of_errors (List[Tuple[str, str]]): The list of data to add in the constraints manager with an annotation error.
        with_fix (bool): The option to fix conclicts. Defaults to `True`.

    Returns:
        Tuple[AbstractConstraintsManager, List[Tuple[str, str, str, bool, bool]]]: The constraints manager and the list of effective annotated constraints.
    """
    
    # Initialize constraints manager.
    constraints_manager: AbstractConstraintsManager = managing_factory(
        list_of_data_IDs=list_of_data_IDs,
        manager="binary",
    )

    # Dictionary of constraints.
    list_of_effective_constraints: List[Tuple[str, str, str, bool, bool]] = []
        
    # If with_fix:
    if with_fix:
        list_of_sampling = sorted(
            list_of_sampling,
            key=lambda x: x in list_of_errors,
        )
        
    # For all constraint to annotate...
    for data_to_annotate in list_of_sampling:

        # Estimate annotator answer (automation based on true intents comparison).
        annotation_type: str = (
            "MUST_LINK"
            if (
                data_to_annotate not in list_of_errors and
                dict_of_true_intents[data_to_annotate[0]] == dict_of_true_intents[data_to_annotate[1]]
            ) or (
                data_to_annotate in list_of_errors and
                dict_of_true_intents[data_to_annotate[0]] != dict_of_true_intents[data_to_annotate[1]]
            )
            else "CANNOT_LINK"
        )

        # Add the constraints (no possible error).
        try:
            constraints_manager.add_constraint(
                data_ID1=data_to_annotate[0],
                data_ID2=data_to_annotate[1],
                constraint_type=annotation_type,
            )
            list_of_effective_constraints.append(
                [
                    data_to_annotate[0],  # data ID
                    data_to_annotate[1],  # data ID
                    annotation_type,  # the effective constraint_type annotated
                    data_to_annotate in list_of_errors,  # have you annotate an error?
                    False,  # has a conflict occured?
                ]
            )

        # Conflict: Keep the error.
        except ValueError:

            # Get annotator correction (automation based on true intents comparison).
            fix_annotation_type: str = (
                "CANNOT_LINK"
                if (annotation_type == "MUST_LINK")
                else "MUST_LINK"
            )

            # Add the constraints (no possible error).
            constraints_manager.add_constraint(
                data_ID1=data_to_annotate[0],
                data_ID2=data_to_annotate[1],
                constraint_type=fix_annotation_type,
            )
            list_of_effective_constraints.append(
                [
                    data_to_annotate[0],  # data ID
                    data_to_annotate[1],  # data ID
                    fix_annotation_type,  # the effective constraint_type annotated
                    not(data_to_annotate in list_of_errors),  # have you annotate an error? (conflict fix)
                    True,  # has a conflict occured?
                ]
            )

    # Return.
    return (
        constraints_manager,
        list_of_effective_constraints
    )