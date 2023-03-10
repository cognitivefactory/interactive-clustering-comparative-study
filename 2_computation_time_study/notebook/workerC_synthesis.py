# -*- coding: utf-8 -*-

"""
* Name:         workerC_synthesis
* Description:  Worker to synthesize results of interactive clustering computation time study experiments in an CSV file.
* Author:       Erwan Schild
* Created:      09/11/2022
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
    A method aimed at synthesize performance of all experiments in a csv file.

    Args:
        list_of_experiment_environments (List[str]): The list of experiments environments used to synthesize results.

    Returns:
        int: Return `0` when finish.
    """

    # Initialize dictionary of synthesis.
    dict_of_experiments_synthesis: Dict[
        str, Dict[
            str, Dict[
                str, Union[str, float, int, None]
            ]
        ]
    ] = {}

    # For each experiment environment...
    for env_path in list_of_experiment_environments:

        ### ### ### ### ###
        ### Load files.
        ### ### ### ### ###
        
        # Load configuration for tasks.
        with open(
            env_path + "config.json", "r"
        ) as file_config_task:
            CONFIG_TASK = json.load(file_config_task)
        
        # Load configuration for datasets.
        with open(
            env_path + "../config.json", "r"
        ) as file_config_dataset:
            CONFIG_DATASET = json.load(file_config_dataset)
        
        # Load configuration for algorithms.
        with open(
            env_path + "config.json", "r"
        ) as file_config_algorithm:
            CONFIG_ALGORITHM = json.load(file_config_algorithm)
        
        # Load computation time.
        with open(
            env_path + "computation_time.json", "r"
        ) as file_computation_time:
            COMPUTATION_TIME = json.load(file_computation_time)

        ### ### ### ### ###
        ### Initialize.
        ### ### ### ### ###
        
        # Get the task.
        task: str = CONFIG_ALGORITHM["_TASK"]

        # Initialize dictionary of synthesis for this experiment.
        if task not in dict_of_experiments_synthesis.keys():
            dict_of_experiments_synthesis[task] = {}
        dict_of_experiments_synthesis[task][env_path] = {}

        # NB : environments paths are formatted links : `../experiments/[TASK]/[DATASET]/[ALGORITHM]`

        ### ### ### ### ###
        ### Store needeed data.
        ### ### ### ### ###
        
        # dataset - name
        dict_of_experiments_synthesis[task][env_path]["dataset_name"] = CONFIG_DATASET["dataset"]
        # dataset - size
        dict_of_experiments_synthesis[task][env_path]["dataset_size"] = CONFIG_DATASET["size"]
        # dataset - random_seed
        dict_of_experiments_synthesis[task][env_path]["dataset_random_seed"] = CONFIG_DATASET["random_seed"]
        
        # previous - nb_constraints
        if task in {"sampling", "clustering"}:
            dict_of_experiments_synthesis[task][env_path]["previous_nb_constraints"] = CONFIG_ALGORITHM["previous"]["constraints"]
        # previous - nb_clusters
        if task == "sampling":
            dict_of_experiments_synthesis[task][env_path]["previous_nb_clusters"] = CONFIG_ALGORITHM["previous"]["clustering"]
        
        # algorithm - name
        dict_of_experiments_synthesis[task][env_path]["algorithm_name"] = CONFIG_ALGORITHM["_ALGORITHM"]
        # algorithm - random_seed
        dict_of_experiments_synthesis[task][env_path]["algorithm_random_seed"] = CONFIG_ALGORITHM["random_seed"]
        # algorithm - nb_to_select
        if task == "sampling":
            dict_of_experiments_synthesis[task][env_path]["algorithm_nb_to_select"] = CONFIG_ALGORITHM["sampling"]["nb_to_select"]
        # algorithm - nb_clusters
        if task == "clustering":
            dict_of_experiments_synthesis[task][env_path]["algorithm_nb_clusters"] = CONFIG_ALGORITHM["clustering"]["nb_clusters"]
        
        # time - start
        dict_of_experiments_synthesis[task][env_path]["time_start"] = str(COMPUTATION_TIME["start"]).replace(".", ",")
        # time - stop
        dict_of_experiments_synthesis[task][env_path]["time_stop"] = str(COMPUTATION_TIME["stop"]).replace(".", ",")
        # time - total
        dict_of_experiments_synthesis[task][env_path]["time_total"] = str(COMPUTATION_TIME["total"]).replace(".", ",")

    ### ### ### ### ###
    ### Store file.
    ### ### ### ### ###

    # Define file path.
    filepath: str = "../results/experiments_synthesis_for_{task}.csv"

    # Define dataframe and store it to a CSV file.
    for task_evaluated in dict_of_experiments_synthesis.keys():
        pd.DataFrame.from_dict(
            data=dict_of_experiments_synthesis[task_evaluated],
            orient="index",
        ).to_csv(
            path_or_buf=filepath.format(task=task_evaluated),
            sep=";",
        )

    # End of script.
    return 0
