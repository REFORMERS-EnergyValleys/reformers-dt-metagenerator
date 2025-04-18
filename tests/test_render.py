import pytest

from metagenerator.labels import *
from metagenerator.manifest import *
from metagenerator.render import *

@pytest.fixture
def manifest_file_path():
    return pathlib.Path(__file__).parent / 'test_manifest.yml'

def test_render_generator_script(manifest_file_path):
    name, info = parse_manifest(manifest_file_path)

    rendered_script = render_generator_script(name, info)

    assert 'GENERATOR_NAME=example-generator' in rendered_script
    assert 'GENERATOR_TAG=v0' in rendered_script
    assert 'GENERATOR_REGISTRY=${GENERATOR_REGISTRY:-reformers-dev.ait.ac.at:8082}' in rendered_script
    assert 'MODEL_REGISTRY=${MODEL_REGISTRY:-reformers-dev.ait.ac.at:8083}' in rendered_script
    assert 'MODEL_DOCKERFILE=${MODEL_DOCKERFILE:-Dockerfile_model}' in rendered_script
    assert 'CONFIG_FILE=${CONFIG_FILE:-/config/config.yml}' in rendered_script
    assert 'GRID_DATA=${GRID_DATA:-/grid_data/grid.json}' in rendered_script
    assert 'INPUT_STREAM=${INPUT_STREAM:-reformers.metering_data.DUMMY1}' in rendered_script
    assert 'OUTPUT_STREAM_BASE=${OUTPUT_STREAM_BASE:-reformers.grid_sim.results}' in rendered_script
    assert 'Run generator example-generator:v0 with the following parameters:' in rendered_script
    assert 'echo - GENERATOR_REGISTRY: ${GENERATOR_REGISTRY}' in rendered_script
    assert 'echo - MODEL_REGISTRY: ${MODEL_REGISTRY}' in rendered_script
    assert 'echo - MODEL_DOCKERFILE: ${MODEL_DOCKERFILE}' in rendered_script
    assert 'echo - CONFIG_FILE: ${CONFIG_FILE}' in rendered_script
    assert 'echo - GRID_DATA: ${GRID_DATA}' in rendered_script
    assert 'echo - INPUT_STREAM: ${INPUT_STREAM}' in rendered_script
    assert 'echo - OUTPUT_STREAM_BASE: ${OUTPUT_STREAM_BASE}' in rendered_script
    assert '--build-arg GENERATOR_REGISTRY=${GENERATOR_REGISTRY}' in rendered_script
    assert '--build-arg MODEL_REGISTRY=${MODEL_REGISTRY}' in rendered_script
    assert '--build-arg MODEL_DOCKERFILE=${MODEL_DOCKERFILE}' in rendered_script
    assert '--build-arg CONFIG_FILE=${CONFIG_FILE}' in rendered_script
    assert '--build-arg GRID_DATA=${GRID_DATA}' in rendered_script
    assert '--build-arg INPUT_STREAM=${INPUT_STREAM}' in rendered_script
    assert '--build-arg OUTPUT_STREAM_BASE=${OUTPUT_STREAM_BASE}' in rendered_script

def test_render_metagenerator_script(manifest_file_path):
    name, info = parse_manifest(manifest_file_path)
    labels = labels_from_manifest(name, info)

    print(name, info, labels)

    rendered_script = render_metagenerator_script(name, info, labels)

    print(rendered_script)

    assert 'GENERATOR_NAME=example-generator' in rendered_script
    assert 'GENERATOR_TAG=v0' in rendered_script
    assert '--label "example-generator.v0.config.MODEL_DOCKERFILE=Dockerfile_model"' in rendered_script
    assert '--label "example-generator.v0.config.MODEL_REGISTRY=reformers-dev.ait.ac.at:8083"' in rendered_script
    assert '--label "example-generator.v0.parameters.CONFIG_FILE.info=path to config file with default values"' in rendered_script
    assert '--label "example-generator.v0.parameters.CONFIG_FILE.default=/config/config.yml"' in rendered_script
    assert '--label "example-generator.v0.parameters.GRID_DATA.info=path to grid data"' in rendered_script
    assert '--label "example-generator.v0.parameters.GRID_DATA.default=/grid_data/grid.json"' in rendered_script
    assert '--label "example-generator.v0.parameters.INPUT_STREAM.info=declare name of input stream"' in rendered_script
    assert '--label "example-generator.v0.parameters.INPUT_STREAM.default=reformers.metering_data.DUMMY1"' in rendered_script
    assert '--label "example-generator.v0.parameters.OUTPUT_STREAM_BASE.info=declare name of output stream"' in rendered_script
    assert '--label "example-generator.v0.parameters.OUTPUT_STREAM_BASE.default=reformers.grid_sim.results"' in rendered_script
    assert '--label "example-generator.v0.build.cache=[python:3.10,python:3.10-slim]"' in rendered_script
