# -*- coding: utf-8 -*-

"""
* Name:         annotation_agreement_score
* Description:  Compute annotation agreement score between annotator and previous clustering.
* Author:       Erwan Schild
* Created:      10/03/2023
* Licence:      CeCILL (https://cecill.info/licences.fr.html)
"""

# ==============================================================================
# IMPORT PYTHON DEPENDENCIES
# ==============================================================================

from typing import List, Dict, Optional, Tuple
import json
import numpy as np
from scipy import stats as scipystats
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

# ==============================================================================
# 1. COMPUTE ANNOTATION AGREEMENT SCORE
# ==============================================================================
def compute_annotation_agreement_score(
    clustering: Dict[str, int],
    annotations: List[Tuple[str, str, str]],
) -> Optional[float]:
    """
    Count the proportion of annotations that is similar to previous clustering results ("MUST_LINK" when same cluster, "CANNOT_LINK" when different clusters).
    NB : if agreement is low (near to 0.0), then constraints annotated will considerably fix clustering in next iteration. Otherwise, clustering is stable.
    
    Args:
        clustering (Dict[str, int]): The clustering result on the previous iteration.
        annotations (List[Tuple[str, str, str]): The constraints annotations on the current iteration.
        
    Returns:
        Optional[float]: The agreement score between annotations and previous clustering. Can be `None` if there is no annotations.
    """
    ok: int = 0
    ko: int = 0
    skip: int = 0
    for annotation in annotations:
        # Get annotation and cluster result.
        cluster_data_1: int = clustering[annotation[0]]
        cluster_data_2: int = clustering[annotation[1]]
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

# ==============================================================================
# 2. DISPLAY ANNOTATION AGREEMENT SCORE EVOLUTION
# ==============================================================================
def display_annotation_agreement_score(
    implementation: str,
    list_of_experiments: List[str],
    list_of_iterations: Optional[List[str]] = None,
    plot_label: str = "Accord annotation/clustering.",
    plot_color: str = "black",
    graph_filename: str = "annotation_agreement_score.png",
) -> Figure:
    """
    Display annotation agreement score per iteration.
    
    Args:
        implementation (str): The folder that represents the folder to display.
        list_of_experiments (List[str]). The list of files that represent experiments to analyze.
        list_of_iterations (Optional[List[str]]): The list of iterations used for display. Defaults to `None`.
        plot_label (str): The label of the plot. Defaults to `"Accord annotation/clustering."`.
        plot_color (str): The color of plot. Defaults to `"black"`.
        graph_filename (str): The graph filename. Default to `"annotation_agreement_score.png"`.
        
    Returns:
        Figure: Figure of annotation agreement score evolution.
    """
    
    # Definition of list_of_iteration:
    if list_of_iterations is None:
        
        # Initialize maximum iteration.
        max_iteration: str = "0001"
    
        # For each experiment...
        for exp1 in list_of_experiments:

            # Load data for the experiment.
            with open("../experiments/" + implementation + "/previous_results___" + exp1, "r") as file_data_r:
                dict_of_clustering_results: Dict[str, Dict[str, int]] = json.load(file_data_r)["dict_of_clustering_results"]

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
            
    # Update iteration by removing "0000".
    list_of_iterations = [
        i
        for i in list_of_iterations
        if i != "0000"
    ]

    # Initialize storage of experiment annotation agreement score for all iterations.
    dict_of_annotation_agreement_score_evolution: Dict[str, List[float]] = {
        iter_cons: [] for iter_cons in list_of_iterations
    }

    # For each experiment...
    for exp2 in list_of_experiments:

        # Load data for the experiment.
        with open("../experiments/" + implementation + "/annotation_agreement_score___" + exp2, "r") as file_scores_r:
            annotation_agreement_scores: Dict[str, float] = json.load(file_scores_r)
        
        # For each requested iteration...
        for iter_a in list_of_iterations:

            # Append the annotation agreement score for the current experiment and for this iteration.
            if iter_a in annotation_agreement_scores.keys():
                dict_of_annotation_agreement_score_evolution[iter_a].append(
                    annotation_agreement_scores[iter_a]
                )
            # If iteration isn't reached by this experiment, add 1.0.
            else:
                dict_of_annotation_agreement_score_evolution[iter_a].append(1.0)
                

    # Initialize storage of experiment annotation agreement score mean for all iterations.
    dict_of_annotation_agreement_score_evolution_MEAN: Dict[str, float] = {
        iter_mean: np.mean(dict_of_annotation_agreement_score_evolution[iter_mean])
        for iter_mean in list_of_iterations
    }
    # Initialize storage of experiment annotation agreement score standard error of the mean for all iterations.
    dict_of_annotation_agreement_score_evolution_SEM: Dict[str, float] = {
        iter_sem: scipystats.sem(dict_of_annotation_agreement_score_evolution[iter_sem])
        for iter_sem in list_of_iterations
    }
    
    # Create a new figure.
    fig_plot: Figure = plt.figure(figsize=(15, 7.5), dpi=300)
    axis_plot = fig_plot.gca()

    # Set range of axis.
    axis_plot.set_xlim(xmin=-0.5, xmax=int(max(list_of_iterations))+1.5)
    axis_plot.set_ylim(ymin=-0.01, ymax=1.01)

    # Plot average annotation agreement score evolution.
    axis_plot.plot(
        [int(iter_mean) for iter_mean in list_of_iterations],  # x
        [dict_of_annotation_agreement_score_evolution_MEAN[iter_mean] for iter_mean in list_of_iterations],  # y
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
        y1=[(dict_of_annotation_agreement_score_evolution_MEAN[iter_errinf] - dict_of_annotation_agreement_score_evolution_SEM[iter_errinf]) for iter_errinf in list_of_iterations],  # y1
        y2=[(dict_of_annotation_agreement_score_evolution_MEAN[iter_errsup] + dict_of_annotation_agreement_score_evolution_SEM[iter_errsup]) for iter_errsup in list_of_iterations],  # y2
        color=plot_color,
        alpha=0.2,
    )

    # Set axis name.
    axis_plot.set_xlabel("itération [#]", fontsize=18,)
    axis_plot.set_ylabel("accord annotation/clustering [%]", fontsize=18,)

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