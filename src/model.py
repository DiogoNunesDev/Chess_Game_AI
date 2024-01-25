import random
import time
from Board import Board
from King import King
from Position import Position
from Rook import Rook
from Pawn import Pawn
from MCTS import MCTS, Node

@profile
def make_random_move(board, PlayerColor):
    # Collect all pieces that have legal moves and color different to the player
    pieces = board.getEnemyPieces() if PlayerColor else board.getTeamPieces()
    
    if not pieces:
        return
    random.shuffle(pieces)

    for piece in pieces:  
      possible_moves = piece.getPossibleMoves(board)
      if possible_moves:
        next_position = random.choice(list(possible_moves))
        if (not board.checkMove(piece, next_position)):
          board.checkFiftyMoveRule(piece, next_position)
          if (isinstance(piece, King) and piece.checkCastle(board, next_position)):
            board.castle(piece, next_position)
          elif isinstance(piece, Pawn) and piece.checkEn_Passant(board, next_position):
            board.En_Passant(piece, next_position)
          else:
            board.movePiece(piece, next_position)
            if isinstance(piece, Pawn) and next_position.row==7:
              board.promote(piece, "Queen")
          board.increment_turn()
          return


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
