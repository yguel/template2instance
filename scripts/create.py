from typing import Optional
import click
import template2instance as t2i
import traceback
import os
from pathlib import Path

output_config_help = """The system will output a configuration file containing 
all the project parameters (computed or entered by the user).
If no output-config-file is provided, the system will output a file named
"package_generation_config.json" in the project directory.
"""

@click.command()
@click.argument("template_dir", type=str, required=True)
@click.argument("project_dir", type=str, required=True)
@click.option("--config","-cfg", type=str, required=False, default=None, help="A configuration file to automate the parameter inputs.")
@click.option("--output-config","-oc", is_flag=True, show_default=True, default=True, help=output_config_help, required=False)
@click.option("--output-config-file","-ocf", type=str, required=False, default=None, help="The name of the output configuration file.")
def main(template_dir, project_dir, config, output_config, output_config_file):
    """create TEMPLATE_DIR PROJECT_DIR

    This script creates an instance of a template in a project directory.
    \f

    Parameters
    ----------
    template_dir : str
        The path to the template directory or the name of the template in the templates directory.
        The script tries to resolve the template directory in the following order:
            1. If the template_dir is a valid path, the script uses it as the template directory.
            2. If the template_dir is not a valid path, the script searches for the template in the templates directory.
    project_dir : str
        The path to the new project directory, where the template instance will be created.
    config : str
        A configuration file to automate some of all the parameter inputs.
    output_config : bool
        If True, the script will output a configuration file containing all the project parameters (computed or entered by the user).
        If False, the script will not output a configuration file.
        default is True.
    output_config_file : str
        The path of the output configuration file. If not provided, the script will output a file named "package_generation_config.json" in the project directory.
    """
    
    # is the template_dir a valid path?
    if not os.path.exists(template_dir):
        # if not, try to find the template in the templates directory
        templates_folder_candidates = ["/usr/share/template2instance/templates", os.path.abspath( Path(__file__).parent.parent / "templates" ) ]
        found = False
        for f in templates_folder_candidates:
            new_template_dir = os.path.join(f, template_dir)
            if os.path.exists(new_template_dir):
                template_dir = new_template_dir
                found = True
                break
        if not found:
            print(f"Template {template_dir} not found. Known templates are in {templates_folder_candidates} folders.")
            return
    try:
        t2i.create_instance(template_dir, 
                            project_dir, 
                            config_file=config, 
                            output_config=output_config, 
                            output_config_file=output_config_file)
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()