# -*- coding: utf-8 -*-

"""
* Name:         workerB_evaluation
* Description:  Worker to evaluate an interactive clustering efficience study experiment.
* Author:       Erwan Schild
* Created:      24/05/2021
* Licence:      CeCILL (https://cecill.info/licences.fr.html)
"""

# ==============================================================================
# IMPORT PYTHON DEPENDENCIES
# ==============================================================================

import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from cognitivefactory.interactive_clustering.constraints.abstract import (
    AbstractConstraintsManager,
)
from cognitivefactory.interactive_clustering.constraints.factory import (
    managing_factory,
)
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from sklearn import metrics


# ==============================================================================
# WORKER - EXPERIMENT EVALUATION
# ==============================================================================
def experiment_evaluate(
    parameters: Dict[str, Any],
):
    """
    A worker to evaluate an interactive clustering efficience study experiment.
    An experiment is aimed at iteratively and automatically annotated an NLP dataset with the interactive clustering methodology.
    The evaluation is aimed at analyze clustering performance at each iteration, and look at several iterations where performance reach specific threshold.
    Then, go to the next step of the efficience study to plot iteration progress (performance evolution, time spent, annotation needed).
    Usage note:
        - The experiment run step of the notebook `2_Run_and_evaluate_experiments.ipynb` has to be done before the evaluation.
        - Parameters have to contain the path experiment to evaluate. A dictionary is needed to get parameters in `multiprocessing.Pool.imap_unordered` call.
        - The path to the environment has to be formatted by the notebook `1_Initialize_convergence_experiments.ipynb`.
        - The notebook `2_Run_until_convergence_and_evaluate_efficience.ipynb` launch this script for all defined experiment environments with the librairy `multiprocessing`.

    Args:
        parameters (Dict[str, Any]): A dictionary that contains several parameters. Two keys are expected in this dictionary: the experiment environment path (`"ENV_PATH"`), the convergence study progress to print (`"study_progress"`). An optional key (`"performance_goals_to_compute"`) can be added to define performance goal for iteration to highlight computation.

    Returns:
        int: Return `0` when finish.
    """

    # Parameters.
    ENV_PATH: str = str(parameters["ENV_PATH"])
    study_progress: str = str(parameters["study_progress"])
    performance_goals_to_compute: List[str] = (
        parameters["performance_goals_to_compute"]
        if ("performance_goals_to_compute" in parameters.keys())
        else ["0.50", "0.60", "0.70", "0.80", "0.90", "0.95", "0.99", "1.00"]
    )

    ### ### ### ### ###
    ### Load needed configurations and data.
    ### ### ### ### ###

    # Load configuration for experiment.
    with open(ENV_PATH + "config.json", "r") as file_config_experiment:
        CONFIG_EXPERIMENT = json.load(file_config_experiment)

    ### ### ### ### ###
    ### Load needed data.
    ### ### ### ### ###

    # Load dict of true intents.
    with open(ENV_PATH + "../../../../../dict_of_true_intents.json", "r") as file_true_intents:
        dict_of_true_intents: Dict[str, str] = json.load(file_true_intents)

    # Get list of data IDs.
    list_of_data_IDs: List[str] = sorted(dict_of_true_intents.keys())

    ### ### ### ### ###
    ### Load storage files.
    ### ### ### ### ###

    # Load dictionary of clustering results.
    with open(ENV_PATH + "dict_of_clustering_results.json", "r") as file_clustering_results:
        dict_of_clustering_results: Dict[str, Dict[str, int]] = json.load(file_clustering_results)

    # Load dictionary of annotation history.
    with open(ENV_PATH + "dict_of_constraints_annotations.json", "r") as file_annotations:
        dict_of_constraints_annotations: Dict[
            str, List[Tuple[str, str, str]]
        ] = json.load(file_annotations)

    # Load dictionary of time spent.
    with open(ENV_PATH + "dict_of_computation_times.json", "r") as file_times:
        dict_of_computation_times: Dict[str, Dict[str, float]] = json.load(file_times)

    # Define list of iterations.
    LIST_OF_ITERATIONS = sorted(dict_of_constraints_annotations.keys())

    ### ### ### ### ###
    ### Start clustering evaluation.
    ### ### ### ### ###

    # Format true intents from dict to list.
    list_of_true_intents: List[str] = [
        dict_of_true_intents[data_ID] for data_ID in list_of_data_IDs
    ]

    # Initialize evaluation storage.
    dict_of_clustering_performances: Dict[str, Dict[str, float]] = {}

    # For all experiment...
    for iteration in LIST_OF_ITERATIONS:

        # Initialize evaluation for the current iteration.
        dict_of_clustering_performances[iteration] = {}

        # Format predicted intents from dict to list.
        list_of_predicted_intents: List[int] = [
            dict_of_clustering_results[iteration][data_ID]
            for data_ID in list_of_data_IDs
        ]

        # Compute homogeneity.
        dict_of_clustering_performances[iteration][
            "homogeneity"
        ] = metrics.homogeneity_score(list_of_true_intents, list_of_predicted_intents)

        # Compute completeness.
        dict_of_clustering_performances[iteration][
            "completeness"
        ] = metrics.completeness_score(list_of_true_intents, list_of_predicted_intents)

        # Compute v_measure.
        dict_of_clustering_performances[iteration][
            "v_measure"
        ] = metrics.v_measure_score(list_of_true_intents, list_of_predicted_intents)

        # Compute adjusted_rand_index.
        dict_of_clustering_performances[iteration][
            "adjusted_rand_index"
        ] = metrics.adjusted_rand_score(list_of_true_intents, list_of_predicted_intents)

        # Compute adjusted_mutual_information.
        dict_of_clustering_performances[iteration][
            "adjusted_mutual_information"
        ] = metrics.adjusted_mutual_info_score(
            list_of_true_intents, list_of_predicted_intents
        )

    # Store dictionary of clustering evaluation.
    with open(ENV_PATH + "dict_of_clustering_performances.json", "w") as file_performances:
        json.dump(dict_of_clustering_performances, file_performances, indent=1)

    ### ### ### ### ###
    ### Find iterations that reach specific performance threshold.
    ### ### ### ### ###

    # Initialize dictionary of iterations to highlight.
    dict_of_iterations_to_highlight: Dict[str, Dict[str, Any]] = {}

    for performance_goal in performance_goals_to_compute:

        # Define performance key.
        performance_key: str = performance_goal + "v"

        # Compute iteration to highlight for this performance goal.
        dict_of_iterations_to_highlight[performance_key] = {
            "iteration": _get_iteration_of_performance_reached(
                evaluations=dict_of_clustering_performances,
                metric="v_measure",
                goal=float(performance_goal),
            ),
            "metric": "v_measure",
            "goal": float(performance_goal),
        }

    # Update dictionary of iterations to highlight with iteration of annotation completeness.
    dict_of_iterations_to_highlight["MAX"] = {
        "iteration": _get_iteration_of_annotation_completness(
            list_of_data_IDs=list_of_data_IDs,
            annotations=dict_of_constraints_annotations,
            manager_type=CONFIG_EXPERIMENT["manager_type"],
        ),
        "metric": "annotation",
        "goal": "MAX",
    }

    # Store dictionary of iteration to highlight.
    with open(ENV_PATH + "dict_of_iterations_to_highlight.json", "w") as file_iteration_highlight:
        json.dump(dict_of_iterations_to_highlight, file_iteration_highlight, indent=1)

    ### ### ### ### ###
    ### Plot clustering performance evolution.
    ### ### ### ### ###

    # Create and store graph of clustering performance evolution.
    _plot_clustering_performance_evolution(
        evaluation_storage=dict_of_clustering_performances,
        iterations_to_highlight=dict_of_iterations_to_highlight,
        graph_folderpath=ENV_PATH,
    )

    ### ### ### ### ###
    ### Plot annotation completeness evolution.
    ### ### ### ### ###

    # Create and store graph of annotation completeness evolution.
    _plot_annotation_completeness_evolution(
        annotation_storage=dict_of_constraints_annotations,
        iterations_to_highlight=dict_of_iterations_to_highlight,
        graph_folderpath=ENV_PATH,
    )

    ### ### ### ### ###
    ### Plot time spent evolution.
    ### ### ### ### ###

    # Create and store graph of time spent evolution.
    _plot_time_spent_evolution(
        time_storage=dict_of_computation_times,
        iterations_to_highlight=dict_of_iterations_to_highlight,
        graph_folderpath=ENV_PATH,
    )

    return 0


