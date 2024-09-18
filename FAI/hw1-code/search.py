# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
# Modified by Shang-Tse Chen (stchen@csie.ntu.edu.tw) on 03/03/2022

"""
This is the main entry point for HW1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,fast)

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_corner": astar_corner,
        "astar_multi": astar_multi,
        "fast": fast,
    }.get(searchMethod)(maze)

def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here

    queue = []
    visited = []
    queue.append((maze.getStart() , [maze.getStart()]))
    visited.append(maze.getStart())

    while queue:
        (currentRow , currentCol) , path = queue.pop(0)

        visited.append((currentRow , currentCol))

        if (currentRow , currentCol) in maze.getObjectives():
            return path

        for nextPosition in maze.getNeighbors(currentRow , currentCol):
            if maze.isValidMove(currentRow , currentCol) and (nextPosition) not in visited:
                queue.append((nextPosition , path + [nextPosition]))
                visited.append(nextPosition)

    return None

def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here

    from queue import PriorityQueue

    def Heuristic(_current , _objectives):

        maxDistance = 0

        if not _objectives:
            return 0

        for _objective in _objectives:
            distance = abs(_current[0] - _objective[0]) + abs(_current[1] - _objective[1])
            maxDistance = max(maxDistance , distance)

        return maxDistance

    start = maze.getStart()
    objectives = maze.getObjectives()

    edge = PriorityQueue()
    edge.put((0 , start))

    forwardCost = {}
    forwardCost[start] = 0
    backwardPath = {}
    backwardPath[start] = None

    while not edge.empty():
        currentCost , current = edge.get()

        if current in objectives:
            objectives.remove(current)
            if len(objectives) == 0:
                break

        for next in maze.getNeighbors(current[0] , current[1]):
            newCost = currentCost + 1

            if next not in forwardCost or newCost < forwardCost[next]:
                forwardCost[next] = newCost
                priority = newCost + Heuristic(next , objectives)
                edge.put((priority , next))
                backwardPath[next] = current

    path = []

    while current != start:
        path.append(current)
        current = backwardPath[current]

    path.append(start)
    path.reverse()

    return path

def astar_corner(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are four corner objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
        """
    # TODO: Write your code here

    from queue import PriorityQueue

    def Heuristic(_currentState):

        _position , _objectives = _currentState
        maxDistance = 0

        if not _objectives:
            return 0

        for _objective in _objectives:
            distance = abs(_position[0] - _objective[0]) + abs(_position[1] - _objective[1])
            maxDistance = max(maxDistance , distance)

        return maxDistance

    initialState = (maze.getStart() , frozenset(maze.getObjectives()))

    edge = PriorityQueue()
    edge.put((0 , initialState))

    forwardCost = {}
    forwardCost[initialState] = 0
    backwardPath = {}
    backwardPath[initialState] = None

    while not edge.empty():
        currentCost , currentState = edge.get()
        position , objectives = currentState

        if not objectives:
            break

        for nextPosition in maze.getNeighbors(position[0] , position[1]):
            if nextPosition in objectives:
                nextObjectives = objectives - {nextPosition}
            else:
                nextObjectives = objectives

            nextState = (nextPosition , nextObjectives)
            newCost = forwardCost[currentState] + 1

            if nextState not in forwardCost or newCost < forwardCost[nextState]:
                forwardCost[nextState] = newCost
                priority = newCost + Heuristic(nextState)
                edge.put((priority , nextState))
                backwardPath[nextState] = currentState

    path = []

    while currentState != initialState:
        path.append(currentState[0])
        currentState = backwardPath[currentState]

    path.append(maze.getStart())
    path.reverse()

    return path

def astar_multi(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here

    from queue import PriorityQueue

    def prebfs(maze , start):

        queue = []
        visited = []
        _distance = {}
        queue.append((start , [start]))
        visited.append(start)

        while queue:
            (currentRow , currentCol) , path = queue.pop(0)

            visited.append((currentRow , currentCol))

            for nextPosition in maze.getNeighbors(currentRow , currentCol):
                if maze.isValidMove(currentRow , currentCol) and (nextPosition) not in visited:
                    _distance[nextPosition] = len(path)
                    queue.append((nextPosition , path + [nextPosition]))
                    visited.append(nextPosition)

        _distance[start] = 0

        return _distance

    def Modify(_position , _objectives , _currentH1 , _currentH2):

        maxDistance = 0

        for _objective in _objectives:
            for __objective in _objectives:
                if distance[_objective][__objective] >= maxDistance:
                    maxDistance = distance[_objective][__objective]
                    _currentH1 = _objective
                    _currentH2 = __objective

        return (_position , _objectives , _currentH1 , _currentH2)

    def Heuristic(_currentState):

        _position , _objectives , _currentH1 , _currentH2 = _currentState

        return distance[_currentH1][_currentH2] + min(distance[_currentH1][_position] , distance[_currentH2][_position])

    distance = {}

    for objective in maze.getObjectives():
        distance[objective] = prebfs(maze , objective)

    initialH1 = maze.getObjectives()[0]
    initialH2 = maze.getObjectives()[0]

    initialState = Modify(maze.getStart() , frozenset(maze.getObjectives()) , initialH1 , initialH2)

    edge = PriorityQueue()
    edge.put((0 , initialState))

    forwardCost = {}
    forwardCost[initialState] = 0
    backwardPath = {}
    backwardPath[initialState] = None

    while not edge.empty():
        currentCost , currentState = edge.get()
        position , objectives , currentH1 , currentH2 = currentState

        if not objectives:
            break

        for nextPosition in maze.getNeighbors(position[0] , position[1]):
            if nextPosition in objectives:
                nextObjectives = objectives - {nextPosition}
            else:
                nextObjectives = objectives

            nextState = Modify(nextPosition , nextObjectives , currentH1 , currentH2)
            newCost = forwardCost[currentState] + 1

            if nextState not in forwardCost or newCost < forwardCost[nextState]:
                forwardCost[nextState] = newCost
                priority = newCost + Heuristic(nextState)
                edge.put((priority , nextState))
                backwardPath[nextState] = currentState

    path = []

    while currentState != initialState:
        path.append(currentState[0])
        currentState = backwardPath[currentState]

    path.append(maze.getStart())
    path.reverse()

    return path

def fast(maze):
    """
    Runs suboptimal search algorithm for part 4.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here\

    path = []
    visited =[]
    start = maze.getStart()
    objectives = maze.getObjectives()

    def dfs(current):
        path.append(current)
        visited.append(current)

        if current in objectives:
            objectives.remove(current)

        if not objectives:
            return None

        for next in maze.getNeighbors(current[0] , current[1]):
            if next not in visited:
                dfs(next)
                if not objectives:
                    return None
                else:
                    path.append(current)

        return None

    dfs(start)

    return path

'''
    Reference :
    Chatgpt for Syntax Learning, Debugging, Alogrithms Implementing
    Discussing with friends for Code Optimization
    Internet for Finding Better Heuristic
    Some Reference Websites(Not all be implemented in hw1):
    https://stackoverflow.com/questions/9994913/pacman-what-kinds-of-heuristics-are-mainly-used
    https://www.redblobgames.com/pathfinding/heuristics/differential.html?fbclid=IwAR3IV2FpLuVpT3POXcHunpbqsETNBMFIjr0p0hSe-NQ7Eosz1NfUZPa2bTw
    https://www.microsoft.com/en-us/research/publication/computing-the-shortest-path-a-search-meets-graph-theory/?fbclid=IwAR06T9oatHMIS5jxUMOnLkv3lBAFSSFHVVVztQKv1AucCCeEPNv-yEIA3Oc
'''