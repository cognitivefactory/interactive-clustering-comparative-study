# -*- coding: utf-8 -*-

"""
* Name:         workerD_synthesis
* Description:  Worker to synthesize results of interactive clustering efficience study experiments in an CSV file.
* Author:       Erwan Schild
* Created:      24/05/2021
* Licence:      CeCILL (https://cecill.info/licences.fr.html)
"""

# ==============================================================================
# IMPORT PYTHON DEPENDENCIES
# ==============================================================================

import json
import pandas as pd

from typing import Dict, List, Optional, Tuple, Union


# ==============================================================================
# WORKER - EXPERIMENT OVERVIEW
# ==============================================================================
def experiments_synthesis(
    list_of_experiment_environments: List[str],
) -> int:
    """
    A method aimed at synthesize performance, annotation and time evolution of all experiments in a csv file.

    Args:
        list_of_experiment_environments (List[str]): The list of experiments environments used to synthesize results.

    Returns:
        int: Return `0` when finish.
    """

    # Define keys of dictionary of iterations that reach performance goals to use.
    LIST_OF_GOALS: List[str] = [
        "0.50v",
        "0.60v",
        "0.70v",
        "0.80v",
        "0.90v",
        "0.95v",
        "0.99v",
        "1.00v",
        "MAX",
    ]

    # Initialize dictionary of synthesis.
    dict_of_experiments_synthesis: Dict[
        str, Dict[str, Union[str, float, int, None]]
    ] = {}

    # For each experiment environment...
    for env_path in list_of_experiment_environments:

        # Initialize dictionary of synthesis for this experiment.
        dict_of_experiments_synthesis[env_path] = {}

        ### ### ### ### ###
        ### Configuration.
        ### ### ### ### ###

        # NB : environments paths are formatted links : `../experiments/[DATASET]/[PREPROCESSING]/[VECTORIZATION]/[SAMPLING]/[CLUSTERING]/[EXPERIMENT]/`

        # Dataset information.
        dict_of_experiments_synthesis[env_path]["dataset"] = env_path.split("/")[2]
        # Preprocessing information.
        dict_of_experiments_synthesis[env_path]["preprocessing"] = env_path.split("/")[
            3
        ]
        # Vectorization information.
        dict_of_experiments_synthesis[env_path]["vectorization"] = env_path.split("/")[
            4
        ]
        # Sampling information.
        dict_of_experiments_synthesis[env_path]["sampling"] = env_path.split("/")[5]
        # Clustering information.
        dict_of_experiments_synthesis[env_path]["clustering"] = env_path.split("/")[6]
        # Random_seed information.
        dict_of_experiments_synthesis[env_path]["random_seed"] = env_path.split("/")[7]

        # Load dictionary of iteration to highlight.
        with open(
            env_path + "dict_of_iterations_to_highlight.json", "r"
        ) as iteration_file:
            dict_of_iterations_to_highlight: Dict[
                str, Dict[str, Union[None, str, float]]
            ] = json.load(iteration_file)

        # Load dictionary of annotations.
        with open(
            env_path + "dict_of_constraints_annotations.json", "r"
        ) as annotation_file:
            dict_of_constraints_annotations: Dict[
                str, List[Tuple[str, str, Optional[str]]]
            ] = json.load(annotation_file)

        # Load dictionary of time spent.
        with open(env_path + "dict_of_computation_times.json", "r") as time_file:
            dict_of_computation_times: Dict[str, Dict[str, float]] = json.load(
                time_file
            )

        ### ### ### ### ###
        ### Iterations that reach specific performance goals.
        ### ### ### ### ###

        # For each performance goal to reach...
        for performance_goal in LIST_OF_GOALS:

            # Replace key for R variable usage.
            performance_id: str = "V" + performance_goal.replace(".", "")

            # Case of `None` (i.e. performance goal is not reached).
            if dict_of_iterations_to_highlight[performance_goal]["iteration"] is None:

                # Iteration to `None`.
                dict_of_experiments_synthesis[env_path][
                    performance_id + "__" + "iteration"
                ] = None

                # Time need for sampling to `None`.
                dict_of_experiments_synthesis[env_path][
                    performance_id + "__" + "sampling_time"
                ] = None
                # Time need for clustering to `None`.
                dict_of_experiments_synthesis[env_path][
                    performance_id + "__" + "clustering_time"
                ] = None
                # Total time needed to `None`.
                dict_of_experiments_synthesis[env_path][
                    performance_id + "__" + "total_time"
                ] = None

                # Number of annotated `"MUST_LINK"` constraints to `None`.
                dict_of_experiments_synthesis[env_path][
                    performance_id + "__" + "constraints_must_link"
                ] = None
                # Number of annotated `"CANNOT_LINK"` constraints to `None`.
                dict_of_experiments_synthesis[env_path][
                    performance_id + "__" + "constraints_cannot_link"
                ] = None
                # Total number of annotated constraints to `None`.
                dict_of_experiments_synthesis[env_path][
                    performance_id + "__" + "constraints_total"
                ] = None
                # Ratio of annotated constraints to `None`.
                dict_of_experiments_synthesis[env_path][
                    performance_id + "__" + "constraints_ratio_must_link"
                ] = None

            # Default case (i.e. performance goal is reached).
            else:

                # Get the iteration that reaches this performance goal for this experiment.
                iter_to_highlight: str = str(
                    dict_of_iterations_to_highlight[performance_goal]["iteration"]
                )

                # Iteration that reaches the performance goal.
                dict_of_experiments_synthesis[env_path][
                    performance_id + "__" + "iteration"
                ] = iter_to_highlight

                # Time need for sampling.
                dict_of_experiments_synthesis[env_path][
                    performance_id + "__" + "sampling_time"
                ] = sum(
                    [
                        time_t1["sampling_TOTAL_RUN"]
                        for iter_t1, time_t1 in dict_of_computation_times.items()
                        if iter_t1 <= iter_to_highlight
                    ]
                )
                # Time need for clustering.
                dict_of_experiments_synthesis[env_path][
                    performance_id + "__" + "clustering_time"
                ] = sum(
                    [
                        time_t2["clustering_TOTAL_RUN"]
                        for iter_t2, time_t2 in dict_of_computation_times.items()
                        if iter_t2 <= iter_to_highlight
                    ]
                )
                # Total time needed.
                dict_of_experiments_synthesis[env_path][
                    performance_id + "__" + "total_time"
                ] = sum(
                    [
                        time_t3["TOTAL_RUN"]
                        for iter_t3, time_t3 in dict_of_computation_times.items()
                        if iter_t3 <= iter_to_highlight
                    ]
                )

                # Number of annotated `"MUST_LINK"` constraints.
                dict_of_experiments_synthesis[env_path][
                    performance_id + "__" + "constraints_must_link"
                ] = len(
                    [
                        annotation_a1
                        for iter_a1, list_of_annotations_a1 in dict_of_constraints_annotations.items()
                        for annotation_a1 in list_of_annotations_a1
                        if iter_a1 <= iter_to_highlight
                        and annotation_a1[2] == "MUST_LINK"
                    ]
                )
                # Number of annotated `"CANNOT_LINK"` constraints.
                dict_of_experiments_synthesis[env_path][
                    performance_id + "__" + "constraints_cannot_link"
                ] = len(
                    [
                        annotation_a2
                        for iter_a2, list_of_annotations_a2 in dict_of_constraints_annotations.items()
                        for annotation_a2 in list_of_annotations_a2
                        if iter_a2 <= iter_to_highlight
                        and annotation_a2[2] == "CANNOT_LINK"
                    ]
                )
                # Total number of annotated constraints.
                dict_of_experiments_synthesis[env_path][
                    performance_id + "__" + "constraints_total"
                ] = len(
                    [
                        annotation_a3
                        for iter_a3, list_of_annotations_a3 in dict_of_constraints_annotations.items()
                        for annotation_a3 in list_of_annotations_a3
                        if iter_a3 <= iter_to_highlight and annotation_a3[2] is not None
                    ]
                )
                # Ratio of annotated constraints.
                dict_of_experiments_synthesis[env_path][
                    performance_id + "__" + "constraints_ratio_must_link"
                ] = (
                    None
                    if (
                        dict_of_experiments_synthesis[env_path][
                            performance_id + "__" + "constraints_total"
                        ]
                        == 0
                    )
                    else (
                        len(
                            [
                                annotation_a4
                                for iter_a4, list_of_annotations_a4 in dict_of_constraints_annotations.items()
                                for annotation_a4 in list_of_annotations_a4
                                if iter_a4 <= iter_to_highlight
                                and annotation_a4[2] == "MUST_LINK"
                            ]
                        )
                        / len(
                            [
                                annotation_a5
                                for iter_a5, list_of_annotations_a5 in dict_of_constraints_annotations.items()
                                for annotation_a5 in list_of_annotations_a5
                                if iter_a5 <= iter_to_highlight
                                and annotation_a5[2] is not None
                            ]
                        )
                    )
                )

    ### ### ### ### ###
    ### Store file.
    ### ### ### ### ###

    # Define file path.
    filepath: str = "../results/experiments_synthesis.csv"

    # Define dataframe and store it to a CSV file.
    pd.DataFrame.from_dict(data=dict_of_experiments_synthesis, orient="index",).to_csv(
        path_or_buf=filepath,
        sep=";",
    )

    # End of script.
    return 0
