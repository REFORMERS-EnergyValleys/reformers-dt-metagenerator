import jinja2
import pathlib

DEFAULT_GENERATOR_TEMPLATE = pathlib.Path(__file__).parent / 'templates' / 'generator.sh.j2'
DEFAULT_METAGENERATOR_TEMPLATE = pathlib.Path(__file__).parent / 'templates' / 'metagenerator.sh.j2'

def render_generator_script(
        generator_name: str,
        generator_info: dict,
        template_file_path: pathlib.Path = DEFAULT_GENERATOR_TEMPLATE,
    ) -> str:
    """
    Render the generator script.
    """
    # Read Jinja2 template.
    with open(template_file_path, 'r') as template_file:
        template = template_file.read()

    # Create Jinja2 environment.
    jinja_env = jinja2.Environment(loader=jinja2.BaseLoader())

    # Render the template.
    return jinja_env.from_string(template).render(
        generator_name=generator_name,
        generator_tag=generator_info['version'],
        generator_config=generator_info['config'],
        generator_parameters=generator_info['parameters'],
    )

def render_metagenerator_script(
        generator_name: str,
        generator_info: dict,
        generator_labels: list[str],
        template_file_path: pathlib.Path = DEFAULT_METAGENERATOR_TEMPLATE,
    ) -> str:
    """
    Render the metagenerator script.
    """
    # Read Jinja2 template.
    with open(template_file_path, 'r') as template_file:
        template = template_file.read()

    # Create Jinja2 environment.
    jinja_env = jinja2.Environment(loader=jinja2.BaseLoader())

    # Render the template.
    return jinja_env.from_string(template).render(
        generator_name=generator_name,
        generator_tag=generator_info['version'],
        generator_labels=generator_labels,
        generator_config=generator_info['config'],
    )
