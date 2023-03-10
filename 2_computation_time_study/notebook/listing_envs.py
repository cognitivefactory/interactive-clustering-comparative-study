# -*- coding: utf-8 -*-

"""
* Name:         listing_envs
* Description:  A set of method to list created interactive clustering computation time study environments.
* Author:       Erwan Schild
* Created:      09/11/2022
* Licence:      CeCILL (https://cecill.info/licences.fr.html)
"""

# ==============================================================================
# IMPORT PYTHON DEPENDENCIES
# ==============================================================================

import os
from typing import List 


# ==============================================================================
# LISTING - TASKS ENVIRONMENTS PATH
# ==============================================================================
def get_list_of_tasks_env_paths() -> List[str]:
    """
    A method aimed at list relative paths to all tasks environments in `../experiments/` directory.
    Tasks environments are first level subfolder of `../experiments/` and have a `config.json` file.

    Returns:
        List[str]: The list of relative paths to the found tasks environments.
    """

    # Get tasks environments.
    list_of_tasks_env_paths: List[str] = [
        "../experiments/" + task_env_name + "/"
        for task_env_name in os.listdir("../experiments/")
        if (os.path.isdir("../experiments/" + task_env_name + "/"))
        and ("config.json" in os.listdir("../experiments/" + task_env_name + "/"))
    ]

    # Return expected environments.
    return list_of_tasks_env_paths


# ==============================================================================
# LISTING - DATASET ENVIRONMENTS PATH
# ==============================================================================
def get_list_of_dataset_env_paths() -> List[str]:
    """
    A method aimed at list relative paths to all datasets environments in `../experiments/` directory.
    Datasets environments are second level subfolder of `../experiments/` (i.e. are subfolder of tasks environments) and have a `config.json` file.

    Returns:
        List[str]: The list of relative paths to the found dataset environments.
    """

    # Get the parent environments.
    list_of_tasks_env_paths: List[str] = get_list_of_tasks_env_paths()

    # Get dataset environments.
    list_of_dataset_env_paths: List[str] = [
        task_env_name + dataset_env_name + "/"
        for task_env_name in list_of_tasks_env_paths
        for dataset_env_name in os.listdir(task_env_name)
        if (os.path.isdir(task_env_name + dataset_env_name + "/"))
        and ("config.json" in os.listdir(task_env_name + dataset_env_name + "/"))
    ]

    # Return expected environments.
    return list_of_dataset_env_paths


# ==============================================================================
# LISTING - ALGORITHM ENVIRONMENTS PATH
# ==============================================================================
def get_list_of_algorithm_env_paths() -> List[str]:
    """
    A method aimed at list relative paths to all algorithms environments in `../experiments/` directory.
    Algorithms environments are third level subfolder of `../experiments/` (i.e. are subfolder of dataset environments) and have a `config.json` file.

    Returns:
        List[str]: The list of relative paths to the found algorithm environments.
    """

    # Get the parent environments.
    list_of_dataset_env_paths: List[str] = get_list_of_dataset_env_paths()

    # Get algorithm environments.
    list_of_algorithm_env_paths: List[str] = [
        dataset_environment + algorithm_env_name + "/"
        for dataset_environment in list_of_dataset_env_paths
        for algorithm_env_name in os.listdir(dataset_environment)
        if (os.path.isdir(dataset_environment + algorithm_env_name + "/"))
        and (
            "config.json"
            in os.listdir(dataset_environment + algorithm_env_name + "/")
        )
    ]

    # Return expected environments.
    return list_of_algorithm_env_paths
