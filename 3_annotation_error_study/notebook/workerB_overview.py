# -*- coding: utf-8 -*-

"""
* Name:         workerB_overview
* Description:  Worker to make overviews of interactive clustering annotation errors study experiments.
* Author:       Erwan Schild
* Created:      24/05/2021
* Licence:      CeCILL (https://cecill.info/licences.fr.html)
"""

# ==============================================================================
# IMPORT PYTHON DEPENDENCIES
# ==============================================================================

import json
import matplotlib
import numpy

from typing import Dict, List, Optional, Tuple, Union
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from scipy import stats as scipystats


# ==============================================================================
# WORKER - EXPERIMENT PERFORMANCE OVERVIEW
# ==============================================================================
def experiments_performance_overview(
    list_of_experiments: List[str],
    filename: str = "plot_performances_evolution.png",
    title: str = "Average v-measure according to a set of annotated constraints\nacross multiple simulations of annotation error",
    
) -> int:
    """
    A method aimed at compute and plot average clustering performance evolution over iteration for several overviews, where an overview is a set of experiments.

    Args:
        list_of_experiments (List[str]): The list of experiments used to plot performance overviews.
        filename (str): The filename of the figure to store.
        title (str): The title of the figure.

    Returns:
        int: Return `0` when finish.
    """

    ### ### ### ### ###
    ### Compute evolution of clustering performance average over experiments.
    ### ### ### ### ###

    # Initialize storage of clustering performances evolution.
    dict_of_performances: Dict[int, Dict[float, Dict[str, List[float]]]] = {}

    ###
    ### List of performances.
    ###

    # For each experiment environment...
    for env_path in list_of_experiments:

        # Load configuration for constraints selection.
        with open(
            env_path + "../config.json", "r"
        ) as file_config_constraints_selection:
            CONFIG_CONSTRAINTS_SELECTION = json.load(file_config_constraints_selection)
        nb_constraints: int = CONFIG_CONSTRAINTS_SELECTION["nb_constraints"]
        
        # Load configuration for errors simulation.
        with open(
            env_path + "config.json", "r"
        ) as file_config_errors_simulation:
            CONFIG_ERRORS_SIMULATION = json.load(file_config_errors_simulation)
        errors_rate: float = CONFIG_ERRORS_SIMULATION["error_rate"]
        
        # Load clustering performances.
        with open(
            env_path + "dict_of_clustering_performances.json", "r"
        ) as file_clustering_perf:
            dict_of_clustering_performances = json.load(file_clustering_perf)
            
        # Add global performance.
        if nb_constraints not in dict_of_performances.keys():
            dict_of_performances[nb_constraints] = {}
        if errors_rate not in dict_of_performances[nb_constraints].keys():
            dict_of_performances[nb_constraints][errors_rate] = {
                "v_measure": [],
                "homogeneity": [],
                "completeness": [],
            }
        dict_of_performances[nb_constraints][errors_rate]["v_measure"].append(dict_of_clustering_performances["v_measure"])
        dict_of_performances[nb_constraints][errors_rate]["homogeneity"].append(dict_of_clustering_performances["homogeneity"])
        dict_of_performances[nb_constraints][errors_rate]["completeness"].append(dict_of_clustering_performances["completeness"])

    ###
    ### Mean of performances.
    ###
    
    # Initialize storage of mean evolution of clustering performance.
    dict_of_performances_MEAN: Dict[int, Dict[float, Dict[str, float]]] = {
        nb_constraints_m: {
            errors_rate_m: {
                "v_measure": numpy.mean(dict_of_performances[nb_constraints_m][errors_rate_m]["v_measure"]),
                "homogeneity": numpy.mean(dict_of_performances[nb_constraints_m][errors_rate_m]["homogeneity"]),
                "completeness": numpy.mean(dict_of_performances[nb_constraints_m][errors_rate_m]["completeness"]),
            }
            for errors_rate_m in dict_of_performances[nb_constraints_m].keys()
        }
        for nb_constraints_m in dict_of_performances.keys()
    }

    ###
    ### Standard error of the mean of performances.
    ###

    # Initialize storage of standard error of the mean evolution of clustering performance.
    dict_of_performances_SEM: Dict[int, Dict[float, Dict[str, float]]] = {
        nb_constraints_s: {
            errors_rate_s: {
                "v_measure": scipystats.sem(dict_of_performances[nb_constraints_s][errors_rate_s]["v_measure"]),
                "homogeneity": scipystats.sem(dict_of_performances[nb_constraints_s][errors_rate_s]["homogeneity"]),
                "completeness": scipystats.sem(dict_of_performances[nb_constraints_s][errors_rate_s]["completeness"]),
            }
            for errors_rate_s in dict_of_performances[nb_constraints_s].keys()
        }
        for nb_constraints_s in dict_of_performances.keys()
    }

    ### ### ### ### ###
    ### Plot graph of performance.
    ### ### ### ### ###

    # Create a new figure.
    fig: Figure = plt.figure(figsize=(15, 7.5), dpi=300)
    axis = fig.gca()

    # Define list of iterations to plot.
    list_of_constraints_number: List[int] = sorted(dict_of_performances.keys())
    list_of_errors_rate: List[float] = sorted(dict_of_performances[list_of_constraints_number[0]].keys())
    min_errors_rate: float = min(list_of_errors_rate)
    max_errors_rate: float = max(list_of_errors_rate)
        
    # Color map.
    list_of_colors = matplotlib.colormaps["RdYlGn"](
        numpy.linspace(1, 0, len(list_of_errors_rate))
    )

    # Set range of axis.
    axis.set_ylim(ymin=0, ymax=1)
    
    for k, errors_rate_k in enumerate(list_of_errors_rate):
        
        # Define configs.
        plot_marker: str = "."
        plot_markerfacecolor = list_of_colors[k]
        plot_markersize: float = 3
        plot_color = list_of_colors[k]
        plot_linewidth: float = 0.5
        plot_linestyle: str = ":"
        if errors_rate_k==min_errors_rate:
            plot_marker = "^"
            plot_markersize = 5
            plot_linewidth = 1
            plot_linestyle = "-"
        elif errors_rate_k==max_errors_rate:
            plot_marker = "v"
            plot_markersize = 5
            plot_linewidth = 1
            plot_linestyle = "-"

        # Plot average clustering performance evolution.
        axis.plot(
            list_of_constraints_number,  # x
            [
                dict_of_performances_MEAN[nb_constraints_y][errors_rate_k]["v_measure"]
                for nb_constraints_y in list_of_constraints_number
            ],  # y
            label="{rate:2d}% of errors".format(rate=int(errors_rate_k*100)),
            marker=plot_marker,
            markerfacecolor=plot_markerfacecolor,
            markersize=plot_markersize,
            color=plot_color,
            linewidth=plot_linewidth,
            linestyle=plot_linestyle,
        )
        
        # Plot curve name.
        axis.text(
            x=list_of_constraints_number[-1],
            y=dict_of_performances_MEAN[
                list_of_constraints_number[-1]
            ][errors_rate_k]["v_measure"],
            s="{rate:2d}%".format(rate=int(errors_rate_k*100)),
        )

        # Plot error bars for clustering performance evolution.
        axis.fill_between(
            x=list_of_constraints_number,  # x
            y1=[
                dict_of_performances_MEAN[nb_constraints_y1][errors_rate_k]["v_measure"]
                - dict_of_performances_SEM[nb_constraints_y1][errors_rate_k]["v_measure"]
                for nb_constraints_y1 in list_of_constraints_number
            ],  # y1
            y2=[
                dict_of_performances_MEAN[nb_constraints_y2][errors_rate_k]["v_measure"]
                + dict_of_performances_SEM[nb_constraints_y2][errors_rate_k]["v_measure"]
                for nb_constraints_y2 in list_of_constraints_number
            ],  # y2
            # label="Standard error of the mean",
            color=plot_color,
            alpha=0.2,
        )

    # Set axis name.
    axis.set_xlabel(
        "constraints (#)",
        fontsize=18,
    )
    axis.set_ylabel(
        "v-measure (%)",
        fontsize=18,
    )

    # Plot the title.
    axis.set_title(
        title,
        fontsize=20,
    )

    # Plot the legend.
    axis.legend(
        bbox_to_anchor=(0.50, -0.10),
        title="Percentage of errors during simulation",
        loc="upper center",
        ncol=3,
        title_fontsize=12,
        fontsize=15,
    )

    # Plot the grid.
    axis.grid(True)

    # Store the graph.
    fig.savefig(
        "../results/" + filename,
        dpi=300,
        transparent=True,
        bbox_inches="tight",
    )

    # Close figure.
    plt.close()

    # End of script.
    return 0
