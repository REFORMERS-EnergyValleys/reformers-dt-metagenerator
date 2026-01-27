import pytest

import pathlib
import schema
import yaml

from metagenerator.manifest import *

@pytest.fixture
def manifest_file_path():
    return pathlib.Path(__file__).parent / 'test_manifest.yml'

def test_parse_manifest(manifest_file_path):
    name, info = parse_manifest(manifest_file_path)

    assert name == 'example-generator'

    version = info['version']
    assert version == 'v0'

    config = info['config']
    assert config['GENERATOR_REGISTRY'] == 'reformers-dev.ait.ac.at:8082'
    assert config['MODEL_REGISTRY'] == 'reformers-dev.ait.ac.at:8083'
    assert config['MODEL_DOCKERFILE'] == 'Dockerfile_model'

    generation_parameters = info['generation_parameters']
    assert generation_parameters['CONFIG_FILE']['info'] == 'path to config file with default values'
    assert generation_parameters['CONFIG_FILE']['default'] == '/config/config.yml'
    assert generation_parameters['GRID_DATA']['info'] == 'path to grid data'
    assert generation_parameters['GRID_DATA']['default'] == '/grid_data/grid.json'
    assert generation_parameters['INPUT_STREAM']['info'] == 'declare name of input stream'
    assert generation_parameters['INPUT_STREAM']['default'] == 'reformers.metering_data.DUMMY1'
    assert generation_parameters['OUTPUT_STREAM_BASE']['info'] == 'declare name of output stream'
    assert generation_parameters['OUTPUT_STREAM_BASE']['default'] == 'reformers.grid_sim.results'

    parameters = info['parameters']
    assert parameters['KNOWLEDGE_GRAPH_ENABLED']['info'] == 'enable knowledge graph'
    assert parameters['KNOWLEDGE_GRAPH_ENABLED']['example'] == "false"

    optional = info['optional']
    assert optional['KNOWLEDGE_GRAPH_ENDPOINT']['info'] == 'endpoint of the knowledge graph database'
    assert optional['KNOWLEDGE_GRAPH_ENDPOINT']['default'] == "http://reformers-dev.ait.ac.at/knowledge-graph/repositories/REFORMERS"

    build = info['build']
    assert 'python:3.10' in build['cache']
    assert 'python:3.10-slim' in build['cache']

def test_validate_manifest_error_empty(monkeypatch, manifest_file_path):
    monkeypatch.setattr(yaml, 'safe_load', lambda f: dict())

    with pytest.raises(schema.SchemaError) as exc_info:
        parse_manifest(manifest_file_path)
    assert 'Missing key' in str(exc_info.value)

def test_validate_manifest_error_invalid_version(monkeypatch, manifest_file_path):
    invalid = {'test': {'version': '_'}}
    monkeypatch.setattr(yaml, 'safe_load', lambda f: invalid)

    with pytest.raises(schema.SchemaError) as exc_info:
        parse_manifest(manifest_file_path)
    assert 'not a valid generator tag' in str(exc_info.value)

def test_validate_manifest_error_missing_nodes(monkeypatch, manifest_file_path):
    invalid = {'test': {'version': 'latest'}}
    monkeypatch.setattr(yaml, 'safe_load', lambda f: invalid)

    with pytest.raises(schema.SchemaError) as exc_info:
        parse_manifest(manifest_file_path)
    assert 'Missing key: \'config\'' in str(exc_info.value)

def test_validate_manifest_error_missing_config(monkeypatch, manifest_file_path):
    invalid = {'test': {'version': 'latest', 'config': {}, 'generation_parameters': {}}}
    monkeypatch.setattr(yaml, 'safe_load', lambda f: invalid)

    with pytest.raises(schema.SchemaError) as exc_info:
        parse_manifest(manifest_file_path)
    assert 'Missing keys: \'GENERATOR_REGISTRY\', \'MODEL_DOCKERFILE\', \'MODEL_REGISTRY\'' in str(exc_info.value)

def test_validate_manifest_error_invalid_registry(monkeypatch, manifest_file_path):
    invalid = {'test': {'version': 'latest', 'config': {'GENERATOR_REGISTRY': 'abc', 'MODEL_DOCKERFILE': 'abc', 'MODEL_REGISTRY': 'abc.de'}, 'generation_parameters': {}}}
    monkeypatch.setattr(yaml, 'safe_load', lambda f: invalid)

    with pytest.raises(schema.SchemaError) as exc_info:
        parse_manifest(manifest_file_path)
    assert 'not a valid registry descriptor' in str(exc_info.value)

def test_validate_manifest_error_missing_param_info(monkeypatch, manifest_file_path):
    invalid = {'test': {'version': 'latest', 'config': {'GENERATOR_REGISTRY': 'abc.de', 'MODEL_DOCKERFILE': 'abc', 'MODEL_REGISTRY': 'abc.de'}, 'generation_parameters': {'TEST':{}}}}
    monkeypatch.setattr(yaml, 'safe_load', lambda f: invalid)

    with pytest.raises(schema.SchemaError) as exc_info:
        parse_manifest(manifest_file_path)
    assert 'Missing keys: \'default\', \'info\'' in str(exc_info.value)
