import json
import h5py
import numpy as np
import pandas as pd
from typing import List, Tuple


def _matlabify(df: pd.DataFrame) -> pd.DataFrame:
    """Zero-based indexing to one-based.

    Helper function for assemble_cell().

    Args:
        df (pd.DataFrame): Dataframe with zero-based
            numerical index.

    Returns:
        pd.DataFrame: One-based dataframe.
    """

    df.index += 1

    return df


def _create_layer(keys: list, name: str, props: list) -> dict:
    """Parses layer properties into a dict.

    Helper function for stack_layers().

    Args:
        keys (list): Mechanical property keys.
        name (str): Layer name.
        props (list): Mechanical properties.

    Returns:
        dict: The layer. 
    """

    props_ = props.copy()
    props_.insert(0, name)

    return dict(zip(keys, props_))


def assemble_cell(layers: List[dict],
                  index_name: str = 'layer_no') -> pd.DataFrame:
    """Assembles stacked layers (a list of dicts) into a cell (homogeneous dataframe).

    Args:
        layers (list[dict]): Cell layers.
        index_name (str, optional): Name of index column.
            Defaults to 'layer_no'.

    Returns:
        pd.DataFrame: _description_

    Example:

    """

    layers = pd.DataFrame(data=layers)
    layers.index.name = index_name
    layers = _matlabify(df=layers)

    return layers


def fetch_simulation(filename: str = 'simulation.h5') -> np.array:
    """Fetches simulation data from hdf5 file.

    Args:
        filename (str, optional): Simulation filename.
            Defaults to 'simulation.h5'.

    Returns:
        np.array: Pressure values. Shape: timestepsXgridsize
    """
    with h5py.File(filename, 'r') as f:
        simulation = np.array(f['/simulation'][:], dtype=np.float16)

    return simulation.T


def save_cell(cell: pd.DataFrame) -> None:
    """Saves cell properties to a csv-file.

    Args:
        cell (pd.DataFrame): Cell properties,
            as prepared by assemble_cell().
    """
    cell.to_csv('cell.csv')


def save_properties(properties: dict) -> None:
    """Saves simulation properties to a json-file.

    Args:
        properties (dict): Simulation properties.
    """

    with open('simulation_props.json', 'w') as f:
        json.dump(properties, f)


def adjust_density(soc: float, rho_anode_0: float,
                   rho_cathode_0: float) -> Tuple[float]:
    """Adjusts electrode density by interpolating against lithiation.

    TODO: Make more realistic. Need a real look-up table.

    Args:
        soc (float): State-of-Charge (0-1).
        rho_anode_0 (float): Anode density at 0% SoC.
        rho_cathode_0 (float): Cathode density at 0% SoC.

    Returns:
        float: rho_anode, scaled.
        float: rho_cathode, scaled.
    """

    rho_anode = rho_anode_0 * (1 - 0.03 * soc)
    rho_cathode = rho_cathode_0 * (1 + 0.03 * soc)

    return rho_anode, rho_cathode


def adjust_stiffness(soc: float, E_anode_0: float,
                     E_cathode_0: float) -> Tuple[float]:
    """Adjusts electrode stiffness by interpolating against lithiation.

    TODO: Make more realistic. Need a real look-up table.

    Args:
        soc (float): State-of-Charge (0-1).
        E_anode_0 (float): Anode Young's modulus at 0% SoC.
        E_cathode_0 (float): Cathode Young's modulus at 0% SoC.

    Returns:
        float: E_anode, scaled.
        float: E_cathode, scaled.
    """

    E_anode = E_anode_0 * (1 - 0.05 * soc)
    E_cathode = E_cathode_0 * (1 + 0.01 * soc)

    return E_anode, E_cathode


def soc(voltage: np.array) -> np.array:
    """

    Assumes a linear relationship between SoC and Voltage.
    As such it's really facile 

    TODO: Make more realistic.

    Args:
        voltage (np.array): _description_

    Returns:
        np.array: State-of-Charge
    """

    if voltage > 4.2 or voltage < 2.7:
        raise ValueError('Passed voltage outside normal operational bounds')

    soc = 0.67 * voltage - 1.8

    return soc


def stack_layers(keys: list, layers_raw: dict, no_stacks: int) -> List[dict]:
    """Stacks individual layers into a list. 

    One of layers_raw should be named 'case' and will be the very first,
    and very last, layer. This is irrespective of the number of layers.

    Args:
        keys (list): Mechanical property keys.
        layers_raw (dict): Raw layers
        no_stacks (int): Number of stacks, i.e. how many times the
            anode/elyte/separator/elyte/cathode is folded upon
            itself.

    Returns:
        list[dict]: A list with a dict for each layer.
    """

    stack = list()
    case_layer = _create_layer(keys=keys,
                               name='case',
                               props=layers_raw['case'])
    stack.append(case_layer)

    # Create a stack
    layers = list()
    for name, props in layers_raw.items():

        if name == 'case':
            continue

        intralayer = _create_layer(keys=keys, name=name, props=props)
        layers.append(intralayer)

    # Repeat stacks
    for _ in range(no_stacks):
        layers = layers[::-1]  # Layers are folded
        stack.extend(layers)

    stack.append(case_layer)

    return stack