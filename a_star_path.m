function path = a_star_path(map, start_coords, end_coords)
    [rows, cols] = size(map);
    node_map = Inf(rows, cols, 3); % Dim 3: [g_cost, h_cost, f_cost]
    parent_map = zeros(rows, cols, 2); % Stores parent [row, col] of each node
    h_cost = sqrt((end_coords(1) - start_coords(1))^2 + (end_coords(2) - start_coords(2))^2);
    start_node_g_cost = 0;
    start_node_f_cost = start_node_g_cost + h_cost;
    node_map(start_coords(1), start_coords(2), :) = [start_node_g_cost, h_cost, start_node_f_cost];
    open_list = [start_node_f_cost, start_node_g_cost, start_coords(1), start_coords(2)];
    closed_list = false(rows, cols);

    while ~isempty(open_list)
        [~, idx] = min(open_list(:,1));
        current_node = open_list(idx,:);
        open_list(idx,:) = [];
        
        row = current_node(3);
        col = current_node(4);
        if row == end_coords(1) && col == end_coords(2)
            break;
        end
        
        closed_list(row, col) = true;
        for dr = -1:1
            for dc = -1:1
                if dr == 0 && dc == 0
                    continue;
                end
                
                new_row = row + dr;
                new_col = col + dc;
                
           
                if new_row < 1 || new_row > rows || new_col < 1 || new_col > cols ...
                   || map(new_row, new_col) == 1 || closed_list(new_row, new_col)
                    continue;
                end
                move_cost = sqrt(dr^2 + dc^2); 
                g_cost = current_node(2) + move_cost;
                h_cost = sqrt((new_row - end_coords(1))^2 + (new_col - end_coords(2))^2);
                f_cost = g_cost + h_cost;
                
                % If new path to neighbor is shorter or neighbor is unvisited
                if g_cost < node_map(new_row, new_col, 1)
                    node_map(new_row, new_col, :) = [g_cost, h_cost, f_cost];
                    parent_map(new_row, new_col, :) = [row, col];
                    
                    % Add to open list if not already there
                    is_in_open = false;
                    for k = 1:size(open_list, 1)
                        if open_list(k,3) == new_row && open_list(k,4) == new_col
                            is_in_open = true;
                            open_list(k,:) = [f_cost, g_cost, new_row, new_col];
                            break;
                        end
                    end
                    if ~is_in_open
                        open_list = [open_list; f_cost, g_cost, new_row, new_col];
                    end
                end
            end
        end
    end
    
    % Reconstruct path from goal to start
    path = [];
    current_pos = end_coords;
    while ~(current_pos(1) == start_coords(1) && current_pos(2) == start_coords(2))
        path = [current_pos; path];
        parent_row = parent_map(current_pos(1), current_pos(2), 1);
        parent_col = parent_map(current_pos(1), current_pos(2), 2);
        
        if parent_row == 0 % Path not found
            path = [];
            return;
        end
        current_pos = [parent_row, parent_col];
    end
    path = [start_coords; path];
end