# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
# Modified by Rahul Kunji (rahulsk2@illinois.edu) on 01/16/2019

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""


# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
import queue
import copy


class state:
    def __init__(self, row, col, cost, objectives=None):
        self.row = row
        self.col = col
        self.cost = cost
        self.parent = None
        self.objectives = objectives    
    def __repr__(self):
        if self.objectives:
            self.objectives.sort()
            return str(self.row)+","+str(self.col)+","+str(self.objectives)
        else:
            return str(self.row)+","+str(self.col)
    def __hash__(self):
        return hash(self.__repr__())
    def __eq__(self, other):
        return self.__repr__() == other.__repr__()
    def __lt__(self, other):
        return self.cost<other.cost

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
        "astar_for_ec": astar_for_ec
    }.get(searchMethod)(maze)

def mhtdis(state_row, state_col, objectives):
    if len(objectives) == 1:
        obj_row, obj_col = objectives[0]
        distance = abs(state_row-obj_row) + abs(state_col-obj_col)
    else:
        dis_list = []
        for obj in objectives:
            obj_row, obj_col = obj
            distance = abs(state_row-obj_row) + abs(state_col-obj_col)
            dis_list.append(distance)
        dis_list.sort()
        distance = dis_list[0]
    return distance


def bfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    startr, startc = maze.getStart()
    #print("start loc",startr, " ", startc)
    #initialize frontier, explored_set, path_set, num_states_explored
    frontier = queue.Queue()
    start_state = state(startr, startc, 0)

    frontier.put(start_state)

    explored_set = {}
    explored_set[(maze.getStart())] = True

    objective_set = maze.getObjectives()
    path_set = []
    num_states_explored = 0
    while (True):
        cur_state = frontier.get()
        #whenever we find the all the dots, break out the loop to draw the path
        if(len(objective_set) == 0):
            break
        # check if any dot is located at the current location
        for obj_loc in objective_set:
            #if we eat a new dot, delete all the marks we made on explored_set,
            #and also clear the queue of frontier
            if ((cur_state.row, cur_state.col) == obj_loc):
                objective_set.remove(obj_loc)
                for elem in explored_set:
                    explored_set[elem] = False
                num_states_explored += len(explored_set)
                with frontier.mutex:
                    frontier.queue.clear()
                frontier.put(cur_state)

        if(len(objective_set) == 0):
            break
        #put new states into the frontier by find the neighbors of the current state
        for neighbors in maze.getNeighbors(cur_state.row, cur_state.col):
            #if the neighbor is not in the explored_set yet,
            #we add the neighbor into the explored_set and also set the parent state
            if (explored_set.get(neighbors) != True):
                explored_set[neighbors]= True
                next_state = state(neighbors[0], neighbors[1], cur_state.cost +1)
                next_state.parent = cur_state
                frontier.put(next_state)
            else:
                continue
    #final_cost = cur_state.cost
    while(True):
        if(cur_state == None):
            break
        else:
            #insert the states to the beginning of the queue,
            #and find the parent state of the current state in each move
            path_set.insert(0, (cur_state.row, cur_state.col))
            cur_state = cur_state.parent

    return path_set, num_states_explored


def dfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    startr, startc = maze.getStart()
    #print("start loc",startr, " ", startc)
    #initialize frontier, explored_set, path_set, num_states_explored
    frontier = queue.LifoQueue()
    start_state = state(startr, startc, 0)

    frontier.put(start_state)

    explored_set = {}
    explored_set[(maze.getStart())] = True

    objective_set = maze.getObjectives()
    path_set = []
    num_states_explored = 0
    while (True):
        cur_state = frontier.get()
        #whenever we find the all the dots, break out the loop to draw the path
        if(len(objective_set) == 0):
            break
        # check if any dot is located at the current location
        for obj_loc in objective_set:
            #if we eat a new dot, delete all the marks we made on explored_set,
            #and also clear the queue of frontier
            if ((cur_state.row, cur_state.col) == obj_loc):
                objective_set.remove(obj_loc)
                for elem in explored_set:
                    explored_set[elem] = False
                num_states_explored += len(explored_set)
                with frontier.mutex:
                    frontier.queue.clear()
                frontier.put(cur_state)

        if(len(objective_set) == 0):
            break
        #put new states into the frontier by find the neighbors of the current state
        for neighbors in maze.getNeighbors(cur_state.row, cur_state.col):
            #if the neighbor is not in the explored_set yet,
            #we add the neighbor into the explored_set and also set the parent state
            if (explored_set.get(neighbors) != True):
                explored_set[neighbors]= True
                next_state = state(neighbors[0], neighbors[1], cur_state.cost +1)
                next_state.parent = cur_state
                frontier.put(next_state)
            else:
                continue
    #final_cost = cur_state.cost
    while(True):
        if(cur_state == None):
            break
        else:
            #insert the states to the beginning of the queue,
            #and find the parent state of the current state in each move
            path_set.insert(0, (cur_state.row, cur_state.col))
            cur_state = cur_state.parent

    return path_set, num_states_explored


