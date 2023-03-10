# -*- coding: utf-8 -*-

"""
* Name:         listing_envs
* Description:  A set of method to list created interactive clustering business consistency study environments.
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
def get_list_of_dataset_env_paths() -> List[str]:
    """
    A method aimed at list relative paths to all datasets environments in `../experiments/` directory.
    Datasets environments are first level subfolder of `../experiments/` and have a `config.json` file.

    Returns:
        List[str]: The list of relative paths to the found dataset environments.
    """

    # Get datasets environments.
    list_of_dataset_env_paths: List[str] = [
        "../experiments/" + dataset_env_name + "/"
        for dataset_env_name in os.listdir("../experiments/")
        if (os.path.isdir("../experiments/" + dataset_env_name + "/"))
        and ("config.json" in os.listdir("../experiments/" + dataset_env_name + "/"))
    ]

    # Return expected environments.
    return list_of_dataset_env_paths


# ==============================================================================
# LISTING - CLUSTERING EVOLUTION ENVIRONMENTS PATH
# ==============================================================================
def get_list_of_clustering_evolution_env_paths() -> List[str]:
    """
    A method aimed at list relative paths to all clustering evolution environments in `../experiments/` directory.
    Clustering evolution environments are second level subfolder of `../experiments/` (i.e. are subfolder of dataset environments) and have a `config.json` file.

    Returns:
        List[str]: The list of relative paths to the found clustering evolution environments.
    """

    # Get the parent environments.
    list_of_datasets_env_paths: List[str] = get_list_of_dataset_env_paths()

    # Get clustering evolution environments.
    list_of_clustering_evolution_env_paths: List[str] = [
        dataset_env_name + clustering_env_name + "/"
        for dataset_env_name in list_of_datasets_env_paths
        for clustering_env_name in os.listdir(dataset_env_name)
        if (os.path.isdir(dataset_env_name + clustering_env_name + "/"))
        and ("config.json" in os.listdir(dataset_env_name + clustering_env_name + "/"))
    ]

    # Return expected environments.
    return list_of_clustering_evolution_env_paths
