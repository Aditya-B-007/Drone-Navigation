import math
class Node:
    def __init__(self,parent=None,position=None):
        self.parent=parent
        self.position=position
        self.g=0
        self.h=0
        self.f=0
    def __eq__(self,other):
        return self.position==other.position
def Searcher(maze,start,end):
    start_node = Node(None,start)
    end_node = Node(None,end)
    open_list = []
    closed_list = []
    open_list.append(start_node)

    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]
        children = []
        for new_position in [(0,-1),(0,1),(-1,0),(1,0)]:
            node_position=(current_node.position[0]+new_position[0],current_node.position[1]+new_position[1])
            if not (0 <= node_position[0] < len(maze) and 0 <= node_position[1] < len(maze[0])):
                continue
            if maze[node_position[0]][node_position[1]] != 0:
                continue
            new_node = Node(current_node,node_position)
            children.append(new_node)
        for child in children:
            if child in closed_list:
                continue
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h
            if any(open_node.f <= child.f and open_node.position == child.position for open_node in open_list):
                continue
            open_list.append(child)
    return None