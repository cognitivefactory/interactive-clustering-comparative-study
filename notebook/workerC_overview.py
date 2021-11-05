# -*- coding: utf-8 -*-

"""
* Name:         workerC_overview
* Description:  Worker to make overviews of interactive clustering comparative study experiments.
* Author:       Erwan Schild
* Created:      24/05/2021
* Licence:      CeCILL (https://cecill.info/licences.fr.html)
"""

# ==============================================================================
# IMPORT PYTHON DEPENDENCIES
# ==============================================================================

import json  # Serialization.
from typing import Dict, List, Optional, Tuple, Union  # Python code typing (mypy).

import numpy  # Statistics computation.
from matplotlib import pyplot as plt  # Graph management.
from matplotlib.figure import Figure
from scipy import stats as scipystats  # Statistics computation.


# ==============================================================================
# WORKER - EXPERIMENT PERFORMANCE OVERVIEW
# ==============================================================================
def experiments_performance_overview(
    overview_settings: Dict[str, Dict[str, Union[str, List[str]]]],
    forced_max_iter: Optional[str] = None,
) -> int:
    """
    A method aimed at compute and plot average clustering performance evolution over iteration for several overviews, where an overview is a set of experiments.

    Args:
        overview_settings (Dict[str, Dict[str, Union[str, List[str]]]]): A dictionary that represents overviews. It contains the plot settings (color, title, ...) and the list of environments for all defined overview.
        forced_max_iter (Optional[str]): The maximum iteration to limit plot range. Defaults to `None`.

    Returns:
        int: Return `0` when finish.
    """

    ### ### ### ### ###
    ### Define the maximum iteration.
    ### ### ### ### ###

    # Initialize evaluation storage.
    MAX_ITER: str = "0000"

    # For each requested overview...
    for _, settings_1 in overview_settings.items():

        # For each experiment in this overview...
        for env_1 in list(settings_1["LIST_OF_ENV_PATHS"]):

            # Load annotations for the current experiment.
            with open(
                env_1 + "dict_of_constraints_annotations.json", "r"
            ) as annotation_file:
                dict_of_constraints_annotations: Dict[
                    str, List[Tuple[str, str, Optional[str]]]
                ] = json.load(annotation_file)

            # Update current maximum iteration.
            current_max_iteration: str = max(dict_of_constraints_annotations.keys())
            if MAX_ITER < current_max_iteration:
                MAX_ITER = current_max_iteration

    # If set, force maximum iteration.
    if forced_max_iter is not None:
        MAX_ITER = min(MAX_ITER, forced_max_iter)

    # Define list of iteration for computations.
    LIST_OF_ITERATIONS: List[str] = [str(i).zfill(4) for i in range(int(MAX_ITER))]

    ### ### ### ### ###
    ### Compute evolution of clustering performance average over experiments.
    ### ### ### ### ###

    # Initialize storage of experiment performances for all iterations of all requested overviews.
    dict_of_global_performances_evolution: Dict[str, Dict[str, List[float]]] = {
        overview_perf: {iter_perf: [] for iter_perf in LIST_OF_ITERATIONS}
        for overview_perf in overview_settings.keys()
    }
    # Initialize storage of performance mean for all iterations of all requested overviews.
    dict_of_global_performances_evolution_MEAN: Dict[str, Dict[str, float]] = {
        overview_mean: {iter_mean: 0 for iter_mean in LIST_OF_ITERATIONS}
        for overview_mean in overview_settings.keys()
    }
    # Initialize storage of performance standard error of the mean for all iterations of all requested overviews.
    dict_of_global_performances_evolution_SEM: Dict[str, Dict[str, float]] = {
        overview_pstdev: {iter_pstdev: 0 for iter_pstdev in LIST_OF_ITERATIONS}
        for overview_pstdev in overview_settings.keys()
    }

    # For each requested overview...
    for overview_2, settings_2 in overview_settings.items():

        # Print overview.
        print(overview_2)

        # For each experiment in this overview...
        for env_2 in list(settings_2["LIST_OF_ENV_PATHS"]):

            # Load clustering evaluations.
            with open(
                env_2 + "dict_of_clustering_performances.json", "r"
            ) as evaluation_file:
                dict_of_clustering_performances: Dict[
                    str, Dict[str, float]
                ] = json.load(evaluation_file)

            # For each requested iteration...
            for iter_2 in LIST_OF_ITERATIONS:

                # Append the clustering performancre for the current experiment and for this iteration.
                if iter_2 in dict_of_clustering_performances.keys():
                    dict_of_global_performances_evolution[overview_2][iter_2].append(
                        dict_of_clustering_performances[iter_2]["v_measure"]
                    )
                # If iteration isn't reached by this experiment, duplicate the last known results.
                # Most of the time: the experiment has reached annotation completeness and there is no more iteration because clustering is "perfect" (v-measure==1.0).
                else:
                    last_iter: str = max(dict_of_clustering_performances.keys())
                    dict_of_global_performances_evolution[overview_2][iter_2].append(
                        dict_of_clustering_performances[last_iter]["v_measure"]
                    )

        # Compute mean and sem of performance for this iteration and for experiment in this overview.
        for iter_3 in LIST_OF_ITERATIONS:

            # Compute mean of performance for this iteration and for experiment in this overview.
            dict_of_global_performances_evolution_MEAN[overview_2][iter_3] = numpy.mean(
                dict_of_global_performances_evolution[overview_2][iter_3]
            )

            # Compute sem of performance for this iteration and for experiment in this overview.
            dict_of_global_performances_evolution_SEM[overview_2][
                iter_3
            ] = scipystats.sem(
                dict_of_global_performances_evolution[overview_2][iter_3]
            )

    ### ### ### ### ###
    ### Plot graph of performance.
    ### ### ### ### ###

    # Create a new figure.
    fig: Figure = plt.figure(figsize=(15, 7.5), dpi=300)
    axis = fig.gca()

    # Define list of iterations to plot.
    list_of_iterations_to_plot: List[int] = [
        int(iter_plot) for iter_plot in LIST_OF_ITERATIONS
    ]

    # For all experiments overview...
    for overview_3, settings_3 in overview_settings.items():

        # Plot average clustering performance evolution.
        axis.plot(
            list_of_iterations_to_plot,  # x
            [
                dict_of_global_performances_evolution_MEAN[overview_3][iter_mean_plot]
                for iter_mean_plot in LIST_OF_ITERATIONS
            ],  # y
            label=str(settings_3["title"]),
            marker=str(settings_3["marker"]),
            markerfacecolor=str(settings_3["color"]),
            markersize=5,
            color=settings_3["color"],
            linewidth=1,
            linestyle=str(settings_3["linestyle"]),
        )

        # Plot error bars for clustering performance evolution.
        axis.fill_between(
            x=list_of_iterations_to_plot,
            y1=[
                dict_of_global_performances_evolution_MEAN[overview_3][iter_errinf_plot]
                - dict_of_global_performances_evolution_SEM[overview_3][
                    iter_errinf_plot
                ]
                for iter_errinf_plot in LIST_OF_ITERATIONS
            ],  # y1
            y2=[
                dict_of_global_performances_evolution_MEAN[overview_3][iter_errsup_plot]
                + dict_of_global_performances_evolution_SEM[overview_3][
                    iter_errsup_plot
                ]
                for iter_errsup_plot in LIST_OF_ITERATIONS
            ],  # y2
            # label="Standard error of the mean",
            color=str(settings_3["color"]),
            alpha=0.2,
        )

    # Set axis name.
    axis.set_xlabel(
        "iteration (#)",
        fontsize=18,
    )
    axis.set_ylabel(
        "v-measure (%)",
        fontsize=18,
    )

    # Plot the title.
    axis.set_title(
        "Average paths observed for optimal convergence of v-measure to a given objective",
        fontsize=20,
    )

    # Plot the legend.
    axis.legend(
        # bbox_to_anchor=(0.50, -0.10),
        # title="Type of settings used for computations",
        # loc="upper center",
        # ncol=2,
        # title_fontsize=12,
        fontsize=15,
    )

    # Plot the grid.
    axis.grid(True)

    # Store the graph.
    fig.savefig(
        "../experiments/plot_global_performances_evolution.png",
        dpi=300,
        transparent=True,
        bbox_inches="tight",
    )

    # Close figure.
    plt.close()

    # End of script.
    return 0


