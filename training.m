% 1. SETUP THE ENVIRONMENT
map = zeros(100, 100); 
map(21:80, 41) = 1; 
map(21, 41:80) = 1;
start_pos = [1, 1];
goal_pos = [100, 100];
z_reference = 10;
% 2. GENERATE THE GLOBAL PATH (Runs ONCE)
fprintf('Generating A* path...\n');
astar_path = a_star_path(map, start_pos, goal_pos);
fprintf('Path generated.\n');
% 3. LINK TO YOUR SIMULINK MODEL
%env = rlSimulinkEnv('my_bicopter_model', 'my_bicopter_model/RL Agent', obsInfo, actInfo);
% 5. START TRAINING
%trainOpts = rlTrainingOptions();
%trainingStats = train(agent, env, trainOpts);