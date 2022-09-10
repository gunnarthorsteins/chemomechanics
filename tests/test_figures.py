from matplotlib import animation
import matplotlib.pyplot as plt
from os.path import exists
from os import getcwd
import pytest

from acoustics import figures, simulation, utils
import params

frames = 10
pwd = getcwd()

@pytest.fixture
def _simulation():
    simulation.run()

@pytest.fixture
def simulation_data():
    simulation_data = utils.fetch_simulation()

    return simulation_data

@pytest.fixture
def cell():
    layers = utils.stack_layers(keys=params.keys,
                                layers_raw=params.layers_raw,
                                no_stacks=params.no_stacks)
    cell = utils.assemble_cell(layers=layers)
    
    return cell

def test_animate(_simulation, simulation_data, cell):
    animation_ = figures.animate(simulation=simulation_data, cell=cell, props=params.properties, frames=frames)

    assert isinstance(animation_, animation.FuncAnimation)


def test_plot_sensor(simulation_data):
    figures.plot_sensor(
        p_sensor=simulation_data[:, -10],
        simulation_duration=params.properties['simulation_duration']
    )

    plt.clf()


@pytest.fixture
def _animation(simulation_data, cell):
    animation_ = figures.animate(simulation=simulation_data, cell=cell, props=params.properties, frames=frames)

    return animation_


def test_save_animation(_animation):
    now = figures.save_animation(animation_=_animation, fps=frames)

    assert exists(f'{pwd}/gifs/simulation_{now}.gif')