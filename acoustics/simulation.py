"""Wrapper for running MATLAB simulation.

Requires MATLAB Engine API to be installed on system:
https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html
"""

import matlab.engine as engine

try:
    engine_ = engine.start_matlab()
except:
    raise Exception('Cannot run simulation from python. Switch to native MATLAB engine to run simulate.m and then return to jupyter.')

paths = ['k-Wave', 'acoustics']

# Add folders to path so MATLAB can execute the respective scripts
for path in paths:
    s = engine_.genpath(path)
    engine_.addpath(s, nargout=0)

def run() -> None:
    """The simulation is saved to an hdf5 file,
    which is why it doesn't return anything
    """
#     try:
    engine_.simulate(nargout=0)  # Call .m script 'simulate'