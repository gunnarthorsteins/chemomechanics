clearvars;

cells_filename = 'cell.csv';
simulation_props_filename = 'simulation_props.json';
cell = readtable(cells_filename);

props = get_properties(simulation_props_filename);

no_layers = max(cell.layer_no);

c = sqrt(cell.E ./ cell.rho);

% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% % 1. Create computational grid
PML_size = 20;  % on each side of grid
Nx = props.Nx - 2*PML_size;
dx = sum(cell.x) / Nx;  % grid point spacing in the x direction [m]
kgrid = kWaveGrid(Nx, dx);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% 2. Define properties of propagation medium
medium.sound_speed = ones(Nx, 1);   % [m/s]
medium.density = ones(Nx, 1);
medium.alpha_coeff = ones(Nx, 1);
medium.alpha_power = props.alpha_power;

upper = 1;
for i = 1:no_layers
    no_points_per_layer = round(Nx * cell.x(i) / sum(cell.x));
    lower = upper;
    upper = upper + no_points_per_layer;

    if i == no_layers  % Last layer
        upper = Nx;
    end

    medium.sound_speed(lower:upper) = c(i);
    medium.density(lower:upper) = cell.rho(i);
    medium.alpha_coeff(lower:upper) = cell.alpha(i);
end

% create the time array
kgrid.makeTime(medium.sound_speed, props.cfl, props.simulation_duration);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% 3. Create initial pressure distribution as a single source point
source.p_mask = zeros(Nx, 1);
source.p_mask(PML_size+1, 1) = 1;

% define a time varying sinusoidal source
source.p = props.source_mag * sin(2 * pi * props.source_freq * kgrid.t_array);

% filter the source to remove high frequencies not supported by the grid
source.p = filterTimeSeries(kgrid, medium, source.p);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% 4. Define a single sensor point
sensor.mask = zeros(Nx, 1);
sensor.mask(Nx - PML_size - 1, 1) = 1; 
sensor.record = {'p', 'p_final'};


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% 5. Run the simulation
sensor_data = kspaceFirstOrder1D(kgrid, medium, source, sensor, ...
    'PlotLayout', false, 'PMLInside', false, ...
    'RecordMovie', false, 'DataCast', 'single', 'DataRecast', false);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 


function properties = get_properties(filename)
    fid = fopen(filename); 
    raw = fread(fid,inf); 
    str = char(raw'); 
    fclose(fid); 
    properties = jsondecode(str);
end