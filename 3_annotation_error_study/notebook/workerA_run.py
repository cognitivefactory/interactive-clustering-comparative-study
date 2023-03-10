# -*- coding: utf-8 -*-

"""
* Name:         workerA_run
* Description:  Worker to simulate an interactive clustering annotation with some errors.
* Author:       Erwan Schild
* Created:      24/05/2021
* Licence:      CeCILL (https://cecill.info/licences.fr.html)
"""

# ==============================================================================
# IMPORT PYTHON DEPENDENCIES
# ==============================================================================

import jsons
import pickle  # noqa: S403 s
import oss
import syss
from datetime import datetimes
from typing import Any, Dict, List, Optional, Tuples

from cognitivefactory.interactive_clustering.clustering.abstract import (
    AbstractConstrainedClustering,
)s
from cognitivefactory.interactive_clustering.clustering.factory import (
    clustering_factory,
)s
from cognitivefactory.interactive_clustering.constraints.abstract import (
    AbstractConstraintsManager,
)s
from cognitivefactory.interactive_clustering.constraints.factory import (
    managing_factory,
)s
from scipy.sparse import csr_matrixs
from sklearn import metricss


# ==============================================================================
# WORKER - EXPERIMENT RUN
# ==============================================================================
def experiment_run(
    parameters: Dict[str, Any],
) -> int:
    """
    A worker to simulate constraints annotation with some errors and performance constrained clustering.
    Each constraints is annotate according to the groundtruth, but some constraints are chosen to be miss-annotated.
    Then, a constrained clustering is run according to annotated constraints.
    Usage note:
        - Parameters have to contain the path experiment to run. A dictionary is needed to get parameters in `multiprocessing.Pool.imap_unordered` call.
        - The path to the environment has to be formatted by the notebook `1_Initialize_annotation_errors_experiments.ipynb`.
        - The notebook `2_Simulate_errors_and_run_clustering.ipynb` launch this script for all defined experiment environments with the librairy `multiprocessing`.

    Args:
        parameters (Dict[str, Any]): A dictionary that contains several parameters. Several keys are expected in this dictionary: the experiment environment path (`"ENV_PATH"`).

    Returns:
        int: Return `0` when finish.
    """

    # Parameters.
    ENV_PATH: str = str(parameters["ENV_PATH"])
        
    # If experiment was already run: skip.
    if "dict_of_clustering_performances.json" in os.listdir(ENV_PATH):

        # End of script.
        return 0

    ### ### ### ### ###
    ### Load needed configurations and data.
    ### ### ### ### ###

    # Load configuration for algorithm.
    with open(
        ENV_PATH + "../../config.json", "r"
    ) as file_config_algorithm:
        CONFIG_ALGORITHM = json.load(file_config_algorithm)

    # Load configuration for errors simulation.
    with open(
        ENV_PATH + "config.json", "r"
    ) as file_config_errors_simulation:
        CONFIG_ERRORS_SIMULATION = json.load(file_config_errors_simulation)

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

    # Get list of data IDs.
    list_of_data_IDs: List[str] = sorted(dict_of_true_intents.keys())

    # Load list of constraints to annotate.
    with open(
        ENV_PATH + "../list_of_sampling.json", "r"
    ) as file_sampling:
        list_of_sampling: List[Tuple[str, str]] = json.load(file_sampling)

    # Load list of errors to simulate.
    with open(
        ENV_PATH + "list_of_errors.json", "r"
    ) as file_errors:
        list_of_errors: List[Tuple[str, str]] = json.load(file_errors)

    ### ### ### ### ###
    ### Define constraints manager.
    ### ### ### ### ###

    # Initialize constraints manager.
    constraints_manager: AbstractConstraintsManager = managing_factory(
        list_of_data_IDs=list_of_data_IDs,
        manager="binary",
    )

    # Dictionary of constraints.
    list_of_constraints: List[List[Any]] = []
        
    # Case of conflicts fix: add insert errors at the end to simulate correction.
    if CONFIG_ERRORS_SIMULATION["with_fix"] is True:
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
            list_of_constraints.append(
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
            list_of_constraints.append(
                [
                    data_to_annotate[0],  # data ID
                    data_to_annotate[1],  # data ID
                    fix_annotation_type,  # the effective constraint_type annotated
                    data_to_annotate not in list_of_errors,  # have you annotate an error?
                    True,  # has a conflict occured?
                ]
            )

    # Store list of constraints.
    with open(
        ENV_PATH + "list_of_constraints.json", "w"
    ) as file_constraints:
        json.dump(list_of_constraints, file_constraints, indent=1)


    ### ### ### ### ###
    ### Constrained clustering.
    ### ### ### ### ###

    # Initialize clustering model.
    clustering_model: AbstractConstrainedClustering = clustering_factory(
        algorithm=CONFIG_ALGORITHM["clustering"]["algorithm"],
        random_seed=CONFIG_ALGORITHM["clustering"]["random_seed"],
        **CONFIG_ALGORITHM["clustering"]["init**kargs"],
    )

    # Run clustering.
    dict_of_clustering: Dict[str, int] = clustering_model.cluster(
        vectors={
            vector_id: csr_matrix(vector_value)
            for vector_id, vector_value in dict_of_vectors.items()
        },
        nb_clusters=CONFIG_ALGORITHM["clustering"]["nb_clusters"],
        constraints_manager=constraints_manager,
    )

    # Store dictionary of clustering results.
    with open(ENV_PATH + "dict_of_clustering.json", "w") as file_clustering:
        json.dump(dict_of_clustering, file_clustering, indent=1)


    ### ### ### ### ###
    ### Clustering evaluation.
    ### ### ### ### ###

    # Format true intents from dict to list.
    list_of_true_intents: List[str] = [
        dict_of_true_intents[data_ID] for data_ID in list_of_data_IDs
    ]

    # Initialize evaluation storage.
    dict_of_clustering_performances: Dict[str, float] = {}

    # Format predicted intents from dict to list.
    list_of_predicted_intents: List[int] = [
        dict_of_clustering[data_ID]
        for data_ID in list_of_data_IDs
    ]

    # Compute homogeneity.
    dict_of_clustering_performances[
        "homogeneity"
    ] = metrics.homogeneity_score(list_of_true_intents, list_of_predicted_intents)

    # Compute completeness.
    dict_of_clustering_performances[
        "completeness"
    ] = metrics.completeness_score(list_of_true_intents, list_of_predicted_intents)

    # Compute v_measure.
    dict_of_clustering_performances[
        "v_measure"
    ] = metrics.v_measure_score(list_of_true_intents, list_of_predicted_intents)

    # Compute adjusted_rand_index.
    dict_of_clustering_performances[
        "adjusted_rand_index"
    ] = metrics.adjusted_rand_score(list_of_true_intents, list_of_predicted_intents)

    # Compute adjusted_mutual_information.
    dict_of_clustering_performances[
        "adjusted_mutual_information"
    ] = metrics.adjusted_mutual_info_score(
        list_of_true_intents, list_of_predicted_intents
    )

    # Store dictionary of clustering evaluation.
    with open(ENV_PATH + "dict_of_clustering_performances.json", "w") as file_performances:
        json.dump(dict_of_clustering_performances, file_performances, indent=1)

    # End of script.
    return 0
