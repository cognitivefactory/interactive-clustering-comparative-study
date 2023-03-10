# -*- coding: utf-8 -*-

"""
* Name:         workerA_run
* Description:  Worker to run an interactive clustering business relevance study experiment.
* Author:       Erwan Schild
* Created:      10/03/2023
* Licence:      CeCILL (https://cecill.info/licences.fr.html)
"""

# ==============================================================================
# IMPORT PYTHON DEPENDENCIES
# ==============================================================================

from typing import Any, Dict, List, Optional, Tuple
import json
import numpy as np
from scipy.sparse import csr_matrix, vstack
from cognitivefactory.features_maximization_metric.fmc import FeaturesMaximizationMetric
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC
from sklearn import metrics

# ==============================================================================
# WORKER - EXPERIMENT RUN
# ==============================================================================
def experiment_run(
    parameters: Dict[str, Any],
) -> int:
    """
    A worker to run an interactive clustering business relevance study on a convergence study (cf. study of efficience).
    Each experiment is evaluate with computation of :
    - clustering consistency score:
    - agreement score between annotations and previous clustering:
    - clustering stabilization score:
    - FMC modelization stabilization score:
    
    Usage note:
        - Parameters have to contain the path experiment to run. A dictionary is needed to get parameters in `multiprocessing.Pool.imap_unordered` call.
        - The name of the environment has to correspond to an experiment of efficience study, exported in a json file and stored in `../previous` folder.
        - The notebook `1_Evaluate_business_relevance.ipynb` launch this script for all defined experiment environments with the librairy `multiprocessing`.

    Args:
        parameters (Dict[str, Any]): A dictionary that contains several parameters. One key is expected in this dictionary: the experiment environment name (`"ENV_FILENAME"`).

    Returns:
        int: Return `0` when finish.
    """

    # Parameters.
    ENV_FILENAME: str = str(parameters["ENV_FILENAME"])
    
    # Initialize results.
    results: Dict[str, Dict[str, Any]] = {}


    ### ### ### ### ###
    ### Load needed configurations and data.
    ### ### ### ### ###
    
    # Load data.
    with open("../previous/" + ENV_FILENAME, "r") as experiment_file:
        experiment_data: Dict[str, Any] = json.load(experiment_file)
    
    # dict_of_preprocessed_texts
    dict_of_preprocessed_texts: Dict[str, str] = experiment_data["dict_of_preprocessed_texts"]
    
    # dict_of_true_intents
    dict_of_true_intents: Dict[str, str] = experiment_data["dict_of_true_intents"]
    
    # dict_of_constraints_annotations
    dict_of_constraints_annotations: Dict[str, List[Tuple[str, str, str]]] = experiment_data["dict_of_constraints_annotations"]
    
    # dict_of_clustering
    dict_of_clustering_results: Dict[str, Dict[str, str]] = experiment_data["dict_of_clustering_results"]


    ### ### ### ### ###
    ### Compute consistency score.
    ### ### ### ### ###
    
    # Initialize consistency score results.
    results["consistency_score"] = {}
    
    # Consistency on groundtruth.
    results["consistency_score"]["groundtruth"] = _compute_consistency_score(
        x_train = [
            dict_of_preprocessed_texts[text_ID]
            for text_ID in dict_of_preprocessed_texts.keys()
        ],
        y_train = [
            dict_of_true_intents[text_ID]
            for text_ID in dict_of_preprocessed_texts.keys()
        ],
        prediction_score_threshold = 0.75,
    )

    # Consistency on clustering.
    results["consistency_score"]["evolution"] = {
        iteration: _compute_consistency_score(
            x_train = [
                dict_of_preprocessed_texts[text_ID]
                for text_ID in dict_of_preprocessed_texts.keys()
            ],
            y_train = [
                str(dict_of_clustering_results[iteration][text_ID])
                for text_ID in dict_of_preprocessed_texts.keys()
            ],
            prediction_score_threshold = 0.75,
        )
        for iteration in dict_of_clustering_results.keys()
    }


    ### ### ### ### ###
    ### Agreement score between annotations and previous clustering.
    ### ### ### ### ###
    
    # Initialize agreement score results.
    results["agreement_score_between_annotations_and_previous_clustering"] = {
        "iteration-1": {},
    }
        
    # Loop on iterations
    previous_iteration = None
    for current_iteration in dict_of_clustering_results.keys():
        
        # Compute agreement.
        if previous_iteration is not None:
            results["agreement_score_between_annotations_and_previous_clustering"]["iteration-1"][current_iteration] = _compute_agreement_score_between_annotations_and_previous_clustering(
                annotations = dict_of_constraints_annotations[current_iteration],
                previous_clustering = dict_of_clustering_results[previous_iteration]
            )
            
        # Update temporary variables.
        previous_iteration = current_iteration


    ### ### ### ### ###
    ### Similarity score between two clustering.
    ### ### ### ### ###
    
    # Initialize agreement score results.
    results["similarity_score_between_two_clustering"] = {
        "groundtruth": {},
        "iteration-1": {},
        "iteration-2": {},
        "iteration-3": {},
    }
        
    # Loop on iterations
    previous_iteration = None
    preprevious_iteration = None
    prepreprevious_iteration = None
    for current_iteration in dict_of_clustering_results.keys():
    
        # Difference to groundtruth.
        results["similarity_score_between_two_clustering"]["groundtruth"][current_iteration] = metrics.v_measure_score(
            labels_true = [
                str(dict_of_true_intents[text_ID])
                for text_ID in dict_of_preprocessed_texts.keys()
            ],
            labels_pred = [
                str(dict_of_clustering_results[current_iteration][text_ID])
                for text_ID in dict_of_preprocessed_texts.keys()
            ],
        )
        
        # Difference to iteration-1.
        if previous_iteration is not None:
            results["similarity_score_between_two_clustering"]["iteration-1"][current_iteration] = metrics.v_measure_score(
                labels_true = [
                    str(dict_of_clustering_results[previous_iteration][text_ID])
                    for text_ID in dict_of_preprocessed_texts.keys()
                ],
                labels_pred = [
                    str(dict_of_clustering_results[current_iteration][text_ID])
                    for text_ID in dict_of_preprocessed_texts.keys()
                ],
            )
            
        # Difference to iteration-2.
        if preprevious_iteration is not None:
            results["similarity_score_between_two_clustering"]["iteration-2"][current_iteration] = metrics.v_measure_score(
                labels_true = [
                    str(dict_of_clustering_results[preprevious_iteration][text_ID])
                    for text_ID in dict_of_preprocessed_texts.keys()
                ],
                labels_pred = [
                    str(dict_of_clustering_results[current_iteration][text_ID])
                    for text_ID in dict_of_preprocessed_texts.keys()
                ],
            )
            
        # Difference to iteration-3.
        if prepreprevious_iteration is not None:
            results["similarity_score_between_two_clustering"]["iteration-3"][current_iteration] = metrics.v_measure_score(
                labels_true = [
                    str(dict_of_clustering_results[prepreprevious_iteration][text_ID])
                    for text_ID in dict_of_preprocessed_texts.keys()
                ],
                labels_pred = [
                    str(dict_of_clustering_results[current_iteration][text_ID])
                    for text_ID in dict_of_preprocessed_texts.keys()
                ],
            )
            
        # Update temporary variables.
        prepreprevious_iteration = preprevious_iteration
        preprevious_iteration = previous_iteration
        previous_iteration = current_iteration


    ### ### ### ### ###
    ### Similarity score between two FMC modelization.
    ### ### ### ### ###
    
    # Initialize agreement score results.
    results["similarity_score_between_two_fmc_modelization"] = {
        "groundtruth": {},
        "iteration-1": {},
        "iteration-2": {},
        "iteration-3": {},
    }
    
    # Define vectorizer for FMC computations.
    vectorizer = TfidfVectorizer(
        min_df=0,
        ngram_range=(1, 3),
        analyzer="word",
        sublinear_tf=True,
    )
    matrix_of_vectors: csr_matrix = vectorizer.fit_transform(
        [
            str(dict_of_preprocessed_texts[text_ID])
            for text_ID in dict_of_preprocessed_texts.keys()
        ]
    )
    list_of_possible_vectors_features: List[str] = list(vectorizer.get_feature_names_out())
    
    # Define groundtruth FMC modelization.
    grountruth_fmc_modelization: FeaturesMaximizationMetric = FeaturesMaximizationMetric(
        data_vectors = matrix_of_vectors,
        data_classes = [
            dict_of_true_intents[text_ID]
            for text_ID in dict_of_preprocessed_texts.keys()
        ],
        list_of_possible_features = list_of_possible_vectors_features,
        amplification_factor = 1,
    )
        
    # Loop on iterations
    previous_iteration = None
    previous_fmc_modelization: Optional[FeaturesMaximizationMetric] = None
    preprevious_iteration = None
    preprevious_fmc_modelization: Optional[FeaturesMaximizationMetric] = None
    prepreprevious_iteration = None
    prepreprevious_fmc_modelization: Optional[FeaturesMaximizationMetric] = None
    for current_iteration in dict_of_clustering_results.keys():
    
        # Define current clustering FMC modelization.
        current_fmc_modelization: FeaturesMaximizationMetric = FeaturesMaximizationMetric(
            data_vectors = matrix_of_vectors,
            data_classes = [
                dict_of_clustering_results[current_iteration][text_ID]
                for text_ID in dict_of_preprocessed_texts.keys()
            ],
            list_of_possible_features = list_of_possible_vectors_features,
            amplification_factor = 1,
        )
    
        # Difference to groundtruth.
        results["similarity_score_between_two_fmc_modelization"]["groundtruth"][current_iteration] = current_fmc_modelization.compare(
            fmc_reference = grountruth_fmc_modelization,
                rounded = 5,
            )[2]
        
        # Difference to iteration-1.
        if previous_iteration is not None:
            results["similarity_score_between_two_fmc_modelization"]["iteration-1"][current_iteration] = current_fmc_modelization.compare(
                fmc_reference = previous_fmc_modelization,
                rounded = 5,
            )[2]
            
        # Difference to iteration-2.
        if preprevious_iteration is not None:
            results["similarity_score_between_two_fmc_modelization"]["iteration-2"][current_iteration] = current_fmc_modelization.compare(
                fmc_reference = preprevious_fmc_modelization,
                rounded = 5,
            )[2]
            
        # Difference to iteration-3.
        if prepreprevious_iteration is not None:
            results["similarity_score_between_two_fmc_modelization"]["iteration-3"][current_iteration] = current_fmc_modelization.compare(
                fmc_reference = prepreprevious_fmc_modelization,
                rounded = 5,
            )[2]
            
        # Update temporary variables.
        prepreprevious_iteration = preprevious_iteration
        prepreprevious_fmc_modelization = preprevious_fmc_modelization
        preprevious_iteration = previous_iteration
        preprevious_fmc_modelization = previous_fmc_modelization
        previous_iteration = current_iteration
        previous_fmc_modelization = current_fmc_modelization


    ### ### ### ### ###
    ### Store computations.
    ### ### ### ### ###
    
    with open("../experiments/" + ENV_FILENAME, "w") as computation_file_w:
        json.dump(
            results,
            computation_file_w,
        )
        
    return 0