def greedy(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    startr, startc = maze.getStart()
    #print("start loc",startr, " ", startc)
    #initialize frontier, explored_set, path_set, num_states_explored
    frontier = queue.PriorityQueue()
    objective_set = maze.getObjectives()
    start_state = state(startr, startc, 0)
    start_rank = mhtdis(startr, startc, objective_set)


    frontier.put((start_rank, start_state))

    explored_set = {}
    explored_set[(maze.getStart())] = True

    
    path_set = []
    num_states_explored = 0
    while (True):
        cur_state = frontier.get()[1]
        #whenever we find the all the dots, break out the loop to draw the path
        if(len(objective_set) == 0):
            break
        # check if any dot is located at the current location
        for obj_loc in objective_set:
            #if we eat a new dot, delete all the marks we made on explored_set,
            #and also clear the queue of frontier
            if ((cur_state.row, cur_state.col) == obj_loc):
                objective_set.remove(obj_loc)
                for elem in explored_set:
                    explored_set[elem] = False
                num_states_explored += len(explored_set)
                with frontier.mutex:
                    frontier.queue.clear()
                if(len(objective_set)!=0):
                    start_rank = mhtdis(cur_state.row, cur_state.col, objective_set)
                    cur_state = state(cur_state.row, cur_state.col, objective_set)
                    frontier.put((start_rank, cur_state))

        if(len(objective_set) == 0):
            break
        #put new states into the frontier by find the neighbors of the current state
        for neighbors in maze.getNeighbors(cur_state.row, cur_state.col):
            #if the neighbor is not in the explored_set yet,
            #we add the neighbor into the explored_set and also set the parent state
            if (explored_set.get(neighbors) != True):
                explored_set[neighbors]= True
                next_state = state(neighbors[0], neighbors[1], cur_state.cost +1)
                next_state.parent = cur_state
                state_rank = mhtdis(neighbors[0], neighbors[1], objective_set)
                #print(state_rank)
                #print(next_state)
                frontier.put((state_rank, next_state))
            else:
                continue
        #print("newstate")
    #final_cost = cur_state.cost
    while(True):
        if(cur_state == None):
            break
        else:
            #insert the states to the beginning of the queue,
            #and find the parent state of the current state in each move
            path_set.insert(0, (cur_state.row, cur_state.col))
            #print(cur_state.row, cur_state.col)
            cur_state = cur_state.parent


    return path_set, num_states_explored


def astar(maze):
    if(len(maze.getObjectives())==1):
        start = maze.getStart()
        end = maze.getObjectives()
        return astar_onedot(start, end, maze)

    frontier = queue.PriorityQueue()
    frontier_dic = {}
    objective_set = maze.getObjectives()
    startr, startc = maze.getStart()
    start_state = state(startr, startc, 0, objective_set)
    explored_set = {}   
    edges={}
    mst_weights_dict = {}

    for check1 in objective_set:
        for check2 in objective_set:
            if(check1 != check2):
                path_line, exp = astar_onedot(check1, [check2], maze)
                lengthofpath = len(path_line)
                edges[(check1,check2)] = lengthofpath

    objective_set.sort()
    mst_weights_dict[str(objective_set)] = get_MST(objective_set,edges, maze)
    start_rank = mhtdis(startr, startc, objective_set)+mst_weights_dict[str(objective_set)]
    frontier.put((start_rank, start_state))
    while (True):
        cur_state = frontier.get()[1]
        #whenever we find the all the dots, break out the loop to draw the path
        if (cur_state.row, cur_state.col) in cur_state.objectives:
            left_objectives = copy.deepcopy(cur_state.objectives)
            left_objectives.remove((cur_state.row, cur_state.col))
            left_objectives.sort()
        else:
            left_objectives = copy.deepcopy(cur_state.objectives)
            left_objectives.sort()
        #print("eww",left_objectives,"row ",cur_state.row, "col ",cur_state.col)
        if len(left_objectives) == 0 or left_objectives == []:
            final = cur_state
            break 
        for neighbors in maze.getNeighbors(cur_state.row, cur_state.col):
            #if the neighbor is not in the explored_set yet,
            #we add the neighbor into the explored_set and also set the parent state
            next_state = state(neighbors[0], neighbors[1], cur_state.cost + 1, left_objectives)

            next_state.parent = cur_state
            if mst_weights_dict.get(str(next_state.objectives)):
                mstpathcost = mst_weights_dict[str(next_state.objectives)]
            else:
                mstpathcost = get_MST(next_state.objectives, edges , maze)
                mst_weights_dict[str(next_state.objectives)] = mstpathcost
            hcost = mhtdis(neighbors[0], neighbors[1],left_objectives)+mstpathcost
            state_rank = next_state.cost+hcost
            if (next_state not in explored_set):
                explored_set[next_state] = cur_state
                frontier.put((state_rank, next_state))
            else:
                parent_state = explored_set[next_state]
                if parent_state.cost > cur_state.cost:
                    next_state.cost = cur_state.cost + 1
                    frontier.put((hcost,next_state))
                    explored_set[next_state] = cur_state
    # print("reached here")
    return backtracking(start_state, final, explored_set), len(explored_set)

def backtracking(s, e, explored_set):
    ret = []
    tmp = e
    while(tmp != s):
        ret.insert(0, (tmp.row,tmp.col))
        tmp = explored_set[tmp]
    ret.insert(0, (s.row,s.col))
    return ret


    # while(True):
    #     if(cur_state == None):
    #         break
    #     else:
    #         #insert the states to the beginning of the queue,
    #         #and find the parent state of the current state in each move
    #         path_set.insert(0, (cur_state.row, cur_state.col))
    #         #print(cur_state.row, cur_state.col)
    #         cur_state = cur_state.parent


    return path_set, num_states_explored



    return [], 0


#def mst(dots, onestepdots, lengthofpath, maze):

def get_MST(objs, pathcost, maze):
    if (len(objs) != 0):
        start = objs[0]
        visited = {}
        visited[start] = True
        mst = 0
        while True:
            if len(visited) == len(objs):
                break
            disq = queue.PriorityQueue()
            for dot1 in visited:
                for dot2 in objs:
                    if visited.get(dot2) != True:
                        dis_dots = (dot1,dot2)
                        disq.put((pathcost[dis_dots]-1,dis_dots))
            new_dis_dots = disq.get()
            visited[new_dis_dots[1][1]] = True
            mst = mst+ new_dis_dots[0]
    return mst


def astar_onedot(start, end, maze):
    # TODO: Write your code here
    # return path, num_states_explored
    startr, startc = start
    #print("start loc",startr, " ", startc)
    #initialize frontier, explored_set, path_set, num_states_explored
    frontier = queue.PriorityQueue()
    frontier_dic = {}
    objective_set = end
    
    start_state = state(startr, startc, 0)
    start_rank = mhtdis(startr, startc, objective_set)
    frontier.put((start_rank, start_state))
    explored_set = {}
    explored_set[(maze.getStart())] = True   
    path_set = []
    num_states_explored = 0
    while (True):
        cur_state = frontier.get()[1]
        #whenever we find the all the dots, break out the loop to draw the path

        if(len(objective_set) == 0):
            break

        for obj_loc in objective_set:
            #if we eat a new dot, delete all the marks we made on explored_set,
            #and also clear the queue of frontier
            if ((cur_state.row, cur_state.col) == obj_loc):
                objective_set.remove(obj_loc)
                for elem in explored_set:
                    explored_set[elem] = False
                num_states_explored += len(explored_set)
                with frontier.mutex:
                    frontier.queue.clear()
                if(len(objective_set)!=0):
                    start_rank = mhtdis(cur_state.row, cur_state.col, objective_set)
                    cur_state = state(cur_state.row, cur_state.col, objective_set)
                    frontier.put((start_rank, cur_state))
        if(len(objective_set) == 0):
            break
        #put new states into the frontier by find the neighbors of the current state
        for neighbors in maze.getNeighbors(cur_state.row, cur_state.col):
            #if the neighbor is not in the explored_set yet,
            #we add the neighbor into the explored_set and also set the parent state
            if (explored_set.get(neighbors) != True):
                explored_set[neighbors]= True
                cost = cur_state.cost
                next_state = state(neighbors[0], neighbors[1], cur_state.cost +1)
                next_state.parent = cur_state
                state_rank = cost+mhtdis(neighbors[0], neighbors[1], objective_set)
                #print(state_rank)
                #print(next_state)
                frontier.put((state_rank, next_state))
                frontier_dic[neighbors] =int(state_rank)
            else:

                if(len(frontier_dic) != 0):
                    cost = cur_state.cost
                    next_state = state(neighbors[0], neighbors[1], cur_state.cost +1)
                    new_rank = cost+mhtdis(neighbors[0], neighbors[1], objective_set)
                    old_rank = frontier_dic.get((neighbors))
                    if(old_rank == None):
                        continue
                    #print(old_rank, "here")
                    #print(frontier_dic)
                    #print(frontier_dic[neighbors])
                    if(int(old_rank) > new_rank):
                        print("here")
                        frontier.put((new_rank, next_state))
        #print("here")

        #print("newstate")
    #final_cost = cur_state.cost

    while(True):
        if(cur_state == None):
            break
        else:
            #insert the states to the beginning of the queue,
            #and find the parent state of the current state in each move
            path_set.insert(0, (cur_state.row, cur_state.col))
            #print(cur_state.row, cur_state.col)
            cur_state = cur_state.parent


    return path_set, num_states_explored

def astar_for_ec(maze):
    if(len(maze.getObjectives())==1):
        start = maze.getStart()
        end = maze.getObjectives()
        return astar_onedot(start, end, maze)

    frontier = queue.PriorityQueue()
    frontier_dic = {}
    objective_set = maze.getObjectives()
    startr, startc = maze.getStart()
    start_state = state(startr, startc, 0, objective_set)
    explored_set = {}   
    edges={}
    mst_weights_dict = {}

    for check1 in objective_set:
        for check2 in objective_set:
            if(check1 != check2):
                #calculating the distance with astar cost too much time, especially when we have a lots of the dots
                #the time increases with n squre,
                #Hence, when we are dealing with the the example maze given for ec,
                #we should reduce the time on this part, and mht distance is easy to calculate, and in most cases,
                #it gives a pretty good assumption
                path_line= mhtdis(check1[0], check1[1], [check2])

                lengthofpath = path_line
                edges[(check1,check2)] = lengthofpath

    objective_set.sort()
    mst_weights_dict[str(objective_set)] = get_MST(objective_set,edges, maze)
    start_rank = mhtdis(startr, startc, objective_set)+mst_weights_dict[str(objective_set)]
    frontier.put((start_rank, start_state))
    while (True):
        cur_state = frontier.get()[1]
        #whenever we find the all the dots, break out the loop to draw the path
        if (cur_state.row, cur_state.col) in cur_state.objectives:
            left_objectives = copy.deepcopy(cur_state.objectives)
            left_objectives.remove((cur_state.row, cur_state.col))
            left_objectives.sort()
        else:
            left_objectives = copy.deepcopy(cur_state.objectives)
            left_objectives.sort()
        #print("eww",left_objectives,"row ",cur_state.row, "col ",cur_state.col)
        if len(left_objectives) == 0 or left_objectives == []:
            final = cur_state
            break 
        for neighbors in maze.getNeighbors(cur_state.row, cur_state.col):
            #if the neighbor is not in the explored_set yet,
            #we add the neighbor into the explored_set and also set the parent state
            next_state = state(neighbors[0], neighbors[1], cur_state.cost + 1, left_objectives)

            next_state.parent = cur_state
            if mst_weights_dict.get(str(next_state.objectives)):
                mstpathcost = mst_weights_dict[str(next_state.objectives)]
            else:
                mstpathcost = get_MST(next_state.objectives, edges , maze)
                mst_weights_dict[str(next_state.objectives)] = mstpathcost
            hcost = mhtdis(neighbors[0], neighbors[1],left_objectives)+mstpathcost
            state_rank = next_state.cost+hcost
            if (next_state not in explored_set):
                explored_set[next_state] = cur_state
                frontier.put((state_rank, next_state))
            else:
                parent_state = explored_set[next_state]
                if parent_state.cost > cur_state.cost:
                    next_state.cost = cur_state.cost + 1
                    frontier.put((hcost,next_state))
                    explored_set[next_state] = cur_state
    # print("reached here")
    return backtracking(start_state, final, explored_set), len(explored_set)


