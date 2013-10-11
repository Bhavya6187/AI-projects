# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util, sys

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        if successorGameState.isWin() :   return sys.maxint 
        if successorGameState.isLose() :  return -sys.maxint
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        foodlist = newFood.asList()
        mini = float("inf")
        GhostPositions=[Ghost.getPosition() for Ghost in newGhostStates];
        ghostdist = 100000; 
        for state in newGhostStates:
          #If timer is not 0, pacman does not consider this ghost
          if(ghostState.scaredTimer <= 0):
            ghostdist = abs(state.getPosition()[1] - newPos[1]) + abs(state.getPosition()[0] - newPos[0])
            if(ghostdist < mini):
              mini = ghostdist;
          #If ghost is too close then leave everything and get away
        if(ghostdist <= 2 ):
          return -float("inf")
        
        mini = float("inf")
        for coord in foodlist:
          tmpdist = abs(newPos[0]-coord[0]) + abs(newPos[1]-coord[1])
          if(mini >= tmpdist):
            mini = tmpdist 
            minicoord = coord
        #the successor score penalises for staying idle, rest of it considers minimum dist and dis from ghost
        return successorGameState.getScore()+(1/(mini*ghostdist))

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    # Max function of Min_Max i.e. Pacman
    def Max_Pacman(self, gameState, depth):
      
      #default action is STOP
      final_action = Directions.STOP
      #if depth is zero and Win or Lose State we return the direction
      if depth==0 or gameState.isWin() or gameState.isLose() :
        return [self.evaluationFunction(gameState), Directions.STOP]
      legalMoves = gameState.getLegalActions(0)
      # Remove "STOP action
      actions = [action for action in legalMoves if action != 'Stop' ]
      maxim = float("-inf")
      for action in actions:
        # calling the Min_Ghost with a reduced depth
        score = self.Min_Ghost(gameState.generateSuccessor(0,action), depth-1)
        if(score[0] > maxim):
          maxim = score[0]
          final_action = action
      return [maxim, final_action]


    # Min function of Min_Max i.e. Ghosts
    def Min_Ghost(self, gameState, depth):
      
      final_action = Directions.STOP
      if depth==0 or gameState.isWin() or gameState.isLose() :
        return [self.evaluationFunction(gameState), Directions.STOP]
      ghostAgents = gameState.getNumAgents()
      minim = float("inf")
      # loop for all the ghosts
      for i in range(1,gameState.getNumAgents()-1):
        legalMoves = gameState.getLegalActions(i)
        # Remove "STOP action
        actions = [action for action in legalMoves if action != 'Stop' ]
        for action in actions:
          # calling the Max_Ghost with same depth to allow for all ghosts to play their turn
          score =  self.Max_Pacman(gameState.generateSuccessor(i,action), depth)
          if(score[0] < minim):
            minim = score[0]
            final_action = action
      #returning the minimum score
      return [minim, final_action]

    def getAction(self, gameState):
      """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
          Returns a list of legal actions for an agent
          agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
          Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
          Returns the total number of agents in the game
      """
      "*** YOUR CODE HERE ***"
      #print self.Max_Pacman(gameState, self.depth)[0], self.Max_Pacman(gameState, self.depth)[1]
      return self.Max_Pacman(gameState, self.depth)[1]
      util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def Max_Pacman(self, gameState, depth, alpha, beta):

      final_action = Directions.STOP
      if depth==0 or gameState.isWin() or gameState.isLose()  :
        return [self.evaluationFunction(gameState), Directions.STOP]
      legalMoves = gameState.getLegalActions(0)
      # Remove "STOP action
      actions = [action for action in legalMoves if action != 'Stop' ]
      maxim = float("-inf")
      for action in actions:
        score = self.Min_Ghost(gameState.generateSuccessor(0,action), depth-1, alpha, beta)
        #changing alpha beta pruning 
        if(score[0] > maxim):
          maxim = score[0]
          final_action = action
        if maxim >= beta:
          return [maxim, final_action]
        alpha = max(alpha, maxim)
      return [maxim, final_action]


    def Min_Ghost(self, gameState, depth, alpha, beta):
      
      final_action = Directions.STOP
      if depth==0 or gameState.isWin() or gameState.isLose() :
        return [self.evaluationFunction(gameState), Directions.STOP]
      ghostAgents = gameState.getNumAgents()
      minim = float("inf")
      for i in range(1,gameState.getNumAgents()-1):
        legalMoves = gameState.getLegalActions(i)
        # Remove "STOP action
        actions = [action for action in legalMoves if action != 'Stop' ]
        for action in actions:
          score =  self.Max_Pacman(gameState.generateSuccessor(i,action), depth, alpha, beta)
          #changing alpha beta pruning 
          if(score[0] < minim):
            minim = score[0]
            final_action = action
          if minim <= alpha:
            return [minim, final_action]
          beta = min(beta, minim)
      return [minim, final_action]

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #print self.Max_Pacman(gameState, self.depth, float("-inf"), float("inf"))[0] 
        #print self.Max_Pacman(gameState, self.depth, float("-inf"), float("inf"))[1]
        return self.Max_Pacman(gameState, self.depth, float("-inf"), float("inf"))[1]
        util.raiseNotDefined()


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

