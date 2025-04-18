import pytest

from metagenerator.manifest import *
from metagenerator.labels import *

@pytest.fixture
def manifest_file_path():
    return pathlib.Path(__file__).parent / 'test_manifest.yml'

def test_render_script_no_version(manifest_file_path):
    name, info = parse_manifest(manifest_file_path)

    info.pop('version')

    with pytest.raises(Exception) as exc_info:
        labels_from_manifest(name, info)

    assert str(exc_info.value) == 'version not specified in generator manifest'

def test_render_script(manifest_file_path):
    name, info = parse_manifest(manifest_file_path)

    labels = labels_from_manifest(name, info)

    assert 'example-generator.v0.config.GENERATOR_REGISTRY=reformers-dev.ait.ac.at:8082' in labels
    assert 'example-generator.v0.config.MODEL_REGISTRY=reformers-dev.ait.ac.at:8083' in labels
    assert 'example-generator.v0.config.MODEL_DOCKERFILE=Dockerfile_model' in labels
    assert 'example-generator.v0.parameters.CONFIG_FILE.info=path to config file with default values' in labels
    assert 'example-generator.v0.parameters.CONFIG_FILE.default=/config/config.yml' in labels
    assert 'example-generator.v0.parameters.GRID_DATA.info=path to grid data' in labels
    assert 'example-generator.v0.parameters.GRID_DATA.default=/grid_data/grid.json' in labels
    assert 'example-generator.v0.parameters.INPUT_STREAM.info=declare name of input stream' in labels
    assert 'example-generator.v0.parameters.INPUT_STREAM.default=reformers.metering_data.DUMMY1' in labels
    assert 'example-generator.v0.parameters.OUTPUT_STREAM_BASE.info=declare name of output stream' in labels
    assert 'example-generator.v0.parameters.OUTPUT_STREAM_BASE.default=reformers.grid_sim.results' in labels
    assert 'example-generator.v0.build.cache=[python:3.10,python:3.10-slim]' in labels
