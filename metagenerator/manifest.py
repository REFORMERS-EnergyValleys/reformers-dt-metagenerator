import pathlib
import yaml
from schema import Optional, Regex, Schema
from typing import Any, Tuple

def __validate_manifest(
        data: Any
    ) -> Any:
    """
    Validate the data loaded from the manifest file
    """
    regex_generator_name = '^[a-zA-Z0-9][a-zA-Z0-9-]+$'
    error_generator_name = '\'{}\' is not a valid generator name'
    regex_generator_tag = '^[a-zA-Z0-9][a-zA-Z0-9-]+$'
    error_generator_tag = '\'{}\' is not a valid generator tag'
    regex_domain_and_port = '^(?:[A-Za-z0-9-]+\.)+[A-Za-z0-9]{1,3}(?::\d{1,5})?$'
    error_domain_and_port = '\'{}\' is not a valid registry descriptor'

    schema = Schema({
        Regex(regex_generator_name, error=error_generator_name): Schema({
            'version': Regex(regex_generator_tag, error=error_generator_tag),
            'config': Schema({
                'GENERATOR_REGISTRY': Regex(regex_domain_and_port, error=error_domain_and_port),
                'MODEL_REGISTRY': Regex(regex_domain_and_port, error=error_domain_and_port),
                'MODEL_DOCKERFILE': str,
                Optional(str): object,
                }),
            'parameters': Schema({
                str: Schema({
                    'info': str,
                    'default': str,
                    }),
                }),
            Optional('build'): object,
            })
        })

    return schema.validate(data)

def parse_manifest(
        manifest_file_path: pathlib.Path
    ) -> Tuple[str, dict]:
    """
    Parse the generator manifest file.
    """
    with open(manifest_file_path, 'r') as file:
        data = yaml.safe_load(file)
        generator_manifest: dict = __validate_manifest(data)

    if not 1 == len(generator_manifest):
        raise ValueError('expected only 1 main node in manifest')

    # Retrieve generator name and manifest info from file.
    generator_name = next(iter(generator_manifest))
    generator_info = generator_manifest[generator_name]

    return generator_name, generator_info
