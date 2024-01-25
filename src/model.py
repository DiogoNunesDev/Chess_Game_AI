import random
import time
from Board import Board
from King import King
from Position import Position
from Rook import Rook
from Pawn import Pawn
from MCTS import MCTS, Node

def make_random_move(board, PlayerColor):
    # Collect all pieces that have legal moves and color different to the player
    pieces = board.getEnemyPieces() if PlayerColor else board.getTeamPieces()
    
    if not pieces:
        return
      
    pieces_with_moves = [piece for piece in pieces if piece.getPossibleMoves(board)]
    
    if not pieces_with_moves:
        return
    # Randomly select a piece
    piece = random.choice(pieces_with_moves)
    
    # Randomly select one of its legal moves
    possible_moves = piece.getPossibleMoves(board)
    
    if not possible_moves:
        return         
    next_position = random.choice(piece.getPossibleMoves(board))
    if (not board.checkMove(piece, next_position)):
      if (isinstance(piece, King) and piece.checkCastle(board, next_position)):
        board.castle(piece, next_position)
      elif isinstance(piece, Pawn) and piece.checkEn_Passant(board, next_position):
        board.En_Passant(piece, next_position)
      else:
        board.movePiece(piece, next_position)
        if isinstance(piece, Pawn) and next_position.row==0:
          promotion_choice = "Queen"
          board.promote(piece, promotion_choice)
      board.increment_turn()


def make_move(board, PlayerColor):
  mcts = MCTS(2, board, not PlayerColor)
  root = Node()
  root.board = board
  root.parent = None

  start_time = time.time()
  while time.time() - start_time < 30:
    node = root
    while node.children:
      print("select")
      node = mcts.selection(node)
      
    if not node.board.endGame:
      print("Expand")
      mcts.expansion(node)
    
    mcts.simulation(node)
    
  best_child = max(root.children, key= lambda child: child.visits)
  return best_child.move  
