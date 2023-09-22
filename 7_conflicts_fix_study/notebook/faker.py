# -*- coding: utf-8 -*-

"""
* Name:         faker
* Description:  A set of method to fake a dataset for interactive clustering study environments.
* Author:       Erwan Schild
* Created:      09/11/2022
* Licence:      CeCILL (https://cecill.info/licences.fr.html)
"""

# ==============================================================================
# IMPORT PYTHON DEPENDENCIES
# ==============================================================================

import os  # Path management.
import random
import string
from typing import Tuple, Dict, List  # Python code typing (mypy).


# ==============================================================================
# FAKER - SPELLING ERRORS
# ==============================================================================
def get_text_with_spelling_errors(
    text: str,
    k: int = 2,
) -> str:
    """
    Add spelling errors in a text.
    
    Args:
        text (str): The base text.
        k (int): The number of spelling errors to generate. Defaults to `2`.
        
    Return:
        str: The text with some spelling errors.
        
    """
    
    # Select index of letters to change.
    letters_to_change: List[int] = random.sample(
        range(len(text)),
        k=k,
    )
    
    # Change the selected letters.
    new_letters: List[str] = [
        (
            text[i]
            if i not in letters_to_change
            else random.choice(string.ascii_letters)
        )
        for i in range(len(text))
    ]
        
    # Return the new text with spelling errors.
    return "".join(new_letters)


# ==============================================================================
# FAKER - DATASET
# ==============================================================================

def fake_dataset(
    dict_of_texts: Dict[str, str],
    dict_of_true_intents: Dict[str, str],
    size: int,
    random_seed: int = 42,
) -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    Increase the size of a dataset by generating data with spelling errors.
    
    Args:
        dict_of_texts (Dict[str, str]): The texts in the base dataset.
        dict_of_true_intents (Dict[str, str]): The labels in the base dataset.
        size (int): The dataset size to reach.
        random_seed (int): The random seed. Defaults to `42`.
        
    Return:
        Tuple[Dict[str, str], Dict[str, str]]: The new dataset which some fake data.
    """
    
    # Set random seed.
    random.seed(random_seed)
    
    # Prepare results variables.
    new_dict_of_texts: Dict[str, str] = dict_of_texts.copy()
    new_dict_of_true_intents: Dict[str, str] = dict_of_true_intents.copy()
        
    # Prepare temporary variables.
    id_counter: int = 0
    list_of_text_ids: List[str] = list(dict_of_texts.keys())
    
    # Loop until the dataset hasn't the requested size...
    while len(new_dict_of_texts.keys()) < size:
        
        # Randomly choose a text.
        text_id: str = random.choice(list_of_text_ids)
                      
        # Generated a new text with spelling errors in the text.
        generated_text: str = get_text_with_spelling_errors(text=dict_of_texts[text_id])
        if generated_text in dict_of_texts.values():
            continue
                      
        # Add the generated text in the dataset.
        generated_text_id: str = "g_{id_counter}".format(id_counter=id_counter)
        new_dict_of_texts[generated_text_id] = generated_text
        new_dict_of_true_intents[generated_text_id] = dict_of_true_intents[text_id]
        
        # Increase the id counter.
        id_counter += 1
    
    # Return the new dataset.
    return (new_dict_of_texts, new_dict_of_true_intents)
        
        