# ==============================================================================
# PRIVATE - GET ITERATION OF PERFORMANCE REACHED
# ==============================================================================
def _get_iteration_of_performance_reached(
    evaluations: Dict[str, Dict[str, float]],
    goal: float,
    metric: str = "v_measure",
) -> Optional[str]:
    """
    A method aimed at find the iteration that reach a performance goal for a specific metric.

    Args:
        evaluations (Dict[str, Dict[str, float]]): A dictionary that contains evaluations for each completed iteration.
        goal (float): The performance goal to reach. Must be between `0.00` and `1.00`.
        metric (str, optional): The performance metric to look at. Defaults to `"v_measure"`.

    Raises:
        ValueError: If parameters are badly set.

    Returns:
        Optional[str]: The iteration that reaches the expected performance goal, `None` if the expected performance is not reached or is not maintained.
    """

    # Check that the requested metric is implemented.
    if metric not in {
        "homogeneity",
        "completeness",
        "v_measure",
        "adjusted_rand_index",
        "adjusted_mutual_information",
    }:
        raise ValueError("The `metric` '" + str(metric) + "' is not implemented.")

    # Check that the requested goal is implemented.
    if (not isinstance(goal, float)) or (goal < 0) or (1 < goal):
        raise ValueError("The `goal` '" + str(goal) + "' must be between 0.0 and 1.0.")

    # Get the list of possible iterations.
    list_of_iterations: List[str] = sorted(evaluations.keys())

    # If no iteration : return None
    if list_of_iterations == []:  # noqa: WPS520
        return None

    # Get the last iteration
    current_iteration: str = list_of_iterations.pop()
    previous_iteration: Optional[str] = None

    # Assert the last iteration reach the expected performance
    if evaluations[current_iteration][metric] < goal:
        return None

    # Look at all iteration (descending order).
    while list_of_iterations != []:  # noqa: WPS520

        # Get the previous iteration
        previous_iteration = list_of_iterations.pop()

        # If the previous iteration doesn't reched the expected performance...
        if evaluations[previous_iteration][metric] < goal:
            # ... then return the current iteration as the best iteration.
            return current_iteration
        # Otherwise (the previous iteration reach the expected performance)...
        else:
            # ... the expected performance is maintained and we can check the previous iteration.
            current_iteration = previous_iteration

    # If all iteration has been checked and the expected performance is still maintained, return the current iteration (first iteration) as best iteration
    return current_iteration


