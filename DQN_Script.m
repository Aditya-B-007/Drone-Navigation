obsInfo = rlNumericSpec([10 1]);
obsInfo.Name = 'Bicopter_Observations';
actInfo = rlNumericSpec([4 1]);
actInfo.Name = 'Bicopter_Control_Signals';
actInfo.LowerLimit = [-1; -1; -1; -1];
actInfo.UpperLimit = [1; 1; 1; 1];
criticLG = layerGraph();

% Define the layers for the observation path
observationPath = [
    featureInputLayer(obsInfo.Dimension(1),'Normalization','none','Name','observation')
    fullyConnectedLayer(128,'Name','fc1')
    reluLayer('Name','relu1')
    fullyConnectedLayer(128,'Name','fc2')
    reluLayer('Name','relu2')];

% Define the layers for the action path (it's just an input layer)
actionPath = [
    featureInputLayer(actInfo.Dimension(1),'Normalization','none','Name','action')];
    
% Define the remaining common path layers
commonPath = [
    concatenationLayer(1,2,'Name','concat')
    fullyConnectedLayer(1,'Name','criticoutput')];

% Add all the layer blocks to the layer graph
criticLG = addLayers(criticLG, observationPath);
criticLG = addLayers(criticLG, actionPath);
criticLG = addLayers(criticLG, commonPath);

% Connect the paths correctly
criticLG = connectLayers(criticLG,'relu2','concat/in1');
criticLG = connectLayers(criticLG,'action','concat/in2');
% Calculate the scale and bias needed to map the tanh output to the action range.
% This is the robust way to handle action scaling.
actorScale = (actInfo.UpperLimit - actInfo.LowerLimit)/2;
actorBias = (actInfo.UpperLimit + actInfo.LowerLimit)/2;
actorNetwork = [
    featureInputLayer(obsInfo.Dimension(1), 'Name', 'observation')
    fullyConnectedLayer(128, 'Name', 'fc1')
    reluLayer('Name', 'relu1')
    fullyConnectedLayer(128, 'Name', 'fc2')
    reluLayer('Name', 'relu2')
    fullyConnectedLayer(actInfo.Dimension(1), 'Name', 'actoroutput')
    tanhLayer('Name','tanh_layer')
    % Corrected scaling layer using the proper formula and dimensions
    scalingLayer('Name','scaling','Scale',actorScale,'Bias',actorBias)
];

% Create actor and critic representations for the DDPG agent
critic = rlQValueRepresentation(criticLG, obsInfo, actInfo,...
    'ObservationInputNames', {'observation'}, 'ActionInputNames', {'action'});
actor = rlDeterministicActorRepresentation(actorNetwork, obsInfo, actInfo,...
    'ObservationInputNames',{'observation'});
    
% Create the DDPG Agent
agentOptions = rlDDPGAgentOptions;
agentOptions.ExperienceBufferLength = 100000;
agentOptions.DiscountFactor = 0.90;
agentOptions.TargetSmoothFactor = 1e-3;
agentOptions.NoiseOptions.Variance = 0.5;
agentObj = rlDDPGAgent(actor, critic, agentOptions);

disp("DDPG Agent 'agentObj' has been created successfully with the corrected multi-input critic network.");