# ==============================================================================
# WORKER - EXPERIMENT TIME OVERVIEW
# ==============================================================================
def experiments_time_overview(
    overview_settings: Dict[str, Dict[str, Union[str, List[str]]]],
    forced_max_iter: Optional[str] = None,
) -> int:
    """
    A method aimed at compute and plot average clustering time evolution over iteration for several overviews, where an overview is a set of experiments.

    Args:
        overview_settings (Dict[str, Dict[str, Union[str, List[str]]]]): A dictionary that represents overviews. It contains the plot settings (color, title, ...) and the list of environments for all defined overview.
        forced_max_iter (Optional[str]): The maximum iteration to limit plot range. Defaults to `None`.

    Returns:
        int: Return `0` when finish.
    """

    ### ### ### ### ###
    ### Define the maximum iteration.
    ### ### ### ### ###

    # Initialize evaluation storage.
    MAX_ITER: str = "0000"

    # For each requested overview...
    for _, settings_1 in overview_settings.items():

        # For each experiment in this overview...
        for env_1 in list(settings_1["LIST_OF_ENV_PATHS"]):

            # Load annotations for the current experiment.
            with open(
                env_1 + "dict_of_constraints_annotations.json", "r"
            ) as annotation_file:
                dict_of_constraints_annotations: Dict[
                    str, List[Tuple[str, str, Optional[str]]]
                ] = json.load(annotation_file)

            # Update current maximum iteration.
            current_max_iteration: str = max(dict_of_constraints_annotations.keys())
            if MAX_ITER < current_max_iteration:
                MAX_ITER = current_max_iteration

    # If set, force maximum iteration.
    if forced_max_iter is not None:
        MAX_ITER = min(MAX_ITER, forced_max_iter)

    # Define list of iteration for computations.
    LIST_OF_ITERATIONS: List[str] = [str(i).zfill(4) for i in range(int(MAX_ITER))]

    ### ### ### ### ###
    ### Compute evolution of clustering performance average over experiments.
    ### ### ### ### ###

    # Initialize storage of experiment times for all iterations of all requested overviews.
    dict_of_global_computation_times_evolution: Dict[str, Dict[str, List[float]]] = {
        overview_perf: {iter_perf: [] for iter_perf in LIST_OF_ITERATIONS}
        for overview_perf in overview_settings.keys()
    }
    # Initialize storage of time mean for all iterations of all requested overviews.
    dict_of_global_computation_times_evolution_MEAN: Dict[str, Dict[str, float]] = {
        overview_mean: {iter_mean: 0 for iter_mean in LIST_OF_ITERATIONS}
        for overview_mean in overview_settings.keys()
    }
    # Initialize storage of time standard error of the mean for all iterations of all requested overviews.
    dict_of_global_computation_times_evolution_SEM: Dict[str, Dict[str, float]] = {
        overview_pstdev: {iter_pstdev: 0 for iter_pstdev in LIST_OF_ITERATIONS}
        for overview_pstdev in overview_settings.keys()
    }

    # For each requested overview...
    for overview_2, settings_2 in overview_settings.items():

        # Print overview.
        print(overview_2)

        # For each experiment in this overview...
        for env_2 in list(settings_2["LIST_OF_ENV_PATHS"]):

            # Load clustering time.
            with open(env_2 + "dict_of_computation_times.json", "r") as time_file:
                dict_of_computation_times: Dict[str, Dict[str, float]] = json.load(
                    time_file
                )

            # For each requested iteration...
            for iter_2 in LIST_OF_ITERATIONS:

                # Append the clustering time for the current experiment and for this iteration.
                if iter_2 in dict_of_computation_times.keys():
                    dict_of_global_computation_times_evolution[overview_2][
                        iter_2
                    ].append(dict_of_computation_times[iter_2]["clustering_TOTAL_RUN"])
                # If iteration isn't reached by this experiment, duplicate the last known results.
                # Most of the time: the experiment has reached annotation completeness and there is no more iteration because clustering is "perfect" (v-measure==1.0).
                else:
                    last_iter: str = max(dict_of_computation_times.keys())
                    dict_of_global_computation_times_evolution[overview_2][
                        iter_2
                    ].append(
                        dict_of_computation_times[last_iter]["clustering_TOTAL_RUN"]
                    )

        # Compute mean and sem of performance for this iteration and for experiment in this overview.
        for iter_3 in LIST_OF_ITERATIONS:

            # Compute mean of clustering time for this iteration and for experiment in this overview.
            dict_of_global_computation_times_evolution_MEAN[overview_2][
                iter_3
            ] = numpy.mean(
                dict_of_global_computation_times_evolution[overview_2][iter_3]
            )

            # Compute sem of clustering time for this iteration and for experiment in this overview.
            dict_of_global_computation_times_evolution_SEM[overview_2][
                iter_3
            ] = scipystats.sem(
                dict_of_global_computation_times_evolution[overview_2][iter_3]
            )

    ### ### ### ### ###
    ### Plot graph of time.
    ### ### ### ### ###

    # Create a new figure.
    fig: Figure = plt.figure(figsize=(15, 7.5), dpi=300)
    axis = fig.gca()

    # Define list of iterations to plot.
    list_of_iterations_to_plot: List[int] = [
        int(iter_plot) for iter_plot in LIST_OF_ITERATIONS
    ]

    # For all experiments overview...
    for overview_3, settings_3 in overview_settings.items():

        # Plot average clustering time evolution.
        axis.plot(
            list_of_iterations_to_plot,  # x
            [
                dict_of_global_computation_times_evolution_MEAN[overview_3][
                    iter_mean_plot
                ]
                for iter_mean_plot in LIST_OF_ITERATIONS
            ],  # y
            label=str(settings_3["title"]),
            marker=str(settings_3["marker"]),
            markerfacecolor=str(settings_3["color"]),
            markersize=5,
            color=settings_3["color"],
            linewidth=1,
            linestyle=str(settings_3["linestyle"]),
        )

        # Plot error bars for clustering time evolution.
        axis.fill_between(
            x=list_of_iterations_to_plot,
            y1=[
                dict_of_global_computation_times_evolution_MEAN[overview_3][
                    iter_errinf_plot
                ]
                - dict_of_global_computation_times_evolution_SEM[overview_3][
                    iter_errinf_plot
                ]
                for iter_errinf_plot in LIST_OF_ITERATIONS
            ],  # y1
            y2=[
                dict_of_global_computation_times_evolution_MEAN[overview_3][
                    iter_errsup_plot
                ]
                + dict_of_global_computation_times_evolution_SEM[overview_3][
                    iter_errsup_plot
                ]
                for iter_errsup_plot in LIST_OF_ITERATIONS
            ],  # y2
            # label="Standard error of the mean",
            color=str(settings_3["color"]),
            alpha=0.2,
        )

    # Set axis name.
    axis.set_xlabel(
        "iteration (#)",
        fontsize=18,
    )
    axis.set_ylabel(
        "time (s)",
        fontsize=18,
    )

    # Plot the title.
    axis.set_title(
        "Evolution of computation time needed, depending on clustering algorithm",
        fontsize=20,
    )

    # Plot the legend.
    axis.legend(
        # bbox_to_anchor=(0.50, -0.10),
        # title="Clustering algorithms",
        # loc="upper center",
        # ncol=2,
        # title_fontsize=12,
        fontsize=15,
    )

    # Plot the grid.
    axis.grid(True)

    # Store the graph.
    fig.savefig(
        "../experiments/plot_global_computation_times_evolution.png",
        dpi=300,
        transparent=True,
        bbox_inches="tight",
    )

    # Close figure.
    plt.close()

    # End of script.
    return 0
