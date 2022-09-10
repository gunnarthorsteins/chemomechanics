from time import time
from os.path import exists, getmtime
import pytest

from acoustics import simulation
from acoustics import utils
import params

simulation_data = 'simulation.h5'

@pytest.fixture(scope='session')
def prep_simulation():
    """Ensure simulation data exists"""
    utils.save_properties(properties=params.properties)

    layers = utils.stack_layers(keys=params.keys,
                                layers_raw=params.layers_raw,
                                no_stacks=params.no_stacks)
    cell = utils.assemble_cell(layers=layers)
    utils.save_cell(cell=cell)


@pytest.fixture(scope='session')
def run():
    simulation.run()


def test_simulation_data_exists(run):
    assert exists(simulation_data)


def test_simulation_created_this_minute(run):
    last_edited = getmtime(simulation_data)

    assert last_edited > time() - 60


@pytest.fixture
def _simulation_data(run):
    simulation_data_ = utils.fetch_simulation()

    return simulation_data_


def test_simulation_data_not_empty(_simulation_data):
    assert len(_simulation_data) > 0
