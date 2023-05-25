# -*- coding: utf-8 -*-

"""
* Name:         workerA_run
* Description:  Worker to run an interactive clustering efficience study experiment.
* Author:       Erwan Schild
* Created:      24/05/2021
* Licence:      CeCILL (https://cecill.info/licences.fr.html)
"""

# ==============================================================================
# IMPORT PYTHON DEPENDENCIES
# ==============================================================================

import json
import pickle  # noqa: S403
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from cognitivefactory.interactive_clustering.clustering.abstract import (
    AbstractConstrainedClustering,
)
from cognitivefactory.interactive_clustering.clustering.factory import (
    clustering_factory,
)
from cognitivefactory.interactive_clustering.constraints.abstract import (
    AbstractConstraintsManager,
)
from cognitivefactory.interactive_clustering.constraints.factory import (
    managing_factory,
)
from cognitivefactory.interactive_clustering.sampling.abstract import (
    AbstractConstraintsSampling,
)
from cognitivefactory.interactive_clustering.sampling.factory import (
    sampling_factory,
)
from scipy.sparse import csr_matrix


# ==============================================================================
# WORKER - EXPERIMENT RUN
# ==============================================================================
def experiment_run(
    parameters: Dict[str, Any],
) -> int:
    """
    A worker to run an interactive clustering efficience study experiment.
    An experiment is aimed at iteratively and automatically annotated an NLP dataset with the interactive clustering methodology.
    At each iteration, the process samples data to annotate, annotates constraints on these data according to the groudtruth, then applies a constrained clustering.
    The loop ends when all possible combination of data are annotated with constraints, or when maximum iteration is reached.
    Then, go to the next step of the efficience study to evaluate results and convergence speed of this experiment.
    Usage note:
        - Parameters have to contain the path experiment to run. A dictionary is needed to get parameters in `multiprocessing.Pool.imap_unordered` call.
        - The path to the environment has to be formatted by the notebook `1_Initialize_convergence_experiments.ipynb`.
        - The notebook `2_Run_until_convergence_and_evaluate_efficience.ipynb` launch this script for all defined experiment environments with the librairy `multiprocessing`.

    Args:
        parameters (Dict[str, Any]): A dictionary that contains several parameters. Two keys are expected in this dictionary: the experiment environment path (`"ENV_PATH"`), the maximum iteration of interactive clustering (`"MAX_ITER"`).

    Returns:
        int: Return `0` when finish.
    """

    # Parameters.
    ENV_PATH: str = str(parameters["ENV_PATH"])
    MAX_ITER: Optional[int] = (
        None if (parameters["MAX_ITER"] is None) else int(parameters["MAX_ITER"])
    )

    ### ### ### ### ###
    ### Load needed configurations and data.
    ### ### ### ### ###

    # Load configuration for sampling.
    with open(ENV_PATH + "../../config.json", "r") as file_config_sampling:
        CONFIG_SAMPLING = json.load(file_config_sampling)

    # Load configuration for clustering.
    with open(ENV_PATH + "../config.json", "r") as file_config_clustering:
        CONFIG_CLUSTERING = json.load(file_config_clustering)

    # Load configuration for experiment.
    with open(ENV_PATH + "config.json", "r") as file_config_experiment:
        CONFIG_EXPERIMENT = json.load(file_config_experiment)

    ### ### ### ### ###
    ### Load needed data.
    ### ### ### ### ###

    # Load dict of true intents.
    with open(
        ENV_PATH + "../../../../../dict_of_true_intents.json", "r"
    ) as file_true_intents:
        dict_of_true_intents: Dict[str, str] = json.load(file_true_intents)

    # Get list of data IDs.
    list_of_data_IDs: List[str] = sorted(dict_of_true_intents.keys())

    # Load dict of vectors.
    with open(ENV_PATH + "../../../dict_of_vectors.pkl", "rb") as file_vectors:
        dict_of_vectors: Dict[str, csr_matrix] = pickle.load(file_vectors)  # noqa: S301

    ### ### ### ### ###
    ### Load storage files.
    ### ### ### ### ###

    # Load dictionary of clustering results.
    with open(ENV_PATH + "dict_of_clustering_results.json", "r") as file_clustering_results_load:
        dict_of_clustering_results: Dict[str, Dict[str, int]] = json.load(file_clustering_results_load)

    # Load dictionary of computation time.
    with open(ENV_PATH + "dict_of_computation_times.json", "r") as file_times_load:
        dict_of_computation_times: Dict[str, Dict[str, float]] = json.load(file_times_load)

    # Load dictionary of annotation history.
    with open(ENV_PATH + "dict_of_constraints_annotations.json", "r") as file_annotations_load:
        dict_of_constraints_annotations: Dict[
            str, List[Tuple[str, str, str]]
        ] = json.load(file_annotations_load)

    ### ### ### ### ###
    ### Define constraints manager.
    ### ### ### ### ###

    # Initialize constraints manager.
    constraints_manager: AbstractConstraintsManager = managing_factory(
        list_of_data_IDs=list_of_data_IDs,
        manager=CONFIG_EXPERIMENT["manager_type"],
    )

    # Update constraints manager.
    for _, list_of_triplet_annotated in dict_of_constraints_annotations.items():
        for previous_annotation in list_of_triplet_annotated:

            # Add constraint to the constraints manager.
            constraints_manager.add_constraint(
                data_ID1=previous_annotation[0],
                data_ID2=previous_annotation[1],
                constraint_type=previous_annotation[2],
            )

    ### ### ### ### ###
    ### Define iteration.
    ### ### ### ### ###

    # Define iteration.
    ITERATION: int = (
        max(
            [
                int(previous_iter_id)
                for previous_iter_id in dict_of_constraints_annotations.keys()
            ],
            default=-1,
        )
        + 1
    )
    ITERATION_ID: str = str(ITERATION).zfill(4)

    # Define previous iteration.
    PREV_ITERATION: Optional[int] = None if (ITERATION == 0) else (ITERATION - 1)

    ### ### ### ### ###
    ### Start interactive clustering iterations.
    ### ### ### ### ###

    # Do interactive clustering iteration until all constraints are annoted
    while (  # noqa: WPS352
        not constraints_manager.check_completude_of_constraints()
        and ((MAX_ITER is None) or (ITERATION <= MAX_ITER))
    ):

        ### ### ### ### ###
        ### Display iteration progress.
        ### ### ### ### ###

        # Compute iteration progress.
        iteration_progress: str = "it: " + ITERATION_ID

        ### ### ### ### ###
        ### Apply constraints sampling.
        ### ### ### ### ###

        # Time evaluation : start !
        TIME_sampling_start: float = datetime.timestamp(datetime.now())
        # Time evaluation : init !
        TIME_sampling_init: float = datetime.timestamp(datetime.now())

        # Sample data to annotate.
        list_of_tuple_to_annotate: List[Tuple[str, str]] = []
        if ITERATION != 0:

            # Get dict of predicted clusters on previous iteration.
            previous_clustering_result: Dict[str, int] = dict_of_clustering_results[
                str(PREV_ITERATION).zfill(4)
            ]

            # Initialize sampler
            sampler: AbstractConstraintsSampling = sampling_factory(
                algorithm=CONFIG_SAMPLING["algorithm"],
                random_seed=CONFIG_EXPERIMENT["random_seed"],
            )

            # Time evaluation : init !
            TIME_sampling_init = datetime.timestamp(datetime.now())

            # Sample data to annotate.
            list_of_tuple_to_annotate = sampler.sample(
                list_of_data_IDs=list_of_data_IDs,
                nb_to_select=CONFIG_SAMPLING["nb_to_select"],
                constraints_manager=constraints_manager,
                clustering_result=previous_clustering_result,
                vectors={
                    vector_id: csr_matrix(vector_value)
                    for vector_id, vector_value in dict_of_vectors.items()
                },
            )

            # Complete with random sampling if needed.
            if list_of_tuple_to_annotate == []:  # noqa: WPS520

                # Initialize new sampler
                random_sampler: AbstractConstraintsSampling = sampling_factory(
                    algorithm="random",
                    random_seed=CONFIG_EXPERIMENT["random_seed"],
                )

                # Sample data to annotate.
                list_of_tuple_to_annotate = random_sampler.sample(
                    list_of_data_IDs=list_of_data_IDs,
                    nb_to_select=CONFIG_SAMPLING["nb_to_select"],
                    constraints_manager=constraints_manager,
                    clustering_result=previous_clustering_result,
                    vectors={
                        vector_id: csr_matrix(vector_value)
                        for vector_id, vector_value in dict_of_vectors.items()
                    },
                )

        # Time evaluation : stop !
        TIME_sampling_stop: float = datetime.timestamp(datetime.now())

        ### ### ### ### ###
        ### Constraints annotation and management.
        ### ### ### ### ###

        # Apply automatic annotation.
        list_of_triplet_with_annotation: List[Tuple[str, str, str]] = []
        for data_sampled in list_of_tuple_to_annotate:

            # Estimate annotator answer (automation based on true intents comparison).

            # Case of "MUST_LINK".
            if (
                dict_of_true_intents[data_sampled[0]]
                == dict_of_true_intents[data_sampled[1]]
            ):
                list_of_triplet_with_annotation.append(
                    (data_sampled[0], data_sampled[1], "MUST_LINK")
                )

            # Case of "CANNOT_LINK".
            elif (
                dict_of_true_intents[data_sampled[0]]
                != dict_of_true_intents[data_sampled[1]]
            ):
                list_of_triplet_with_annotation.append(
                    (data_sampled[0], data_sampled[1], "CANNOT_LINK")
                )

        # Update constraints manager.
        for annotation in list_of_triplet_with_annotation:

            # Add constraint to the constraints manager (no conflicts possible)
            constraints_manager.add_constraint(
                data_ID1=annotation[0],
                data_ID2=annotation[1],
                constraint_type=annotation[2],
            )

        ### ### ### ### ###
        ### Constrained clustering.
        ### ### ### ### ###

        # Time evaluation : start !
        TIME_clustering_start: float = datetime.timestamp(datetime.now())

        # Initialize clustering model.
        clustering_model: AbstractConstrainedClustering = clustering_factory(
            algorithm=CONFIG_CLUSTERING["algorithm"],
            random_seed=CONFIG_EXPERIMENT["random_seed"],
            **CONFIG_CLUSTERING["init**kargs"],
        )

        # Time evaluation : init !
        TIME_clustering_init: float = datetime.timestamp(datetime.now())

        # Run clustering.
        current_clustering_result: Dict[str, int] = clustering_model.cluster(
            vectors={
                vector_id: csr_matrix(vector_value)
                for vector_id, vector_value in dict_of_vectors.items()
            },
            nb_clusters=CONFIG_CLUSTERING["nb_clusters"],
            constraints_manager=constraints_manager,
        )

        # Time evaluation : stop !
        TIME_clustering_stop: float = datetime.timestamp(datetime.now())

        ### ### ### ### ###
        ### Store computations.
        ### ### ### ### ###

        # Store dictionary of clustering results.
        with open(ENV_PATH + "dict_of_clustering_results.json", "w") as file_clustering_results_save:
            dict_of_clustering_results[ITERATION_ID] = current_clustering_result
            json.dump(dict_of_clustering_results, file_clustering_results_save, indent=1)

        # Store dictionary of computation time.
        with open(ENV_PATH + "dict_of_computation_times.json", "w") as file_time_save:
            dict_of_computation_times[ITERATION_ID] = {
                "sampling_start": TIME_sampling_start,
                "sampling_init": TIME_sampling_init,
                "sampling_stop": TIME_sampling_stop,
                "sampling_TOTAL_RUN": (TIME_sampling_stop - TIME_sampling_init),
                "clustering_start": TIME_clustering_start,
                "clustering_init": TIME_clustering_init,
                "clustering_stop": TIME_clustering_stop,
                "clustering_TOTAL_RUN": (
                    TIME_clustering_stop - TIME_clustering_init
                ),
                "TOTAL_RUN": (TIME_sampling_stop - TIME_sampling_init)
                + (TIME_clustering_stop - TIME_clustering_init),
            }
            json.dump(dict_of_computation_times, file_time_save, indent=1)

        # Store dictionary of annotation history.
        with open(
            ENV_PATH + "dict_of_constraints_annotations.json", "w"
        ) as file_annotations_save:
            dict_of_constraints_annotations[
                ITERATION_ID
            ] = list_of_triplet_with_annotation
            json.dump(dict_of_constraints_annotations, file_annotations_save, indent=1)

        ### ### ### ### ###
        ### Update iteration.
        ### ### ### ### ###

        # Update previous iteration.
        PREV_ITERATION = ITERATION  # PREV_ITERATION = (PREV_ITERATION + 1) if (PREV_ITERATION is not None) else 0

        # Update iteration.
        ITERATION += 1
        ITERATION_ID = str(ITERATION).zfill(4)

    # Write a ".done" file when convergence.
    with open(
        ENV_PATH + ".done", "a"
    ) as file_done:
        pass
    return 0
