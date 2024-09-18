# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        score = successorGameState.getScore()

        minFoodDistance = float('inf')
        for food in newFood.asList():
            distance = manhattanDistance(newPos, food)
            minFoodDistance = min(minFoodDistance, distance)

        minGhostDistance = min([manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates])

        for ghost in newGhostStates:
            if ghost.scaredTimer == 0 and ghost.getPosition() == newPos:
                return -float('inf')

        score += minGhostDistance / minFoodDistance

        if action == 'Stop':
            score -= 50

        return score

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def value(_gameState: GameState, _depth, _agentIndex, _action):

            _agentIndex %= _gameState.getNumAgents()

            if _gameState.isWin() or _gameState.isLose():
                return self.evaluationFunction(_gameState), _action

            if _agentIndex == 0:
                return max_value(_gameState, _depth, _agentIndex, _action)
            else:
                return min_value(_gameState, _depth, _agentIndex, _action)

        def max_value(_gameState: GameState, _depth, _agentIndex, _action):

            if _depth == 0:
                return self.evaluationFunction(_gameState), _action

            v = -float('inf')
            bestAction = None

            for legalAction in _gameState.getLegalActions(_agentIndex):
                successor = _gameState.generateSuccessor(_agentIndex, legalAction)

                current, _ = value(successor, _depth - 1, _agentIndex + 1, _action)
                v = max(current, v)

                if current == v:
                    bestAction = legalAction

            return v, bestAction

        def min_value(_gameState: GameState, _depth, _agentIndex, _action):

            v = float('inf')

            for legalAction in _gameState.getLegalActions(_agentIndex):
                successor = _gameState.generateSuccessor(_agentIndex, legalAction)

                current, _ = value(successor, _depth, _agentIndex + 1, _action)
                v = min(current, v)

            return v, _action

        _, action = value(gameState, self.depth, 0, None)

        return action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def value(_gameState: GameState, _depth, _agentIndex, _action, _alpha, _beta):

            _agentIndex %= _gameState.getNumAgents()

            if _gameState.isWin() or _gameState.isLose():
                return self.evaluationFunction(_gameState), _action

            if _agentIndex == 0:
                return max_value(_gameState, _depth, _agentIndex, _action, _alpha, _beta)
            else:
                return min_value(_gameState, _depth, _agentIndex, _action, _alpha, _beta)

        def max_value(_gameState: GameState, _depth, _agentIndex, _action, _alpha, _beta):

            if _depth == 0:
                return self.evaluationFunction(_gameState), _action

            v = -float('inf')
            bestAction = None

            for legalAction in _gameState.getLegalActions(_agentIndex):
                successor = _gameState.generateSuccessor(_agentIndex, legalAction)

                current, _ = value(successor, _depth - 1, _agentIndex + 1, _action, _alpha, _beta)
                v = max(current, v)

                if current == v:
                    bestAction = legalAction

                if v > _beta:
                    return v, bestAction

                _alpha = max(_alpha, v)

            return v, bestAction

        def min_value(_gameState: GameState, _depth, _agentIndex, _action, _alpha, _beta):

            v = float('inf')

            for legalAction in _gameState.getLegalActions(_agentIndex):
                successor = _gameState.generateSuccessor(_agentIndex, legalAction)

                current, _ = value(successor, _depth, _agentIndex + 1, _action, _alpha, _beta)
                v = min(current, v)

                if v < _alpha:
                    return v, _action

                _beta = min(_beta, v)

            return v, _action

        _, action = value(gameState, self.depth, 0, None, -float('inf'), float('inf'))

        return action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        def value(_gameState: GameState, _depth, _agentIndex, _action):

            _agentIndex %= _gameState.getNumAgents()

            if _gameState.isWin() or _gameState.isLose():
                return self.evaluationFunction(_gameState), _action

            if _agentIndex is 0:
                return max_value(_gameState, _depth, _agentIndex, _action)
            else:
                return exp_value(_gameState, _depth, _agentIndex, _action)

        def max_value(_gameState: GameState, _depth, _agentIndex, _action):

            if _depth == 0:
                return self.evaluationFunction(_gameState), _action

            v = -float('inf')
            bestAction = None

            for legalAction in _gameState.getLegalActions(_agentIndex):
                successor = _gameState.generateSuccessor(_agentIndex, legalAction)

                current, _ = value(successor, _depth - 1, _agentIndex + 1, _action)
                v = max(current, v)

                if current is v:
                    bestAction = legalAction

            return v, bestAction

        def exp_value(_gameState: GameState, _depth, _agentIndex, _action):

            v = 0
            p = 1 / len(_gameState.getLegalActions(_agentIndex))

            for legalAction in _gameState.getLegalActions(_agentIndex):
                successor = _gameState.generateSuccessor(_agentIndex, legalAction)

                current, _ = value(successor, _depth, _agentIndex + 1, _action)
                v += p * current

            return v, _action

        _, action = value(gameState, self.depth, 0, None)

        return action

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: Use almost the same evaluation function as q1, but add the capsuleCount in.
                 Since every time pacman beats the ghost, it gets additional points. As a result,
                 giving capusuleCount a relatively large weight so pacman will surely eat the capsule
                 every time goes through it, and then try to chase the ghost to beat it.
    """
    "*** YOUR CODE HERE ***"

    currentPosition = currentGameState.getPacmanPosition()
    ghostPositions = currentGameState.getGhostPositions()
    foodPositions = currentGameState.getFood().asList()
    currentScore = currentGameState.getScore()
    currentGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in currentGhostStates]

    foodCount = len(foodPositions)
    capsuleCount = len(currentGameState.getCapsules())

    minFoodDistance = float('inf')
    if len(foodPositions) != 0:
        minFoodDistance = min([manhattanDistance(currentPosition, food) for food in foodPositions])

    minGhostDistance = float('inf')
    for ghostPosition in ghostPositions:
        ghostDistance = manhattanDistance(currentPosition, ghostPosition)
        minGhostDistance = min(minGhostDistance, ghostDistance)

    error = 0
    if minGhostDistance <= 2 :
        error = -float('inf')

    if sum(newScaredTimes) == 0:
        features = [currentScore, minGhostDistance / minFoodDistance, foodCount, capsuleCount, error]
        weights = [100, 10, -100, -10000, 1]
        totalScore = sum([feature * weight for feature, weight in zip(features, weights)])
    else:
        features = [currentScore, minGhostDistance, 1 / minFoodDistance, foodCount]
        weights = [100, -10, 10 , -50]
        totalScore = sum([feature * weight for feature, weight in zip(features, weights)])

    return totalScore

# Abbreviation
better = betterEvaluationFunction

"Reference: Chatgpt for syntax learning and algorithms implementing."