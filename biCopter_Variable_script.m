% Bi-Copter Physical Parameters
m = 0.5;      % Mass (kg)
g = 9.81;     % Gravity (m/s^2)
L = 0.25;     % Distance from CoM to motor (m)

% Moments of Inertia (kg*m^2) - assuming a simple rectangular body
Ixx = 0.005;
Iyy = 0.005;
Izz = 0.01;
I = diag([Ixx, Iyy, Izz]); % Inertia Matrix

% Motor & Servo Limits
max_thrust_per_motor = 5; % Newtons (adjust based on motor specs)
min_thrust_per_motor = 0; % Newtons
max_servo_angle = pi/6;   % Radians (30 degrees)
min_servo_angle = -pi/6;  % Radians (-30 degrees)

% Initial Conditions (at rest on the ground)
initial_position = [0; 0; 0];      % [x, y, z]
initial_velocity = [0; 0; 0];      % [u, v, w]
initial_angles = [0; 0; 0];        % [phi, theta, psi]
initial_ang_velocity = [0; 0; 0];  % [p, q, r]

% Combine initial states into a single vector for Simulink
initial_states = [initial_position; initial_angles; initial_velocity; initial_ang_velocity];
% --- Motor Parameters ---
k_T = 1.5e-6;   % Thrust coefficient (N/(rad/s)^2)
tau_motor = 0.05; % Motor time constant in seconds (how fast it responds)

disp('Bi-Copter parameters loaded into workspace.');