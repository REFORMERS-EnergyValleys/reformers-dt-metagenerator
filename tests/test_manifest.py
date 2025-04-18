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

    parameters = info['parameters']
    assert parameters['CONFIG_FILE']['info'] == 'path to config file with default values'
    assert parameters['CONFIG_FILE']['default'] == '/config/config.yml'
    assert parameters['GRID_DATA']['info'] == 'path to grid data'
    assert parameters['GRID_DATA']['default'] == '/grid_data/grid.json'
    assert parameters['INPUT_STREAM']['info'] == 'declare name of input stream'
    assert parameters['INPUT_STREAM']['default'] == 'reformers.metering_data.DUMMY1'
    assert parameters['OUTPUT_STREAM_BASE']['info'] == 'declare name of output stream'
    assert parameters['OUTPUT_STREAM_BASE']['default'] == 'reformers.grid_sim.results'

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
    assert 'Missing keys: \'config\', \'parameters\'' in str(exc_info.value)

def test_validate_manifest_error_missing_config(monkeypatch, manifest_file_path):
    invalid = {'test': {'version': 'latest', 'config': {}, 'parameters': {}}}
    monkeypatch.setattr(yaml, 'safe_load', lambda f: invalid)

    with pytest.raises(schema.SchemaError) as exc_info:
        parse_manifest(manifest_file_path)
    assert 'Missing keys: \'GENERATOR_REGISTRY\', \'MODEL_DOCKERFILE\', \'MODEL_REGISTRY\'' in str(exc_info.value)

def test_validate_manifest_error_invalid_registry(monkeypatch, manifest_file_path):
    invalid = {'test': {'version': 'latest', 'config': {'GENERATOR_REGISTRY': 'abc', 'MODEL_DOCKERFILE': 'abc', 'MODEL_REGISTRY': 'abc.de'}, 'parameters': {}}}
    monkeypatch.setattr(yaml, 'safe_load', lambda f: invalid)

    with pytest.raises(schema.SchemaError) as exc_info:
        parse_manifest(manifest_file_path)
    assert 'not a valid registry descriptor' in str(exc_info.value)

def test_validate_manifest_error_missing_param_info(monkeypatch, manifest_file_path):
    invalid = {'test': {'version': 'latest', 'config': {'GENERATOR_REGISTRY': 'abc.de', 'MODEL_DOCKERFILE': 'abc', 'MODEL_REGISTRY': 'abc.de'}, 'parameters': {'TEST':{}}}}
    monkeypatch.setattr(yaml, 'safe_load', lambda f: invalid)

    with pytest.raises(schema.SchemaError) as exc_info:
        parse_manifest(manifest_file_path)
    assert 'Missing keys: \'default\', \'info\'' in str(exc_info.value)
