# -*- coding: utf-8 -*-

"""
* Name:         clustering_similarity_moving_average
* Description:  Compute clustering similarity moving average with MACD (_moving average convergence divergence_).
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
def compute_clustering_similarity_moving_average(
    dict_of_clustering_results: Dict[str, Dict[str, int]],
    short_average: int = 3,
    long_average: int = 5,
) -> Dict[str, Dict[str, float]]:
    """
    Compute v-measure between two clustering, then moving average with MACD (_moving average convegrence divergence_) method to predict when clustering converge.
    NB : 
    
    Args:
        dict_of_clustering_results (Dict[str, int]): The clustering results during iterations.
        short_average (int): The span for short average of v-measure. Defaults to `3`.
        long_average (int): The span for long average of v-measure. Defaults to `5`.
        
    Returns:
        Dict[str, Dict[str, float]]: The v-measures between clustering and the moving averages.
    """
    
    # Compute av-measure between two clustering.
    vmeasures_evolution: Dict[str, float] = {}
    previous_iteration: Optional[str] = None
    for iteration in dict_of_clustering_results.keys():
        # Compute av-measure between two clustering. It starts at iteration "0001".
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
        "vmeasure": vmeasures_evolution,
        "short_average": df_averages["short_average"].to_dict(),
        "long_average": df_averages["long_average"].to_dict(),
        "MACD": df_averages["MACD"].to_dict(),
    }
    
# ==============================================================================
# 2. DISPLAY CLUSTERING SIMILARITY MOVING AVERAGE
# ==============================================================================
def display_clustering_similarity_moving_average(
    implementation: str,
    list_of_experiments: List[str],
    list_of_iterations: Optional[List[str]] = None,
    plot_label: str = "MACD.",
    plot_color: str = "black",
    graph_filename: str = "MACD.png",
) -> Figure:
    """
    Display clustering similarity moving average per iteration.
    
    Args:
        implementation (str): The folder that represents the folder to display.
        list_of_experiments (List[str]). The list of files that represent experiments to analyze.
        list_of_iterations (Optional[List[str]]): The list of iterations used for display. Defaults to `None`.
        plot_label (str): The label of the plot. Defaults to `"Accord annotation/clustering."`.
        plot_color (str): The color of plot. Defaults to `"black"`.
        graph_filename (str): The graph filename. Default to `"annotation_agreement_score.png"`.
        
    Returns:
        Figure: Figure of clustering similarity movinging average evolution.
    """
    return None
    # Compute mean
    # Display short average
    # Display long average
    # Display average vmeasure with groundtruth
    # Display average vmeasure beatween clustering