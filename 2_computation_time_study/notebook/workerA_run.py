# -*- coding: utf-8 -*-

"""
* Name:         workerA_run
* Description:  Worker to estimate the interactive clustering computation time.
* Author:       Erwan Schild
* Created:      09/11/2022
* Licence:      CeCILL (https://cecill.info/licences.fr.html)
"""

# ==============================================================================
# IMPORT PYTHON DEPENDENCIES
# ==============================================================================

import json
import pickle  # noqa: S403
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from cognitivefactory.interactive_clustering.utils.preprocessing import (
    preprocess,
)
from cognitivefactory.interactive_clustering.utils.vectorization import (
    vectorize,
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
    A worker to estimate the interactive clustering computation time.
    Several task can be evaluate: preprocessing, vectorization, sampling and clustering.
    During each experiment, only one task is evaluate, but several can be run in order to get the needed data (ex: performing data preprocessing, data vectorization and constraints modelization before performing constrained clustering).
    Usage note:
        - Parameters have to contain the path experiment to run. A dictionary is needed to get parameters in `multiprocessing.Pool.imap_unordered` call.
        - The path to the environment has to be formatted by the notebook `1_Initialize_computation_time_experiments.ipynb`.
        - The notebook `2_Estimate_computation_time.ipynb` launch this script for all defined experiment environments with the librairy `multiprocessing`.

    Args:
        parameters (Dict[str, Any]): A dictionary that contains several parameters. Several keys are expected in this dictionary: the experiment environment path (`"ENV_PATH"`), the task to evaluate (`"_TASK"`) and many settings dependening on evaluated task.

    Returns:
        int: Return `0` when finish.
    """

    # Parameters.
    ENV_PATH: str = str(parameters["ENV_PATH"])
        
    # If experiment was already run: skip.
    if "computation_time.json" in os.listdir(ENV_PATH):

        # End of script.
        return 0

    ### ### ### ### ###
    ### Load needed configurations and data.
    ### ### ### ### ###

    # Load configuration for algorithm.
    with open(
        ENV_PATH + "config.json", "r"
    ) as file_config_algorithm:
        CONFIG_ALGORITHM = json.load(file_config_algorithm)

    ### ### ### ### ###
    ### Load needed data.
    ### ### ### ### ###

    # Load dict of true intents.
    with open(
        ENV_PATH + "../dict_of_texts.json", "r"
    ) as file_texts:
        dict_of_texts: Dict[str, str] = json.load(file_texts)

    # Load dict of true intents.
    with open(
        ENV_PATH + "../dict_of_true_intents.json", "r"
    ) as file_true_intents:
        dict_of_true_intents: Dict[str, str] = json.load(file_true_intents)
            
    # Define list of data IDs.
    list_of_data_IDs: List[str] = list(dict_of_texts.keys())

    ### ### ### ### ###
    ### Initialize time counter.
    ### ### ### ### ###
    
    time_start: float = 0.0
    time_stop: float = 0.0
    time_total: float = 0.0
            
    ### ### ### ### ###
    ### Data preprocessing
    ### ### ### ### ###
    
    # Preprocess.
    time_start = datetime.timestamp(datetime.now())
    dict_of_preprocessed_texts: Dict[str, str] = preprocess(
        dict_of_texts=dict_of_texts,
        apply_lemmatization=bool(CONFIG_ALGORITHM["preprocessing"]["apply_lemmatization"]),
        apply_parsing_filter=bool(CONFIG_ALGORITHM["preprocessing"]["apply_parsing_filter"]),
        spacy_language_model=str(CONFIG_ALGORITHM["preprocessing"]["spacy_language_model"]),
    )
    time_stop = datetime.timestamp(datetime.now())
    
    # If _TASK == "preprocessing": store computation time and exit.
    if CONFIG_ALGORITHM["_TASK"] == "preprocessing":
        with open(ENV_PATH + "computation_time.json", "w") as file_time_preprocessing:
            json.dump(
                {
                    "start": time_start,
                    "stop": time_stop,
                    "total": (time_stop - time_start),
                },
                file_time_preprocessing,
            )
        return 0
            
    ### ### ### ### ###
    ### Data vectorization
    ### ### ### ### ###
    
    # Vectorize.
    time_start = datetime.timestamp(datetime.now())
    dict_of_vectors: Dict[str, csr_matrix] = vectorize(
        dict_of_texts=dict_of_preprocessed_texts,
        vectorizer_type=str(CONFIG_ALGORITHM["vectorization"]["vectorizer_type"]),
        spacy_language_model=str(CONFIG_ALGORITHM["vectorization"]["spacy_language_model"]),
    )
    time_stop = datetime.timestamp(datetime.now())
    
    # If _TASK == "vectorization": store computation time and exit.
    if CONFIG_ALGORITHM["_TASK"] == "vectorization":
        with open(ENV_PATH + "computation_time.json", "w") as file_time_vectorization:
            json.dump(
                {
                    "start": time_start,
                    "stop": time_stop,
                    "total": (time_stop - time_start),
                },
                file_time_vectorization,
            )
        return 0
    

    ### ### ### ### ###
    ### Generate needed data.
    ### ### ### ### ###
    
    # Initialize constraints manager.
    constraints_manager: AbstractConstraintsManager = managing_factory(
        manager="binary",
        list_of_data_IDs=list_of_data_IDs,
    )
        
    # Generate previous constraints.
    list_of_previous_constraints: List[Tuple[str, str]] = sampling_factory(
        algorithm="random",
        random_seed=CONFIG_ALGORITHM["random_seed"],
    ).sample(
        constraints_manager=constraints_manager,
        nb_to_select=CONFIG_ALGORITHM["previous"]["constraints"],
    )
        
    # Add constraint to the constraints manager (according to the groundtruth for this experiment).
    for constraint in list_of_previous_constraints:
        data_ID1: str = constraint[0]
        data_ID2: str = constraint[1]
        constraints_manager.add_constraint(
            data_ID1=data_ID1,
            data_ID2=data_ID2,
            constraint_type=(
                "MUST_LINK"
                if dict_of_true_intents[data_ID1] == dict_of_true_intents[data_ID2]
                else "CANNOT_LINK"
            ),
        )
        
    # Generate previous clustering.
    dict_of_previous_clusters: Dict[str, int] = {}
    if CONFIG_ALGORITHM["_TASK"] == "sampling":
        dict_of_previous_clusters = clustering_factory(
            algorithm="kmeans",
            random_seed=CONFIG_ALGORITHM["random_seed"],
            max_iteration=10,
        ).cluster(
            vectors=dict_of_vectors,
            nb_clusters=CONFIG_ALGORITHM["previous"]["clustering"],
            constraints_manager=constraints_manager,
        )

            
    ### ### ### ### ###
    ### Constraints sampling
    ### ### ### ### ###
    
    # If _TASK == "sampling":
    if CONFIG_ALGORITHM["_TASK"] == "sampling":

        # Sampling.
        time_start = datetime.timestamp(datetime.now())
        sampling_factory(
            algorithm=CONFIG_ALGORITHM["sampling"]["algorithm"],
            random_seed=CONFIG_ALGORITHM["random_seed"],
        ).sample(
            constraints_manager=constraints_manager,
            nb_to_select=CONFIG_ALGORITHM["sampling"]["nb_to_select"],
            clustering_result=dict_of_previous_clusters,
            vectors=dict_of_vectors,
        )
        time_stop = datetime.timestamp(datetime.now())
    
        # Store computation time and exit.
        with open(ENV_PATH + "computation_time.json", "w") as file_time_sampling:
            json.dump(
                {
                    "start": time_start,
                    "stop": time_stop,
                    "total": (time_stop - time_start),
                },
                file_time_sampling,
            )
        return 0
            
    ### ### ### ### ###
    ### Constrained clustering
    ### ### ### ### ###
    
    # If _TASK == "clustering":
    if CONFIG_ALGORITHM["_TASK"] == "clustering":
    
        # Clustering.
        time_start = datetime.timestamp(datetime.now())
        clustering_factory(
            algorithm=CONFIG_ALGORITHM["clustering"]["algorithm"],
            random_seed=CONFIG_ALGORITHM["random_seed"],
            **CONFIG_ALGORITHM["clustering"]["init**kargs"],
        ).cluster(
            vectors=dict_of_vectors,
            nb_clusters=CONFIG_ALGORITHM["clustering"]["nb_clusters"],
            constraints_manager=constraints_manager,
        )
        time_stop = datetime.timestamp(datetime.now())
    
        # Store computation time and exit.
        with open(ENV_PATH + "computation_time.json", "w") as file_time_clustering:
            json.dump(
                {
                    "start": time_start,
                    "stop": time_stop,
                    "total": (time_stop - time_start),
                },
                file_time_clustering,
            )
        return 0
   
    # End of script.
    return 0