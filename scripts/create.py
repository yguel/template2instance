from typing import Optional
import click
import template2instance as t2i
import traceback

output_config_help = """The system will output a configuration file containing 
all the project parameters (computed or entered by the user).
If no output-config-file is provided, the system will output a file named
"package_generation_config.json" in the project directory.
"""

@click.command()
@click.argument("template_dir", type=str, required=True)
@click.argument("project_dir", type=str, required=True)
@click.option("--config","-cfg", type=str, required=False, default=None, help="A configuration file to automate the parameter inputs.")
@click.option("--output-config","-oc", is_flag=True, show_default=True, default=False, help=output_config_help, required=False)
@click.option("--output-config-file","-ocf", type=str, required=False, default=None, help="The name of the output configuration file.")
def main(template_dir, project_dir, config, output_config, output_config_file):
    """create TEMPLATE_DIR PROJECT_DIR

    This script creates an instance of a template in a project directory.
    \f

    Parameters
    ----------
    template_dir : str
        The path to the template directory
    project_dir : str
        The path to the new project directory, where the template instance will be created.
    """
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