# -*- coding: utf-8 -*-

"""
* Name:         clustering_similarity
* Description:  Compute clustering similarity.
* Author:       Erwan Schild
* Created:      10/03/2023
* Licence:      CeCILL (https://cecill.info/licences.fr.html)
"""

# ==============================================================================
# IMPORT PYTHON DEPENDENCIES
# ==============================================================================

from typing import List, Dict, Optional, Tuple
import json
import pandas as pd
from sklearn import metrics
import numpy as np
from scipy import stats as scipystats
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

# ==============================================================================
# 1. COMPUTE CLUSTERING SIMILARITY MOVING AVERAGE
# ==============================================================================
def compute_clustering_similarity(
    dict_of_clustering_results: Dict[str, Dict[str, int]],
    short_average: int = 2,
    long_average: int = 4,
) -> Dict[str, Dict[str, float]]:
    """
    Compute v-measure between two clustering, then moving average with MACD (_moving average convegrence divergence_) method to predict when clustering converge.
    NB : 
    
    Args:
        dict_of_clustering_results (Dict[str, int]): The clustering results during iterations.
        short_average (int): The span for short average of v-measure. Defaults to `2`.
        long_average (int): The span for long average of v-measure. Defaults to `4`.
        
    Returns:
        Dict[str, Dict[str, float]]: The v-measures between clustering and the moving averages.
    """
    
    # Compute a v-measure between two clustering.
    vmeasures_evolution: Dict[str, float] = {}
    previous_iteration: Optional[str] = None
    for iteration in dict_of_clustering_results.keys():
        # Compute a v-measure between two clustering. It starts at iteration "0001".
        if iteration != "0000":
            vmeasures_evolution[iteration] = metrics.v_measure_score(
                labels_true=[str(dict_of_clustering_results[previous_iteration][text_id]) for text_id in dict_of_clustering_results[previous_iteration].keys()],
                labels_pred=[str(dict_of_clustering_results[iteration][text_id]) for text_id in dict_of_clustering_results[iteration].keys()],
            )
        # Update temporary variables.
        previous_iteration = iteration
        
    # Compute moving averages.
    df_averages = pd.DataFrame.from_dict({
        "iteration": list(vmeasures_evolution.keys()),
        "vmeasure": list(vmeasures_evolution.values())
    })
    df_averages.set_index("iteration", inplace=True)
    df_averages["short_average"] = pd.Series.ewm(df_averages["vmeasure"], span=short_average).mean()
    df_averages["long_average"] = pd.Series.ewm(df_averages["vmeasure"], span=long_average).mean()
    df_averages["MACD"] = df_averages["short_average"] - df_averages["long_average"]
    
    # Return results.
    return {
        "similarity": vmeasures_evolution,
        "short_average": df_averages["short_average"].to_dict(),
        "long_average": df_averages["long_average"].to_dict(),
        "MACD": df_averages["MACD"].to_dict(),
    }
    