# ==============================================================================
# 1. CONSISTENCY SCORE
# ==============================================================================
def _compute_consistency_score(
    x_train: List[str],
    y_train: List[str],
    prediction_score_threshold: float = 0.75,
) -> float:
    """
    Test a TF-IDF + Linear SVM model on its own trainset with a high prediction score threshold in order to check data consistency.
    NB : if f1-score is low (i.e. less than 0.90), then trainset can be inconsistent. Data may be badly labeled or classes may overlap.
    
    Args:
        x_train (List[str]): List of texts.
        y_train (List[str]): List of labels.
        prediction_score_threshold (float): Prediction score threshold to accept a prediction. Defaults to `0.75`.
    
    Returns:
        float: Consitency score, i.e. f1-score on trainset.
    """
    # Define a classifier (TF-IDF + Linear SVM).
    classifier = Pipeline(
        [
            ("tfidf", TfidfVectorizer(min_df=0, ngram_range=(1, 3), analyzer="word", sublinear_tf=True)),
            ("clf", CalibratedClassifierCV(LinearSVC())),
        ],
        verbose=False,
    )
    
    # Train model.
    classifier.fit(x_train, y_train)
    
    # Test model with a hight prediction score threshold.
    y_predict = []
    for x in x_train:
    
        # Get model inference with sorted prediction scores.
        prediction_scores = classifier.predict_proba([x])[0]
        sorted_indexes = np.argsort(prediction_scores)
        sorted_prediction_scores = prediction_scores[sorted_indexes][::-1]
        sorted_prediction_classes = classifier.classes_[sorted_indexes].tolist()[::-1]
        
        # Get first model prediction if and only if it is the only one with a prediction score higher than threshold.
        if (
            sorted_prediction_scores[0] >= prediction_score_threshold  # best classe with prediction score higher than threshold.
            and sorted_prediction_scores[1] < prediction_score_threshold  # AND other classes with prediction scores lower than threshold.
        ):
            y_predict.append(sorted_prediction_classes[0])
        else:
            y_predict.append("")
    
    # Compute and return f1-score.
    return metrics.f1_score(
        y_true=y_train,
        y_pred=y_predict,
        average="macro",
    )
    
