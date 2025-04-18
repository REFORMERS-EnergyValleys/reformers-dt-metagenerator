import click
import pathlib
import os

from ..manifest import parse_manifest
from ..render import render_generator_script, DEFAULT_GENERATOR_TEMPLATE

@click.command()
@click.argument('manifest')
@click.option('-t', '--template',
              default=DEFAULT_GENERATOR_TEMPLATE,
              help='path to generator script template file')
@click.option('-o', '--output',
              default='generator.sh',
              help='path to output generator script file (default: generator.sh)')
def main(manifest, template, output):
    """
    Parse the MANIFEST (generator manifest file) and
    create a proper model generator script from it.
    """
    # Parse generator manifest file.
    manifest_file_path = pathlib.Path(manifest).resolve(strict=True)
    generator_name, generator_info = parse_manifest(manifest_file_path)

    # Render the generator script.
    template_file_path = pathlib.Path(template).resolve(strict=True)
    rendered_script = render_generator_script(
        generator_name, generator_info, template_file_path
    )

    def opener(path, flags):
        os.umask(0)
        return os.open(path, flags, 0o744)

    # Save the rendered template to a file
    with open(output, 'w', opener=opener) as f:
        f.write(rendered_script)

if __name__ == '__main__':
    main()
