import copy
import math
import random
from King import King
from Pawn import Pawn


class Node: 
    def __init__(self, board, piece_position, move, parent_node, color):
      self.parent = parent_node
      self.color = color
      self.children = []
      self.eval = 0
      self.wins = 0
      self.losses = 0
      self.visits = 0
      self.board = board
      self.piece_position = piece_position
      self.move = move
      self.depth = parent_node.depth + 1 if parent_node is not None else 0
      
      if self.parent:
        piece = self.board.getCell(self.piece_position[0], self.piece_position[1]).piece
        self.board.checkFiftyMoveRule(piece, move)
        promotion_row = 0 if piece.color == self.board.PlayerColor else 7
        self.board.movePiece(piece, move)
        if isinstance(piece, Pawn) and move[0]==promotion_row:
          board.promote(piece, "Queen")
        self.board.increment_turn()
        self.board.updateBoardStateHistory()
      
      
    def uct_score(self, total_simulations, exploration_param=math.sqrt(2)):
      if self.visits == 0:
          return float('inf')  # Handle the division by zero case
      return (self.wins / self.visits) + exploration_param * math.sqrt(math.log(total_simulations) / self.visits)
    
    @profile
    def simulateGame(self):
      result = None
      simulationBoard = self.board.copy()
      while result is None:        
        if simulationBoard.turn_counter % 2 == 0:
          pieces = list(simulationBoard.getPiecesByColor(False))
          random.shuffle(pieces)
          for piece in pieces:  
            possible_moves = piece.getPossibleMoves(simulationBoard)
            if possible_moves:
              next_position = random.choice(list(possible_moves))
              
              simulationBoard.checkFiftyMoveRule(piece, next_position)
              promotion_row = 0 if piece.color == simulationBoard.PlayerColor else 7
              simulationBoard.movePiece(piece, next_position)
              if isinstance(piece, Pawn) and next_position[0]==promotion_row:
                simulationBoard.promote(piece, "Queen")
              simulationBoard.updateBoardStateHistory()
              break
          
        elif simulationBoard.turn_counter % 2 != 0:
          pieces = list(simulationBoard.getPiecesByColor(True))
          random.shuffle(pieces)
          for piece in pieces:  
            possible_moves = piece.getPossibleMoves(simulationBoard)
            if possible_moves:
              next_position = random.choice(list(possible_moves))
              
              simulationBoard.checkFiftyMoveRule(piece, next_position)
              promotion_row = 0 if piece.color == simulationBoard.PlayerColor else 7
              simulationBoard.movePiece(piece, next_position)
              if isinstance(piece, Pawn) and next_position[0]==promotion_row:
                simulationBoard.promote(piece, "Queen")
              simulationBoard.updateBoardStateHistory()
              break
        
        simulationBoard.increment_turn()
        
        result = simulationBoard.checkEndGame()

      return result
    #@profile
    def backpropagate(self, result):
      # Update the node's statistics based on the result
      self.updateStatistics(result)
      
      # Propagate the result up to the parent (if there is a parent)
      if self.parent is not None:
        self.parent.backpropagate(result)
    #@profile
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
  #@profile  
  def selection(self, node):
    if len(node.children) > 0:
      total_simulations = sum(child.visits for child in node.children)
      return max(node.children, key=lambda child: child.uct_score(total_simulations))
    
    return node
  #@profile  
  def expansion(self, node):
    color = not node.color
    pieces = node.board.getPiecesByColor(color)
    for piece in pieces:
      possible_moves = piece.getPossibleMoves(node.board)
      if possible_moves:
        for next_position in possible_moves:
          expanded_node_board = node.board.copy()
          expanded_piece_position = piece.position
          expanded_node = Node(expanded_node_board, expanded_piece_position, next_position, node, color)
          node.children.append(expanded_node) 
        
  #@profile
  def simulation(self, node):    
    for child_node in node.children:
      print("simulate")
      result = child_node.simulateGame()
      child_node.backpropagate(result)
    

    
    

    
      
    

      
    
    