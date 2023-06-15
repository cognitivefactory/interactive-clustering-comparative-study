# -*- coding: utf-8 -*-

"""
* Name:         consistency_score
* Description:  Compute constistency score of a dataset.
* Author:       Erwan Schild
* Created:      10/03/2023
* Licence:      CeCILL (https://cecill.info/licences.fr.html)
"""

# ==============================================================================
# IMPORT PYTHON DEPENDENCIES
# ==============================================================================

from typing import List, Dict, Optional, Any
import json
import numpy as np
from scipy import stats as scipystats
from cognitivefactory.features_maximization_metric.fmc import FeaturesMaximizationMetric
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC
from sklearn import metrics
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

# ==============================================================================
# 1. COMPUTE CONSISTENCY SCORE
# ==============================================================================
def compute_consistency_score(
    x_train: List[str],
    y_train: List[str],
    prediction_score_threshold: float = 0.75,
) -> float:
    """
    Test a TF-IDF + Linear SVM model on its own trainset with a high prediction score threshold in order to check data consistency.
    NB : if f1-score is low (i.e. less than 0.75), then trainset can be inconsistent. Data may be badly labeled or classes may overlap.
    
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
# 2. DISPLAY CONSISTENCY SCORE EVOLUTION
# ==============================================================================
def display_consistency_score(
    implementation: str,
    list_of_experiments: List[str],
    list_of_iterations: Optional[List[str]] = None,
    plot_label: str = "Score de cohérence du clustering.",
    plot_color: str = "black",
    graph_filename: str = "consistency_score.png",
) -> Figure:
    """
    Display consistency score per iteration.
    
    Args:
        implementation (str): The folder that represents the folder to display.
        list_of_experiments (List[str]). The list of files that represent experiments to analyze.
        list_of_iterations (Optional[List[str]]): The list of iterations used for display. Defaults to `None`.
        plot_label (str): The label of the plot. Defaults to `"Score de cohérence du clustering."`.
        plot_color (str): The color of plot. Defaults to `"black"`.
        graph_filename (str): The graph filename. Default to `"consistency_score.png"`.
        
    Returns:
        Figure: Figure of consistency score evolution.
    """
    
    # Definition of list_of_iteration:
    if list_of_iterations is None:
        
        # Initialize maximum iteration.
        max_iteration: str = "0000"
    
        # For each experiment...
        for exp1 in list_of_experiments:

            # Load data for the experiment.
            with open("../experiments/" + implementation + "/previous_results___" + exp1, "r") as file_data_r:
                dict_of_clustering_results: Dict[str, Any] = json.load(file_data_r)["dict_of_clustering_results"]

            # Update meximum iteration.
            max_iteration = max(
                max(dict_of_clustering_results.keys()),
                max_iteration,
            )

        # Update list of iterations
        list_of_iterations: List[str] = [
            str(i).zfill(4)
            for i in range(int(max_iteration))
        ]

    # Initialize storage of experiment consistency for all iterations.
    dict_of_consistency_evolution: Dict[str, List[float]] = {
        iter_cons: [] for iter_cons in list_of_iterations
    }

    # Initialize storage of groundtruth consistency.
    groundtruth_consistency_score: str = 0.0

    # For each experiment...
    for exp2 in list_of_experiments:

        # Load data for the experiment.
        with open("../experiments/" + implementation + "/constistency_score___" + exp2, "r") as file_scores_r:
            experiment_scores: Dict[str, Any] = json.load(file_scores_r)

        # Get groundtruth consistency (same for all experiments).
        groundtruth_consistency_score = experiment_scores["groundtruth"]
        
        # For each requested iteration...
        for iter_a in list_of_iterations:

            # Append the clustering consistency for the current experiment and for this iteration.
            if iter_a in experiment_scores["evolution"].keys():
                dict_of_consistency_evolution[iter_a].append(
                    experiment_scores["evolution"][iter_a]
                )
            # If iteration isn't reached by this experiment, duplicate the last known results.
            else:
                dict_of_consistency_evolution[iter_a].append(
                    experiment_scores["groundtruth"]
                )
        

    # Initialize storage of experiment consistency mean for all iterations.
    dict_of_consistency_evolution_MEAN: Dict[str, float] = {
        iter_mean: np.mean(dict_of_consistency_evolution[iter_mean])
        for iter_mean in list_of_iterations
    }
    # Initialize storage of experiment consistency standard error of the mean for all iterations.
    dict_of_consistency_evolution_SEM: Dict[str, float] = {
        iter_sem: scipystats.sem(dict_of_consistency_evolution[iter_sem])
        for iter_sem in list_of_iterations
    }
    
    # Create a new figure.
    fig_plot: Figure = plt.figure(figsize=(15, 7.5), dpi=300)
    axis_plot = fig_plot.gca()

    # Set range of axis.
    axis_plot.set_xlim(xmin=-0.5, xmax=int(max(list_of_iterations))+1.5)
    axis_plot.set_ylim(ymin=-0.01, ymax=1.01)

    # Plot average clustering consistency evolution.
    axis_plot.plot(
        [int(iter_mean) for iter_mean in list_of_iterations],  # x
        [dict_of_consistency_evolution_MEAN[iter_mean] for iter_mean in list_of_iterations],  # y
        label=plot_label,
        marker="",
        markerfacecolor=plot_color,
        markersize=5,
        color=plot_color,
        linewidth=2,
        linestyle="--",
    )
    axis_plot.fill_between(
        x=[int(iter_err) for iter_err in list_of_iterations],  # x
        y1=[(dict_of_consistency_evolution_MEAN[iter_errinf] - dict_of_consistency_evolution_SEM[iter_errinf]) for iter_errinf in list_of_iterations],  # y1
        y2=[(dict_of_consistency_evolution_MEAN[iter_errsup] + dict_of_consistency_evolution_SEM[iter_errsup]) for iter_errsup in list_of_iterations],  # y2
        color=plot_color,
        alpha=0.2,
    )

    # Plot groundtruth consistency.
    axis_plot.plot(
        [int(iter_plot) for iter_plot in list_of_iterations],  # x
        [groundtruth_consistency_score for iter_mean_plot in list_of_iterations],  # y
        label="Score de cohérence de la vérité terrain.",
        marker="",
        markerfacecolor="black",
        markersize=5,
        color="black",
        linewidth=2,
        linestyle="-",
    )

    # Set axis name.
    axis_plot.set_xlabel("itération [#]", fontsize=18,)
    axis_plot.set_ylabel("cohérence [%]", fontsize=18,)

    # Plot the legend.
    axis_plot.legend(fontsize=15, loc="lower right")

    # Plot the grid.
    axis_plot.grid(True)
    
    # Store the graph.
    if graph_filename is not None:
        fig_plot.savefig(
            "../results/" + graph_filename,
            dpi=300,
            transparent=True,
            bbox_inches="tight",
        )

    return fig_plot