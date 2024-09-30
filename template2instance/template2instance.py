import json
import os
from pathlib import Path
import re
import shutil
from typeguard import typechecked
import semver
import traceback
from .open_source_license_management import get_license_short_text


@typechecked
def import_functions_from_file(file : str) -> dict:
    """
    This function imports functions from a file into current namespace.
    """
    with open(file, "r") as f:
        code = f.read()
    exec(code, globals())
    return globals()

@typechecked
def validate_email(email : str) -> bool:
    """
    This function validates an email address.
    """
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    return False

@typechecked
def validate_semver(version : str) -> bool:
    """
    This function validates a semantic version.
    """
    # check if the string is a valid semantic version
    return semver.Version.parse(version) is not None

@typechecked
def validate_camel_case(name : str) -> bool:
    """
    This function validates a camel case name.
    """
    return re.match(r"^[A-Z]+([A-Z][a-z][0-9]+)*$", name)

@typechecked
def validate_uncapitalized_camel_case(name : str) -> bool:
    """
    This function validates an uncapitalized camel case name.
    """
    return re.match(r"^[a-z]+([A-Z][a-z][0-9]+)*$", name)
    

@typechecked
def get_user_input(imsg : str, var : dict) -> str:
    """
    This function prompts the user to input a value for a variable.
    """
    if "default" in var:
        default = var["default"]
        if "value_example" in var:
            imsg += f" (default is {default}, e.g. {var['value_example']})"
        else:
            imsg += f" (default is {default})"
    print(imsg+".")
    if "type" in var:
        vtype = var["type"]
        while True:
            print("Please enter a value of type", vtype+".")
            print("?> ", end="")
            try:
                if vtype == "int":
                    value = int(input())
                elif vtype == "float":
                    value = float(input())
                elif vtype == "bool":
                    value = input().lower()
                    if value == "true" or value == "t" or value == "yes" or value == "y" or value == "1":
                        value = True
                    elif value == "false" or value == "f" or value == "no" or value == "n" or value == "0":
                        value = False
                    else:
                        raise ValueError
                else:
                    value = input()
                if "validation" in var:
                    try:
                        f = eval("validate_" + var["validation"])
                        if not f(value):
                            raise ValueError
                    except Exception as e:
                        trace = traceback.format_exc()
                        print(f"Error while validating the value: {e} : {trace}.")
                        raise ValueError
                # everything is fine, break the loop
                break
            except ValueError:
                try:
                    desc = " with description : " + var["description"]
                except:
                    desc = ""
                try:
                    validated_by = " validated by function: " + "validate_" + var["validation"]
                except:
                    validated_by = ""
                print(f"Invalid input ({value}). Please enter a value of type {vtype} {desc} {validated_by}.")
    else:
        value = input()
    if value == "" and "default" in var:
        value = var["default"]
    return str(value)


@typechecked
def cli_user_input(var_def : dict) -> dict:
    """
    This function takes a dictionary of variables and their default values and prompts the user to input new values.
    The function returns a dictionary of the new values.
    """
    var_new = {}
    variables = var_def["variables"]
    for var in variables:
        name = var["name"]
        desc = var["description"]
        if "function" in var:
            f = eval(var["function"])
            var_new[name] = f(var_new)
        else:
            imsg = f"Enter a value for {name} ({desc})"
            var_new[name] = get_user_input(imsg, var)
    return var_new


@typechecked
def create_instance(template_dir : str, instance_dir : str):
    """
    This function creates an instance from a template directory at instance_dir.

    Parameters
    ----------
    template_dir : str
        The path to the template directory
    instance_dir : str
        The path to the new instance directory
    """
    # Check if the template directory exists
    if not os.path.exists(template_dir):
        raise Exception(f"Template directory {template_dir} does not exist.")
    
    # Load the template variables located in template_variables.json file
    ## Check if the file exists
    var_json_path = os.path.join(template_dir, "template2instance/template_variables.json")
    if not os.path.exists(var_json_path):
        raise Exception(f"Template variables file {var_json_path} does not exist.")
    
    ## Load the file
    var_json = None
    with open(var_json_path, "r") as f:
        try:
            var_json = json.load(f)
        except Exception as e:
            raise Exception(f"Error while loading {var_json_path} as a json dict :  {e}.")
    try:
        vars = var_json["variables"]
    except:
        raise Exception(f"Variables not found in {var_json_path}.")
    ## Load the functions in the template2instance/template2instance_plugin.py file
    plugin_file = os.path.join(template_dir, "template2instance/template2instance_plugin.py")
    if os.path.exists(plugin_file):
        import_functions_from_file(plugin_file)
    variables = {}
    
    # For each variable compute the value and store it in the variables dictionary
    for v in vars:
        name = v["name"]
        if "default" == v["access"]:
            variables[name] = v["default"] % variables
        elif "function" == v["access"]:
            f = eval(v["function"])
            variables[name] = f(variables)
        else:
            variables[name] = get_user_input(f"Enter a value for {name}", v)
    
    # Check if the instance directory exists or create it
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
    
    # Copy recursively all files and directories from the template 
    # directory to the instance directory except the template2instance folder.
    # For each file: either the file name finishes by .template and the file should
    # be copied without the .template extension and the variables should be replaced
    # by calculated variables, or the file should be copied as is.
    p_template_dir = Path(template_dir)
    p_instance_dir = Path(instance_dir)
    for root, dirs, files in os.walk(template_dir, topdown=True):
        for d in dirs:
            if "template2instance" != d:      
                # Create the directory
                ## get the relative path of the directory d
                p_d = Path(d)
                ## create the directory in the instance directory
                new_path = p_instance_dir.joinpath(p_d)
                os.makedirs(new_path,exist_ok=True)
        r_d = Path(root)
        rel_path = r_d.relative_to(p_template_dir)
        new_r_path = p_instance_dir.joinpath(rel_path)
        for file in files:
            if file.endswith(".template"):
                try:
                    with open(os.path.join(root, file), "r") as f:
                        content = f.read()
                    content_updated = content % variables
                    new_file_path = new_r_path.joinpath(file[:-len(".template")])
                    with open(new_file_path, "w") as f:
                        f.write(content_updated)
                except Exception as e:
                    print(f"Error while processing file {file} : {e}")
            else:
                # copy the file as is
                shutil.copy(os.path.join(root, file), new_r_path)