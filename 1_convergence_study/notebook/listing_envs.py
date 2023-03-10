# -*- coding: utf-8 -*-

"""
* Name:         listing_envs
* Description:  A set of method to list created interactive clustering convergence study environments.
* Author:       Erwan Schild
* Created:      24/05/2021
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
# LISTING - PREPROCESSING ENVIRONMENTS PATH
# ==============================================================================
def get_list_of_preprocessing_env_paths() -> List[str]:
    """
    A method aimed at list relative paths to all preprocessing environments in `../experiments/` directory.
    Preprocessing environments are second level subfolder of `../experiments/` (i.e. are subfolder of dataset environments) and have a `config.json` file.

    Returns:
        List[str]: The list of relative paths to the found preprocessing environments.
    """

    # Get the parent environments.
    list_of_dataset_env_paths: List[str] = get_list_of_dataset_env_paths()

    # Get preprocessing environments.
    list_of_preprocessing_env_paths: List[str] = [
        dataset_environment + preprocessing_env_name + "/"
        for dataset_environment in list_of_dataset_env_paths
        for preprocessing_env_name in os.listdir(dataset_environment)
        if (os.path.isdir(dataset_environment + preprocessing_env_name + "/"))
        and (
            "config.json"
            in os.listdir(dataset_environment + preprocessing_env_name + "/")
        )
    ]

    # Return expected environments.
    return list_of_preprocessing_env_paths


# ==============================================================================
# LISTING - VECTORIZATION ENVIRONMENTS PATH
# ==============================================================================
def get_list_of_vectorization_env_paths() -> List[str]:
    """
    A method aimed at list relative paths to all vectorization environments in `../experiments/` directory.
    Vectorization environments are third level subfolder of `../experiments/` (i.e. are subfolder of preprocessing environments) and have a `config.json` file.

    Returns:
        List[str]: The list of relative paths to the found vectorization environments.
    """

    # Get the parent environments
    list_of_preprocessing_env_paths: List[str] = get_list_of_preprocessing_env_paths()

    # Get vectorization environments.
    list_of_vectorization_env_paths: List[str] = [
        preprocessing_environment + vectorization_env_name + "/"
        for preprocessing_environment in list_of_preprocessing_env_paths
        for vectorization_env_name in os.listdir(preprocessing_environment)
        if (os.path.isdir(preprocessing_environment + vectorization_env_name + "/"))
        and (
            "config.json"
            in os.listdir(preprocessing_environment + vectorization_env_name + "/")
        )
    ]

    # Return expected environments.
    return list_of_vectorization_env_paths


# ==============================================================================
# LISTING - SAMPLING ENVIRONMENTS PATH
# ==============================================================================
def get_list_of_sampling_env_paths() -> List[str]:
    """
    A method aimed at list relative paths to all sampling environments in `../experiments/` directory.
    Sampling environments are third level subfolder of `../experiments/` (i.e. are subfolder of vectorization environments) and have a `config.json` file.

    Returns:
        List[str]: The list of relative paths to the found sampling environments.
    """

    # Get the parent environments
    list_of_vectorization_env_paths: List[str] = get_list_of_vectorization_env_paths()

    # Get sampling environments.
    list_of_sampling_env_paths: List[str] = [
        vectorization_env_path + sampling_env_name + "/"
        for vectorization_env_path in list_of_vectorization_env_paths
        for sampling_env_name in os.listdir(vectorization_env_path)
        if (os.path.isdir(vectorization_env_path + sampling_env_name + "/"))
        and (
            "config.json"
            in os.listdir(vectorization_env_path + sampling_env_name + "/")
        )
    ]

    # Return expected environments.
    return list_of_sampling_env_paths


# ==============================================================================
# LISTING - CLUSTERING ENVIRONMENTS PATH
# ==============================================================================
def get_list_of_clustering_env_paths() -> List[str]:
    """
    A method aimed at list relative paths to all clustering environments in `../experiments/` directory.
    Clustering environments are third level subfolder of `../experiments/` (i.e. are subfolder of sampling environments) and have a `config.json` file.

    Returns:
        List[str]: The list of relative paths to the found clustering environments.
    """

    # Get the parent environments
    list_of_sampling_env_paths: List[str] = get_list_of_sampling_env_paths()

    # Get clustering environments.
    list_of_clustering_env_paths: List[str] = [
        sampling_env_path + clustering_env_name + "/"
        for sampling_env_path in list_of_sampling_env_paths
        for clustering_env_name in os.listdir(sampling_env_path)
        if (os.path.isdir(sampling_env_path + clustering_env_name + "/"))
        and ("config.json" in os.listdir(sampling_env_path + clustering_env_name + "/"))
    ]

    # Return expected environments.
    return list_of_clustering_env_paths


# ==============================================================================
# LISTING - EXPERIMENT ENVIRONMENTS PATH
# ==============================================================================
def get_list_of_experiment_env_paths() -> List[str]:
    """
    A method aimed at list relative paths to all experiments environments in `../experiments/` directory.
    Experiments environments are third level subfolder of `../experiments/` (i.e. are subfolder of clustering environments) and have a `config.json` file.

    Returns:
        List[str]: The list of relative paths to the found experiment environments.
    """

    # Get the parent environments
    list_of_clustering_env_paths: List[str] = get_list_of_clustering_env_paths()

    # Get experiment environments.
    list_of_experiment_env_paths: List[str] = [
        clustering_env_path + experiment_env_name + "/"
        for clustering_env_path in list_of_clustering_env_paths
        for experiment_env_name in os.listdir(clustering_env_path)
        if (os.path.isdir(clustering_env_path + experiment_env_name + "/"))
        and (
            "config.json" in os.listdir(clustering_env_path + experiment_env_name + "/")
        )
    ]

    # Return expected environments.
    return list_of_experiment_env_paths