# ==============================================================================
# PRIVATE - GET ITERATION OF PERFORMANCE REACHED
# ==============================================================================
def _get_iteration_of_annotation_completness(
    list_of_data_IDs: List[str],
    annotations: Dict[str, List[Tuple[str, str, str]]],
    manager_type: str = "binary",
) -> Optional[str]:
    """
    A method aimed at find the iteration that reach the annotation completness.

    Args:
        list_of_data_IDs (List[str]): The list of data IDs to manage.
        annotations (Dict[str, List[Tuple[str, str, str]]]): List of triplet of annotation over iterations.
        manager_type (str, optional): The constraints manager type. Defaults to `"binary"`.

    Raises:
        ValueError: If parameters are badly set.

    Returns:
        Optional[str]: The iteration that reaches the annotation completness, else `None`.
    """

    # Initialize constraints manager.
    constraints_manager: AbstractConstraintsManager = managing_factory(
        list_of_data_IDs=list_of_data_IDs,
        manager=manager_type,
    )

    # For each iteration of annotation...
    for iteration, list_of_triplet_annotated in annotations.items():

        # Update constraints manager.
        for annotation in list_of_triplet_annotated:

            # Add constraint to the constraints manager.
            constraints_manager.add_constraint(
                data_ID1=annotation[0],
                data_ID2=annotation[1],
                constraint_type=annotation[2],
            )

        # Check the annotation completude.
        if constraints_manager.check_completude_of_constraints():
            return iteration

    # If completude is not reach over iteration, return `None`.
    return None