# ==============================================================================
# 2. DISPLAY CLUSTERING SIMILARITY MOVING AVERAGE
# ==============================================================================
def display_clustering_similarity(
    implementation: str,
    list_of_experiments: List[str],
    list_of_iterations: Optional[List[str]] = None,
    plot_label: str = "Similarité entre deux itérations de clustering.",
    plot_color: str = "black",
    graph_filename: str = "clustering_similarity.png",
) -> Figure:
    """
    Display clustering similarity per iteration.
    
    Args:
        implementation (str): The folder that represents the folder to display.
        list_of_experiments (List[str]). The list of files that represent experiments to analyze.
        list_of_iterations (Optional[List[str]]): The list of iterations used for display. Defaults to `None`.
        plot_label (str): The label of the plot. Defaults to `"Similarité entre deux itérations de clustering."`.
        plot_color (str): The color of plot. Defaults to `"black"`.
        graph_filename (str): The graph filename. Default to `"clustering_similarity.png"`.
        
    Returns:
        Figure: Figure of clustering similarity evolution.
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
    dict_of_clustering_similarity_evolution: Dict[str, List[float]] = {
        iter_2i: [] for iter_2i in list_of_iterations
    }

    # For each experiment...
    for exp2 in list_of_experiments:

        # Load data for the experiment.
        with open("../experiments/" + implementation + "/clustering_similarity___" + exp2, "r") as file_scores_r:
            clustering_similarity: Dict[str, Dict[str, float]] = json.load(file_scores_r)
        
        # For each requested iteration...
        for iter_2 in list_of_iterations:

            # Append the clustering similarity for the current experiment and for this iteration.
            if iter_2 in clustering_similarity["similarity"].keys():
                dict_of_clustering_similarity_evolution[iter_2].append(
                    clustering_similarity["similarity"][iter_2]
                )
            # If iteration isn't reached by this experiment, add 1.0.
            else:
                dict_of_clustering_similarity_evolution[iter_2].append(1.0)
                

    # Initialize storage of experiment clustering similarity mean for all iterations.
    dict_of_clustering_similarity_evolution_MEAN: Dict[str, float] = {
        iter_2m: np.mean(dict_of_clustering_similarity_evolution[iter_2m])
        for iter_2m in list_of_iterations
    }
    # Initialize storage of experiment clustering similarity standard error of the mean for all iterations.
    dict_of_clustering_similarity_evolution_SEM: Dict[str, float] = {
        iter_2s: scipystats.sem(dict_of_clustering_similarity_evolution[iter_2s])
        for iter_2s in list_of_iterations
    }
        

    # Initialize storage of experiment performances for all iterations.
    dict_of_performances_evolution_per_iteration: Dict[str, List[float]] = {
        iter_3i: []
        for iter_3i in list_of_iterations
    }
    
    # For each experiments.
    for exp3 in list_of_experiments:
        
        # Load data.
        with open("../experiments/" + implementation + "/previous_results___" + exp3, "r") as file_experiment_data_r:
            experiment_data: Dict[str, Any] = json.load(file_experiment_data_r)
        dict_of_clustering_performances: Dict[str, Dict[str, float]] = experiment_data["dict_of_clustering_performances"]

        # For each requested iteration...
        for iter_3 in list_of_iterations:

            # Append the clustering performancre for the current experiment and for this iteration.
            if iter_3 in dict_of_clustering_performances.keys():
                dict_of_performances_evolution_per_iteration[iter_3].append(
                    dict_of_clustering_performances[iter_3]["v_measure"]
                )
            # If iteration isn't reached by this experiment, duplicate the last known results.
            # Most of the time: the experiment has reached annotation completeness and there is no more iteration because clustering is "perfect" (v-measure==1.0).
            else:
                dict_of_performances_evolution_per_iteration[iter_3].append(1.0)
                
    # Compute mean of performance evolution.
    dict_of_performances_evolution_per_iteration_MEAN: Dict[str, Dict[str, float]] = {
        iter_3m: np.mean(dict_of_performances_evolution_per_iteration[iter_3m])
        for iter_3m in dict_of_performances_evolution_per_iteration.keys()
    }
        
    # Compute sem of performance evolution.
    dict_of_performances_evolution_per_iteration_SEM: Dict[str, Dict[str, float]] = {
        iter_3s: scipystats.sem(dict_of_performances_evolution_per_iteration[iter_3s])
        for iter_3s in dict_of_performances_evolution_per_iteration.keys()
    }
    
    # Create a new figure.
    fig_plot: Figure = plt.figure(figsize=(15, 7.5), dpi=300)
    axis_plot = fig_plot.gca()

    # Set range of axis.
    axis_plot.set_xlim(xmin=-0.5, xmax=int(max(list_of_iterations))+1.5)
    axis_plot.set_ylim(ymin=-0.01, ymax=1.01)

    # Plot average clustering similarity evolution.
    axis_plot.plot(
        [int(iter_mean) for iter_mean in list_of_iterations],  # x
        [dict_of_clustering_similarity_evolution_MEAN[iter_mean] for iter_mean in list_of_iterations],  # y
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
        y1=[(dict_of_clustering_similarity_evolution_MEAN[iter_errinf] - dict_of_clustering_similarity_evolution_SEM[iter_errinf]) for iter_errinf in list_of_iterations],  # y1
        y2=[(dict_of_clustering_similarity_evolution_MEAN[iter_errsup] + dict_of_clustering_similarity_evolution_SEM[iter_errsup]) for iter_errsup in list_of_iterations],  # y2
        color=plot_color,
        alpha=0.2,
    )

    # Plot average performance of clustering.
    axis_plot.plot(
        [int(iter_mean) for iter_mean in list_of_iterations],  # x
        [dict_of_performances_evolution_per_iteration_MEAN[iter_mean] for iter_mean in list_of_iterations],  # y
        label="Similarité moyenne entre le clustering et la vérité terrain",
        marker="",
        markerfacecolor="black",
        markersize=5,
        color="black",
        linewidth=2,
        linestyle="-",
    )
    axis_plot.fill_between(
        x=[int(iter_err) for iter_err in list_of_iterations],  # x
        y1=[(dict_of_performances_evolution_per_iteration_MEAN[iter_errinf] - dict_of_performances_evolution_per_iteration_SEM[iter_errinf]) for iter_errinf in list_of_iterations],  # y1
        y2=[(dict_of_performances_evolution_per_iteration_MEAN[iter_errsup] + dict_of_performances_evolution_per_iteration_SEM[iter_errsup]) for iter_errsup in list_of_iterations],  # y2
        color="black",
        alpha=0.2,
    )

    # Set axis name.
    axis_plot.set_xlabel("itération [#]", fontsize=18,)
    axis_plot.set_ylabel("v-measure [%]", fontsize=18,)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)

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