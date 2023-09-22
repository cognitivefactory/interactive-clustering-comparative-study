# -*- coding: utf-8 -*-

"""
* Name:         workerC_synthesis
* Description:  Worker to synthesize results of interactive clustering conflicts fix study experiments in an CSV file.
* Author:       Erwan Schild
* Created:      24/05/2021
* Licence:      CeCILL (https://cecill.info/licences.fr.html)
"""

# ==============================================================================
# IMPORT PYTHON DEPENDENCIES
# ==============================================================================

import json
import pandas as pd

from typing import Dict, List, Optional, Tuple, Union


# ==============================================================================
# WORKER - EXPERIMENT OVERVIEW
# ==============================================================================
def experiments_synthesis(
    list_of_experiment_environments: List[str],
) -> int:
    """
    A method aimed at synthesize performance of all experiments in a csv file.

    Args:
        list_of_experiment_environments (List[str]): The list of experiments environments used to synthesize results.

    Returns:
        int: Return `0` when finish.
    """

    # Initialize dictionary of synthesis.
    dict_of_experiments_synthesis: Dict[
        str, Dict[str, Union[str, float, int, None]]
    ] = {}

    # For each experiment environment...
    for env_path in list_of_experiment_environments:

        # Initialize dictionary of synthesis for this experiment.
        dict_of_experiments_synthesis[env_path] = {}

        ### ### ### ### ###
        ### Load files.
        ### ### ### ### ###
        
        # Load configuration for algorithm.
        with open(
            env_path + "../../config.json", "r"
        ) as file_config_algorithm:
            CONFIG_ALGORITHM = json.load(file_config_algorithm)
        
        # Load configuration for constraints selection.
        with open(
            env_path + "../config.json", "r"
        ) as file_config_constraints_selection:
            CONFIG_CONSTRAINTS_SELECTION = json.load(file_config_constraints_selection)
        
        # Load configuration for errors simulation.
        with open(
            env_path + "config.json", "r"
        ) as file_config_errors_simulation:
            CONFIG_ERRORS_SIMULATION = json.load(file_config_errors_simulation)
        
        # Load constraints.
        with open(
            env_path + "list_of_constraints.json", "r"
        ) as file_constraints:
            list_of_constraints = json.load(file_constraints)
        
        # Load clustering performances.
        with open(
            env_path + "dict_of_clustering_performances.json", "r"
        ) as file_clustering_perf:
            dict_of_clustering_performances = json.load(file_clustering_perf)

        ### ### ### ### ###
        ### Configuration.
        ### ### ### ### ###

        # NB : environments paths are formatted links : `../experiments/[DATASET]/[CLUSTERING]/[CONSTRAINTS_SELECTION]/[ERRORS_SIMULATION]`

        # Dataset information.
        dict_of_experiments_synthesis[env_path]["dataset"] = env_path.split("/")[2]
        # Algorithm information.
        dict_of_experiments_synthesis[env_path]["algorithm"] = env_path.split("/")[3]
        # Constraints selection information.
        dict_of_experiments_synthesis[env_path]["constraints_selection"] = env_path.split("/")[4]
        # Error simulation information.
        dict_of_experiments_synthesis[env_path]["error_simulation"] = env_path.split("/")[5]

        # constraints_selection__algorithm
        dict_of_experiments_synthesis[env_path]["constraints_selection__algorithm"] = CONFIG_CONSTRAINTS_SELECTION["sampling"]
        # constraints_selection__number
        dict_of_experiments_synthesis[env_path]["constraints_selection__number"] = CONFIG_CONSTRAINTS_SELECTION["nb_constraints"]
        # constraints_selection__random_seed
        dict_of_experiments_synthesis[env_path]["constraints_selection__random_seed"] = CONFIG_CONSTRAINTS_SELECTION["random_seed"]

        # error_simulation__error_rate
        dict_of_experiments_synthesis[env_path]["error_simulation__error_rate"] = str(CONFIG_ERRORS_SIMULATION["error_rate"]).replace('.',',')
        # error_simulation__random_seed
        dict_of_experiments_synthesis[env_path]["error_simulation__random_seed"] = CONFIG_ERRORS_SIMULATION["random_seed"]
        # error_simulation__with_fix
        dict_of_experiments_synthesis[env_path]["error_simulation__with_fix"] = CONFIG_ERRORS_SIMULATION["with_fix"]

        # constraints__annotated
        dict_of_experiments_synthesis[env_path]["constraints__annotated"] = len(list_of_constraints)
        # constraints__MUST LINK
        dict_of_experiments_synthesis[env_path]["constraints__MUST_LINK"] = len([
            constraint for constraint in list_of_constraints if constraint[2] == "MUST_LINK"
        ])
        # constraints__CANNOT_LINK
        dict_of_experiments_synthesis[env_path]["constraints__CANNOT_LINK"] = len([
            constraint for constraint in list_of_constraints if constraint[2] == "CANNOT_LINK"
        ])
        # constraints_-_errors
        dict_of_experiments_synthesis[env_path]["constraints__errors"] = len([
            constraint for constraint in list_of_constraints if constraint[3] is True
        ])
        # constraints__conflicts
        dict_of_experiments_synthesis[env_path]["constraints__conflicts"] = len([
            constraint for constraint in list_of_constraints if constraint[4] is True
        ])
        
        # clustering__v_measure
        dict_of_experiments_synthesis[env_path]["clustering__v_measure"] = str(
            dict_of_clustering_performances["v_measure"]
        ).replace(".", ",")
        # clustering__homogeneity
        dict_of_experiments_synthesis[env_path]["clustering__homogeneity"] = str(
            dict_of_clustering_performances["homogeneity"]
        ).replace(".", ",")
        # clustering__completeness
        dict_of_experiments_synthesis[env_path]["clustering__completeness"] = str(
            dict_of_clustering_performances["completeness"]
        ).replace(".", ",")

    ### ### ### ### ###
    ### Store file.
    ### ### ### ### ###

    # Define file path.
    filepath: str = "../results/experiments_synthesis.csv"

    # Define dataframe and store it to a CSV file.
    pd.DataFrame.from_dict(
        data=dict_of_experiments_synthesis,
        orient="index",
    ).to_csv(
        path_or_buf=filepath,
        sep=";",
    )

    # End of script.
    return 0
