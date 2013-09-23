# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util 
class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"
  from game import Directions
  South = Directions.SOUTH
  West = Directions.WEST
  East = Directions.EAST
  North = Directions.NORTH

  state_stack= util.Stack()
  visited = set()
  parents = dict()
  direction = dict()
  path = list()
  state_stack.push(problem.getStartState())
  parents[problem.getStartState()] = (-1,-1);
  direction[problem.getStartState()] = "null";
  
  visited.add(problem.getStartState());
  while not state_stack.isEmpty():
    curr_state = state_stack.pop()
    children = problem.getSuccessors(curr_state)
   
    for child in children:
      if child[0] not in visited:
        if problem.isGoalState(child[0]):
          goal = child
          parents[child[0]]=curr_state
          direction[child[0]] = child[1]
          state_stack.empty() 
          break
        else:  
          state_stack.push(child[0])
          visited.add(child[0])
          parents[child[0]]=curr_state 
          direction[child[0]]=child[1]
  child = goal[0]
 
  while direction[child] != "null":
    path.append(direction[child])
    child = parents[child]
  path.reverse()
  print path
  return path
  "util.raiseNotDefined()"

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  "*** YOUR CODE HERE ***"
  from game import Directions
  South = Directions.SOUTH
  West = Directions.WEST
  East = Directions.EAST
  North = Directions.NORTH

  state_queue= util.Queue();
  visited = set()
  parents = dict()
  direction = dict()
  path = list()
  state_queue.push(problem.getStartState())
  parents[problem.getStartState()] = (-1,-1);
  direction[problem.getStartState()] = "null";
  
  visited.add(problem.getStartState());
  i=0
  while not state_queue.isEmpty():
    curr_state = state_queue.pop()
    children = problem.getSuccessors(curr_state)
   
    for child in children:
      print child, child[0]
      i = i+1
      if child[0] not in visited:
        if problem.isGoalState(child[0]):
          goal = child
          parents[child[0]]=curr_state
          direction[child[0]] = child[1]
          state_queue.empty() 
          break
        else:  
          state_queue.push(child[0])
          visited.add(child[0])
          parents[child[0]]=curr_state 
          direction[child[0]]=child[1]
  child = goal[0]
 
  while direction[child] != "null":
    path.append(direction[child])
    child = parents[child]
  path.reverse()
  print path
  return path
  util.raiseNotDefined()
      

def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"

  from game import Directions
  South = Directions.SOUTH
  West = Directions.WEST
  East = Directions.EAST
  North = Directions.NORTH

  state_queue= util.PriorityQueue();
  visited = set()
  parents = dict()
  direction = dict()
  cost = dict()
  path = list()
  state_queue.push(problem.getStartState(),0)
  parents[problem.getStartState()] = (-1,-1);
  direction[problem.getStartState()] = "null";
  
  cost[problem.getStartState()] = 0;
  i=0
  goalcost = float("inf")
  " print cost"
  while not state_queue.isEmpty():
    curr_state = state_queue.pop()
    if curr_state in visited:
      continue
    children = problem.getSuccessors(curr_state)
    visited.add(curr_state)
    if(cost[curr_state] > goalcost ):
      break
    for child in children:
      i = i+1
      if child[0] not in visited:
        if problem.isGoalState(child[0]):
          if(  cost[curr_state]+child[2] < goalcost):
            goal = child
            parents[child[0]]=curr_state
            direction[child[0]] = child[1]
            goalcost=child[2]+cost[curr_state]
          break
        else:  
          state_queue.push(child[0],child[2] +cost[curr_state])
          cost[child[0]] = child[2] + cost[curr_state]
          parents[child[0]]=curr_state
          direction[child[0]]=child[1]

  child = goal[0]
  while direction[child] != "null":
    path.append(direction[child])
    child = parents[child]
  path.reverse()
  return path

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  from game import Directions
  South = Directions.SOUTH
  West = Directions.WEST
  East = Directions.EAST
  North = Directions.NORTH

  state_queue= util.PriorityQueue();
  visited = set()
  parents = dict()
  direction = dict()
  cost = dict()
  path = list()
  state_queue.push(problem.getStartState(),0)
  parents[problem.getStartState()] = (-1,-1);
  direction[problem.getStartState()] = "null";
  
  cost[problem.getStartState()] = 0;
  i=0
  grid = problem.getStartState()[1]
  goalcost = float("inf")
  " print cost"
  while not state_queue.isEmpty():
    curr_state = state_queue.pop()
    if curr_state in visited:
      continue
    children = problem.getSuccessors(curr_state)
    visited.add(curr_state)
    if(cost[curr_state] +  heuristic(curr_state,problem)> goalcost ):
      break
    for child in children:
      i = i+1
      if child[0] not in visited:
        if problem.isGoalState(child[0]):
          if(  cost[curr_state]+child[2] < goalcost):
            goal = child
            parents[child[0]]=curr_state
            direction[child[0]] = child[1]
            goalcost=child[2]+cost[curr_state]
          break
        else:  
          state_queue.push(child[0],child[2] + heuristic(child[0],problem) +cost[curr_state])
          cost[child[0]] = child[2] + cost[curr_state]
          parents[child[0]]=curr_state
          direction[child[0]]=child[1]

  child = goal[0]
  while direction[child] != "null":
    path.append(direction[child])
    child = parents[child]
  path.reverse()
  "print patti"
  return path
  util.raiseNotDefined()
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
