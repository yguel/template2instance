# This script traverses a folder and looks for anything that looks like a variable name:
#  - in any folder of file name the list of strings in a %(xxxx)s pattern
#  - in all files, the list of strings in a %(xxxx)s pattern
# It record the list of variables found in each file with its line number.
# It create a report with the list of variables and the places where they have been found as a json file.

import os
import re
from typing import List

reg_match = r'%\((\w+)\)s'

def find_variables_in_file(file_path: str) -> dict:
    """
    This function finds all the variables in a file.
    
    Parameters
    ----------
    file_path : str
        The path to the file
        
    Returns
    -------
    dict
        A dictionary with the variables as keys and the list of line numbers where they have been found as values
    """
    variables = {}
    with open(file_path, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            for match in re.finditer(reg_match, line):
                variable = match.group(1)
                if variable not in variables:
                    variables[variable] = [i]
                variables[variable].append(i)
    return variables

def find_variables_in_folder(folder_path: str) -> dict:
    """
    This function finds all the variables in a folder.
    
    Parameters
    ----------
    folder_path : str
        The path to the folder
        
    Returns
    -------
    dict
        A dictionary with the variables as keys and as value a list of dictionaries with the following keys:
            - "type" : "file_name" or "folder_name" or "file"
            - "path" : the path to the file or folder
            - "lines" : the list of line numbers where the variable has been found only if the type is "file"
    """
    variables = {}
    for root, dirs, files in os.walk(folder_path):
        # for dirs and files we also look into their content
        for file in files:
            # look for variables in the file name
            file_name : str = file
            for match in re.finditer(reg_match, file_name):
                variable = match.group(1)
                entry = {"type": "file_name", "path": os.path.join(root, file)}
                if variable not in variables:
                    variables[variable] = [entry]
                else:
                    variables[variable].append(entry)
            # look for variables in the file content
            file_path = os.path.join(root, file) 
            vars = find_variables_in_file(file_path)
            for var, lines in vars.items():
                if var not in variables:
                    variables[var] = [{"type": "file", "path": file_path, "lines": lines}]
                else:
                    variables[var].append({"type": "file", "path": file_path, "lines": lines})
        for dir in dirs:
            # look for variables in the folder name
            folder_name : str = dir
            for match in re.finditer(reg_match, folder_name):
                variable = match.group(1)
                entry = {"type": "folder_name", "path": os.path.join(root, dir)}
                if variable not in variables:
                    variables[variable] = [entry]
                else:
                    variables[variable].append(entry)
            dir_path = os.path.join(root, dir)
            vars = find_variables_in_folder(dir_path)
            for var, entries in vars.items():
                if var not in variables:
                    variables[var] = entries
                else:
                    variables[var] += entries
    return variables
