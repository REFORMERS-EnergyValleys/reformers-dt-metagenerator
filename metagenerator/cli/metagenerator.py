import click
import pathlib
import os

from ..labels import labels_from_manifest
from ..manifest import parse_manifest
from ..render import render_metagenerator_script, DEFAULT_METAGENERATOR_TEMPLATE

@click.command()
@click.argument('manifest')
@click.option('-t', '--template',
              default=DEFAULT_METAGENERATOR_TEMPLATE,
              help='path to generator script template file')
@click.option('-o', '--output',
              default='metagenerator.sh',
              help='path to output metagenerator script file (default: metagenerator.sh)')
def main(manifest, template, output):
    """
    Parse the MANIFEST (generator manifest file) and
    create a proper metagenerator script from it.
    """
    # Parse generator manifest file.
    manifest_file_path = pathlib.Path(manifest).resolve(strict=True)
    generator_name, generator_info = parse_manifest(manifest_file_path)
    generator_labels = labels_from_manifest(generator_name, generator_info)

    # Render the generator script.
    template_file_path = pathlib.Path(template).resolve(strict=True)
    rendered_script = render_metagenerator_script(
        generator_name, generator_info, generator_labels, template_file_path
    )

    def opener(path, flags):
        os.umask(0)
        return os.open(path, flags, 0o744)

    # Save the rendered template to a file
    with open(output, 'w', opener=opener) as f:
        f.write(rendered_script)

if __name__ == '__main__':
    main()