# ==============================================================================
# PRIVATE - PLOT CLUSTERING PERFORMANCE EVOLUTION
# ==============================================================================
def _plot_clustering_performance_evolution(
    evaluation_storage: Dict[str, Dict[str, float]],
    iterations_to_highlight: Dict[str, Dict[str, Any]],
    graph_title: str = "Interactive clustering performance over iterations",
    graph_folderpath: str = "",
    graph_filename: str = "plot_clustering_performances_evolution.png",
) -> int:
    """
    A method aimed at create and store a graph that represents clustering performance evolution over iterations.

    Args:
        evaluation_storage (Dict[str, Dict[str, float]]): The dictionary that store the clustering performances for all iterations.
        iterations_to_highlight (Dict[str, Dict[str, Any]]): The dictionary that contains iteration that reach specif performance goal.
        graph_title (str, optional): The title of the graph to show. Defaults to `"Interactive clustering performance over iteration"`.
        graph_folderpath (str, optional): The foldername of the graph. Defaults to `""`.
        graph_filename (str, optional): The filename of the graph. Defaults to `"plot_clustering_performances_evolution.png"`.

    Returns:
        int: Return `0` when finish.
    """

    # Create a new figure.
    fig: Figure = plt.figure(figsize=(15, 7.5), dpi=300.0)
    axis = fig.gca()

    # Define list of iterations to plot.
    list_of_iteration: List[int] = [
        int(iteration) for iteration in evaluation_storage.keys()
    ]

    # Set range of axis.
    axis.set_ylim(ymin=0, ymax=1)

    # Plot homogeneity evolution.
    axis.plot(
        list_of_iteration,  # x
        [
            evaluation_storage[iteration]["homogeneity"]
            for iteration in evaluation_storage.keys()
        ],  # y
        label="Homogeneity",
        marker="o",
        markerfacecolor="blue",
        markersize=5,
        color="blue",
        linewidth=1,
    )

    # Plot completness evolution.
    axis.plot(
        list_of_iteration,  # x
        [
            evaluation_storage[iteration]["completeness"]
            for iteration in evaluation_storage.keys()
        ],  # y
        label="Completeness",
        marker="o",
        markerfacecolor="red",
        markersize=5,
        color="red",
        linewidth=1,
    )

    # Plot v-measure evolution.
    axis.plot(
        list_of_iteration,  # x
        [
            evaluation_storage[iteration]["v_measure"]
            for iteration in evaluation_storage.keys()
        ],  # y
        label="V-measure",
        marker="o",
        markerfacecolor="green",
        markersize=5,
        color="green",
        linewidth=1,
        linestyle="dashed",
    )

    # Add markers for iteration that reach specific performance goal.
    for specific_iteration in iterations_to_highlight.keys():

        # Get the iteration.
        if iterations_to_highlight[specific_iteration]["iteration"] is not None:

            # Plot a vertical line at the iteration
            axis.axvline(
                x=int(str(iterations_to_highlight[specific_iteration]["iteration"])),
                color="black",
                linestyle="--",
            )

    # Set axis name.
    axis.set_xlabel("iteration (#)")
    axis.set_ylabel("performance (%)")

    # Plot the title.
    axis.set_title(graph_title, fontsize=20)

    # Plot the legend.
    axis.legend(
        bbox_to_anchor=(0.50, -0.10),
        title="Type of displayed performance metrics",
        loc="upper center",
        ncol=4,
        title_fontsize=12,
        fontsize=10,
    )

    # Plot the grid.
    axis.grid(True)

    # Store the graph.
    fig.savefig(
        graph_folderpath + graph_filename,
        dpi=300,
        transparent=True,
        bbox_inches="tight",
    )

    # Close figure.
    plt.close()

    # End of script.
    return 0


