import copy
import math
import random
from Position import Position
from King import King
from Pawn import Pawn
from Rook import Rook


class Node: 
    def __init__(self):
      self.parent = None
      self.children = []
      self.eval = 0
      self.wins = 0
      self.losses = 0
      self.visits = 0
      self.board = None
      self.move = None
      
    def uct_score(self, total_simulations, exploration_param=math.sqrt(2)):
      if self.visits == 0:
          return float('inf')  # Handle the division by zero case
      return (self.wins / self.visits) + exploration_param * math.sqrt(math.log(total_simulations) / self.visits)
    @profile
    def checkMove(self, board, piece, next_position):
      if (not board.checkMove(piece, next_position)):
        if (isinstance(piece, King) and piece.checkCastle(board, next_position)):
          board.castle(piece, next_position)
          board.increment_turn()
        elif isinstance(piece, Pawn) and piece.checkEn_Passant(board, next_position):
          board.En_Passant(piece, next_position)
          board.increment_turn()
        else:
          piece.move(board, next_position)
          board.increment_turn()
        board.updateBoardStateHistory()
    
    @profile
    def simulateGame(self):
      result = None
      simulationBoard = copy.deepcopy(self.board)
      while result is None:        
        if simulationBoard.turn_counter % 2 == 0 and simulationBoard.PlayerColor:
          piece = random.choice(simulationBoard.getTeamPieces())
          while len(piece.getPossibleMoves(simulationBoard)) == 0:
            piece = random.choice(simulationBoard.getTeamPieces())
          next_position = random.choice(list(piece.getPossibleMoves(simulationBoard)))
          
          self.checkMove(simulationBoard, piece, next_position)
          
        elif simulationBoard.turn_counter % 2 != 0 and not simulationBoard.PlayerColor:
          piece = random.choice(simulationBoard.getTeamPieces())
          while len(piece.getPossibleMoves(simulationBoard)) == 0:
            piece = random.choice(simulationBoard.getTeamPieces())
          next_position = random.choice(list(piece.getPossibleMoves(simulationBoard)))
          
          self.checkMove(simulationBoard, piece, next_position)
            
        else:
          piece = random.choice(simulationBoard.getEnemyPieces())
          while len(piece.getPossibleMoves(simulationBoard)) == 0:
            piece = random.choice(simulationBoard.getEnemyPieces())
          next_position = random.choice(list(piece.getPossibleMoves(simulationBoard)))
          
          self.checkMove(simulationBoard, piece, next_position)

        result = simulationBoard.checkEndGame()

      return result
    
    def backpropagate(self, result):
      # Update the node's statistics based on the result
      self.updateStatistics(result)
      
      # Propagate the result up to the parent (if there is a parent)
      if self.parent is not None:
        self.parent.backpropagate(result)
    
    def updateStatistics(self, result):
      # Update the node's statistics here
      # For example, increment visit count, update win/loss score, etc.
      self.visits += 1
      if result == 1:
          self.wins += 1
      elif result == -1:
          self.losses += 1    


class MCTS:
  
  def __init__(self, depth, board, AI_color):
    self.depth = depth
    self.board = board
    self.AI_color = AI_color
  @profile  
  def selection(self, node):
    if len(node.children) > 0:
      total_simulations = sum(child.visits for child in node.children)
      return max(node.children, key=lambda child: child.uct_score(total_simulations))
    
    return node
  @profile  
  def expansion(self, node):
    for piece in node.board.getEnemyPieces():#Enemy pieces are the enemy of the player pieces
      for next_position in piece.getPossibleMoves(node.board):
        expanded_node = Node()
        expanded_node.parent = node
        node.children.append(expanded_node) 
        expanded_node.board = copy.deepcopy(node.board)
        
        if (not node.board.checkMove(piece, next_position)):
          if ((isinstance(piece, King) or isinstance(piece, Rook)) and piece.checkCastle(expanded_node.board, next_position)):
            expanded_node.board.castle(piece, next_position)
            expanded_node.board.increment_turn()
            expanded_node.move = next_position
          elif isinstance(piece, Pawn) and piece.checkEn_Passant(expanded_node.board, next_position):
            expanded_node.board.En_Passant(piece, next_position)
            expanded_node.board.increment_turn()
            expanded_node.move = next_position
          else:
            piece.move(expanded_node.board, next_position)
            expanded_node.board.increment_turn()
            expanded_node.move = next_position
          expanded_node.board.updateBoardStateHistory()
  @profile
  def simulation(self, node):    
    for child_node in node.children:
      print("simulate")
      result = child_node.simulateGame()
      child_node.backpropagate(result)
    

    
    

    
      
    

      
    
    