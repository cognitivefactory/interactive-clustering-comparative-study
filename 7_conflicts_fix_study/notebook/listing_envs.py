# -*- coding: utf-8 -*-

"""
* Name:         listing_envs
* Description:  A set of method to list created interactive clustering conflicts fix study environments.
* Author:       Erwan Schild
* Created:      24/10/2022
* Licence:      CeCILL (https://cecill.info/licences.fr.html)
"""

# ==============================================================================
# IMPORT PYTHON DEPENDENCIES
# ==============================================================================

import os
from typing import List


# ==============================================================================
# LISTING - DATASET ENVIRONMENTS PATH
# ==============================================================================
def get_list_of_dataset_env_paths() -> List[str]:
    """
    A method aimed at list relative paths to all datasets environments in `../experiments/` directory.
    Datasets environments are first level subfolder of `../experiments/` and have a `config.json` file.

    Returns:
        List[str]: The list of relative paths to the found dataset environments.
    """

    # Get dataset environments.
    list_of_dataset_env_paths: List[str] = [
        "../experiments/" + dataset_env_name + "/"
        for dataset_env_name in os.listdir("../experiments/")
        if (os.path.isdir("../experiments/" + dataset_env_name + "/"))
        and ("config.json" in os.listdir("../experiments/" + dataset_env_name + "/"))
    ]

    # Return expected environments.
    return list_of_dataset_env_paths


# ==============================================================================
# LISTING - ALGORITHM ENVIRONMENTS PATH
# ==============================================================================
def get_list_of_algorithm_env_paths() -> List[str]:
    """
    A method aimed at list relative paths to all algorithms environments in `../experiments/` directory.
    Algorithms environments are second level subfolder of `../experiments/` (i.e. are subfolder of dataset environments) and have a `config.json` file.

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


# ==============================================================================
# LISTING - CONSTRAINTS SELECTION ENVIRONMENTS PATH
# ==============================================================================
def get_list_of_constraints_selection_env_paths() -> List[str]:
    """
    A method aimed at list relative paths to all constraints selection environments in `../experiments/` directory.
    Constraints selection environments are third level subfolder of `../experiments/` (i.e. are subfolder of algorithm environments) and have a `config.json` file.

    Returns:
        List[str]: The list of relative paths to the found constraints selection environments.
    """

    # Get the parent environments
    list_of_algorithm_env_paths: List[str] = get_list_of_algorithm_env_paths()

    # Get constraints selection environments.
    list_of_constraints_selection_env_paths: List[str] = [
        algorithm_environment + constraints_selection_env_name + "/"
        for algorithm_environment in list_of_algorithm_env_paths
        for constraints_selection_env_name in os.listdir(algorithm_environment)
        if (os.path.isdir(algorithm_environment + constraints_selection_env_name + "/"))
        and (
            "config.json"
            in os.listdir(algorithm_environment + constraints_selection_env_name + "/")
        )
    ]

    # Return expected environments.
    return list_of_constraints_selection_env_paths


# ==============================================================================
# LISTING - ERROR SIMULATION ENVIRONMENTS PATH
# ==============================================================================
def get_list_of_errors_simulation_env_paths() -> List[str]:
    """
    A method aimed at list relative paths to all errors simulation environments in `../experiments/` directory.
    Errors simulation environments are fourth level subfolder of `../experiments/` (i.e. are subfolder of constraints selection environments) and have a `config.json` file.

    Returns:
        List[str]: The list of relative paths to the found error simulation environments.
    """

    # Get the parent environments
    list_of_constraints_selection_env_paths: List[str] = get_list_of_constraints_selection_env_paths()

    # Get errors simulation environments.
    list_of_errors_simulation_env_paths: List[str] = [
        constraints_selection_env_path + errors_simulation_env_name + "/"
        for constraints_selection_env_path in list_of_constraints_selection_env_paths
        for errors_simulation_env_name in os.listdir(constraints_selection_env_path)
        if (os.path.isdir(constraints_selection_env_path + errors_simulation_env_name + "/"))
        and (
            "config.json"
            in os.listdir(constraints_selection_env_path + errors_simulation_env_name + "/")
        )
    ]

    # Return expected environments.
    return list_of_errors_simulation_env_paths