# ==============================================================================
# 2. AGREEMENT SCORE BETWEEN ANNOTATIONS AND PREVIOUS CLUSTERING
# ==============================================================================
def _compute_agreement_score_between_annotations_and_previous_clustering(
    annotations: List[Tuple[str, str, str]],
    previous_clustering: Dict[str, str]
) -> Optional[float]:
    """
    Compute the proportion of annotations that is similar to previous clustering results ("MUST_LINK" when same cluster, "CANNOT_LINK" when different clusters).
    If agreement is low (near to `0.0`), then constraints annotated will considerably fix clustering in next iteration.
    Otherwise, clustering is stable.
    
    Args:
        annotations (List[Tuple[str, str, str]): The constraints annotations during an iteration.
        previous_clustering (Dict[str, str]): The clustering result on the previous iteration.
        
    Returns:
        Optional[float]: The agreement between annotations and previous clustering. Can be `None` if there is no annotations.
    """
    
    # Initialize counters.
    ok: int = 0
    ko: int = 0
    skip: int = 0
    
    # loop on annotations...
    for annotation in annotations:
    
        # Get annotation and cluster result.
        cluster_data_1: int = previous_clustering[annotation[0]]
        cluster_data_2: int = previous_clustering[annotation[1]]
        constraint_type: str = annotation[2]
        
        # Case of agreement.
        if (
            (constraint_type == "MUST_LINK" and cluster_data_1 == cluster_data_2)
            or (constraint_type == "CANNOT_LINK" and cluster_data_1 != cluster_data_2)
        ):
            ok += 1
            
        # Case of disagreement.
        elif (
            (constraint_type == "MUST_LINK" and cluster_data_1 != cluster_data_2)
            or (constraint_type == "CANNOT_LINK" and cluster_data_1 == cluster_data_2)
        ):
            ko += 1
            
        # Case of not annotated.
        else:
            skip += 1

    # Return agreement score.
    return (
        ok / (ok + ko)
        if (ok + ko) != 0
        else None
    )
