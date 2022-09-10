import pandas as pd

properties = {
    'Nx': 512,  # number of grid points in the x (row) direction
    'cfl': 0.2,
    'simulation_duration': 1e-7,  # [s]
    'source_freq': 25e6,  # [Hz]
    'source_mag': 2,  # [Pa]
    'alpha_power': 1.5,
}

electrolyte = [2e9, 1000, 50e-6, 1.2]

layers_raw = {
    'case': [70E9, 2700, 100E-6, 0.7],
    'aluminum': [70E9, 2700, 10E-6, 0.7],
    'cathode': [200e9, 3300, 50e-6, 0.5],
    'anode': [10E9, 2260, 60E-6, 0.6],
    'anolyte': electrolyte,
    'separator': [2e9, 920, 20e-6, 1.1],
    'catholyte': electrolyte,
    'copper': [130E9, 8960, 10E-6, 0.5],
}

keys = ['name', 'E', 'rho', 'x', 'alpha']
no_stacks = 1

dummy_df = pd.DataFrame(data={
    'nobody': ['expects', 'the'],
    'spanish': ['inquisition', '!']
})