# ==============================================================================
# PRIVATE - PLOT ANNOTATION EVOLUTION
# ==============================================================================
def _plot_annotation_completeness_evolution(
    annotation_storage: Dict[str, List[Tuple[str, str, str]]],
    iterations_to_highlight: Dict[str, Dict[str, Any]],
    graph_title: str = "Interactive clustering annotations over iterations",
    graph_folderpath: str = "",
    graph_filename: str = "plot_annotations_completeness_evolution.png",
) -> int:
    """
    A method aimed at create and store a graph that represents annotations evolution over iterations.

    Args:
        annotation_storage (Dict[str, List[Tuple[str, str, str]]]): The dictionary that store the triplet of annotated constraints for all iterations.
        iterations_to_highlight (Dict[str, Dict[str, Any]]): The dictionary that contains iteration that reach specif performance goal.
        graph_title (str, optional): The title of the graph to show. Defaults to `"Interactive clustering performance over iteration"`.
        graph_folderpath (str, optional): The foldername of the graph. Defaults to `""`.
        graph_filename (str, optional): The filename of the graph. Defaults to `"plot_annotations_completeness_evolution.png"`.

    Returns:
        int: Return `0` when finish.
    """

    # Create a new figure.
    fig: Figure = plt.figure(figsize=(15, 7.5), dpi=300.0)
    axis = fig.gca()

    # Define list of iterations to plot.
    list_of_iteration: List[int] = [
        int(iteration) for iteration in annotation_storage.keys()
    ]

    # Define cumulative list of constraints.
    cumul_list_of_must_link: List[int] = []
    cumul_list_of_cannot_link: List[int] = []
    cumul_list_of_all_constraints: List[int] = []

    # For all iteration of interactive clustering annotation.
    for _, list_of_triplet_annotated in annotation_storage.items():

        # Define current cumulative count for `"MUST_LINK"` and `"CANNOT_LINK"` constraints.
        count_ml: int = (
            0
            if (cumul_list_of_must_link == [])  # noqa: WPS520
            else cumul_list_of_must_link[-1]
        )
        count_cl: int = (
            0
            if (cumul_list_of_cannot_link == [])  # noqa: WPS520
            else cumul_list_of_cannot_link[-1]
        )

        # For all annotated constraints: updte the count.
        for annotation in list_of_triplet_annotated:
            if annotation[2] == "MUST_LINK":
                count_ml += 1
            elif annotation[2] == "CANNOT_LINK":
                count_cl += 1

        # Add the cumulaive counts to the lists.
        cumul_list_of_must_link.append(count_ml)
        cumul_list_of_cannot_link.append(count_cl)
        cumul_list_of_all_constraints.append(count_ml + count_cl)

    # Plot "MUST_LINK" evolution.
    axis.plot(
        list_of_iteration,  # x
        cumul_list_of_must_link,  # y
        label="MUST-LINK",
        marker="o",
        markerfacecolor="green",
        markersize=5,
        color="green",
        linewidth=1,
    )

    # Plot "CANNOT_LINK" evolution.
    axis.plot(
        list_of_iteration,  # x
        cumul_list_of_cannot_link,  # y
        label="CANNOT-LINK",
        marker="o",
        markerfacecolor="red",
        markersize=5,
        color="red",
        linewidth=1,
    )

    # Plot constraints evolution.
    axis.plot(
        list_of_iteration,  # x
        cumul_list_of_all_constraints,  # y
        label="Total",
        marker="o",
        markerfacecolor="blue",
        markersize=5,
        color="blue",
        linewidth=1,
        linestyle="dashed",
    )

    # Add markers for iteration that reach specific performance goal.
    for specific_iteration in iterations_to_highlight.keys():

        # Get the iteration.
        if iterations_to_highlight[specific_iteration]["iteration"] is not None:

            # Plot a vertical line at the iteration
            axis.axvline(
                x=int(str(iterations_to_highlight[specific_iteration]["iteration"])),
                color="black",
                linestyle="--",
            )

    # Set axis name.
    axis.set_xlabel("iteration (#)")
    axis.set_ylabel("constraints number (#)")

    # Plot the title.
    if graph_title is not None:
        axis.set_title(graph_title, fontsize=20)

    # Plot the legend.
    axis.legend(
        bbox_to_anchor=(0.50, -0.10),
        title="Type of annotated constraints",
        loc="upper center",
        ncol=4,
        title_fontsize=12,
        fontsize=10,
    )

    # Plot the grid.
    axis.grid(True)

    # Store the graph.
    fig.savefig(
        graph_folderpath + graph_filename,
        dpi=300,
        transparent=True,
        bbox_inches="tight",
    )

    # Close figure.
    plt.close()

    # End of script.
    return 0


