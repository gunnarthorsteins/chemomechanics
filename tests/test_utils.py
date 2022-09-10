from math import isclose
from os.path import exists
import pandas as pd
import pytest

from acoustics import utils
import params


@pytest.fixture
def cell():
    layers = utils.stack_layers(keys=params.keys,
                                layers_raw=params.layers_raw,
                                no_stacks=params.no_stacks)
    cell = utils.assemble_cell(layers=layers)

    return cell


@pytest.fixture
def layers():
    layers = utils.stack_layers(keys=params.keys,
                                layers_raw=params.layers_raw,
                                no_stacks=params.no_stacks)

    return layers


def test_matlabify():
    df_ = utils._matlabify(df=params.dummy_df)

    assert df_.index[0] == 1


def test_create_layer():
    for name, props in params.layers_raw.items():
        layer = utils._create_layer(keys=params.keys, name=name, props=props)
        break

    assert isinstance(layer, dict)
    assert layer['name'] == 'case'


def test_assemble_cell(layers):
    cell = utils.assemble_cell(layers=layers)

    assert isinstance(cell, pd.DataFrame)
    assert cell.index.name == 'layer_no'


def test_save_properties():
    utils.save_properties(properties=params.properties)


def test_scale_stiffness():
    E_anode, E_cathode = utils.adjust_stiffness(soc=0.5,
                                               E_anode_0=10e9,
                                               E_cathode_0=200e9)

    assert isclose(E_anode, 9.75e9, abs_tol=1e6)
    assert isclose(E_cathode, 201e9, abs_tol=1e6)


def test_soc():
    soc = utils.soc(voltage=3.45)

    assert isclose(soc, 0.5, abs_tol=1e-1)


def test_stack_layers():
    layers = utils.stack_layers(keys=params.keys,
                                layers_raw=params.layers_raw,
                                no_stacks=params.no_stacks)

    assert isinstance(layers, list)
    assert isinstance(layers[0], dict)
    assert layers[0]['name'] == 'case'
    assert layers[1]['name'] != 'case'
    assert layers[-1]['name'] == 'case'


def test_save_cell(cell):
    utils.save_cell(cell=cell)

    assert exists('cell.csv')