# ==============================================================================
# PRIVATE - PLOT TIME SPENT EVOLUTION
# ==============================================================================
def _plot_time_spent_evolution(
    time_storage: Dict[str, Dict[str, float]],
    iterations_to_highlight: Dict[str, Dict[str, Any]],
    graph_title: str = "Interactive clustering time spent over iterations",
    graph_folderpath: str = "",
    graph_filename: str = "plot_computation_times_evolution.png",
) -> int:
    """
    A method aimed at create and store a graph that represents time spent evolution over iterations.

    Args:
        time_storage (Dict[str, Dict[str, float]]): The dictionary that store the datetime checkpoints for all iterations.
        iterations_to_highlight (Dict[str, Dict[str, Any]]): The dictionary that contains iteration that reach specif performance goal.
        graph_title (str, optional): The title of the graph to show. Defaults to `"Interactive clustering performance over iteration"`.
        graph_folderpath (str, optional): The foldername of the graph. Defaults to `""`.
        graph_filename (str, optional): The filename of the graph. Defaults to `"plot_computation_times_evolution.png"`.

    Returns:
        int: Return `0` when finish.
    """

    # Create a new figure.
    fig: Figure = plt.figure(figsize=(15, 7.5), dpi=300.0)
    axis = fig.gca()

    # Define list of iterations to plot.
    list_of_iteration: List[int] = [int(iteration) for iteration in time_storage.keys()]

    # Plot sampling computation time evolution.
    axis.plot(
        list_of_iteration,  # x
        [
            time_storage[iteration]["sampling_TOTAL_RUN"]
            for iteration in time_storage.keys()
        ],  # y
        label="Sampling",
        marker="o",
        markerfacecolor="green",
        markersize=5,
        color="green",
        linewidth=1,
    )

    # Plot clustering computation time evolution.
    axis.plot(
        list_of_iteration,  # x
        [
            time_storage[iteration]["clustering_TOTAL_RUN"]
            for iteration in time_storage.keys()
        ],  # y
        label="Clustering",
        marker="o",
        markerfacecolor="red",
        markersize=5,
        color="red",
        linewidth=1,
    )

    # Plot total computation time evolution.
    axis.plot(
        list_of_iteration,  # x
        [
            time_storage[iteration]["TOTAL_RUN"] for iteration in time_storage.keys()
        ],  # y
        label="Total",
        marker="o",
        markerfacecolor="blue",
        markersize=5,
        color="blue",
        linewidth=1,
        linestyle="dashed",
    )

    # Add markers for iteration that reach specific performance goal.
    for specific_iteration in iterations_to_highlight.keys():

        # Get the iteration.
        if iterations_to_highlight[specific_iteration]["iteration"] is not None:

            # Plot a vertical line at the iteration
            axis.axvline(
                x=int(str(iterations_to_highlight[specific_iteration]["iteration"])),
                color="black",
                linestyle="--",
            )

    # Set axis name.
    axis.set_xlabel("iteration (#)")
    axis.set_ylabel("time spent (s)")

    # Plot the title.
    axis.set_title(graph_title, fontsize=20)

    # Plot the legend.
    axis.legend(
        bbox_to_anchor=(0.50, -0.10),
        title="Computation steps",
        loc="upper center",
        ncol=4,
        title_fontsize=12,
        fontsize=10,
    )

    # Plot the grid.
    axis.grid(True)

    # Store the graph.
    fig.savefig(
        graph_folderpath + graph_filename,
        dpi=300,
        transparent=True,
        bbox_inches="tight",
    )

    # Close figure.
    plt.close()

    # End of script.
    return 0
