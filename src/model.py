import random
from Pawn import Pawn
#from MCTS import MCTS, Node
from minimax import MiniMax


def make_random_move(board, PlayerColor):
    pieces = list(board.piecesByColor[not PlayerColor])   

    if not pieces:
        return
    random.shuffle(pieces)
    for piece in pieces:  
      possible_moves = piece.getPossibleMoves(board)
      if possible_moves:
        next_position = random.choice(list(possible_moves))
        #if (not board.checkMove(piece, next_position)):
        board.checkFiftyMoveRule(piece, next_position)
        promotion_row = 0 if piece.color == board.PlayerColor else 7
        board.movePiece(piece, next_position)
        if isinstance(piece, Pawn) and next_position[0]==promotion_row:
          board.promote(piece, "Queen")
        board.increment_turn()
        board.updateBoardStateHistory() 
        return

def make_move(board, PlayerColor):
  copy_board = board.copy()
  mcts = MCTS(1, copy_board, not PlayerColor)
  root = Node(copy_board, None, None, None, mcts.AI_color)
  node = root
  best_child = None
  while node.depth != mcts.depth:
    node = root
    while node.children:
      print("select")
      node = mcts.selection(node)
      
    if not node.board.endGame:
      print("Expand")
      mcts.expansion(node)
    
    mcts.simulation(node)
    print("Done")
    
    best_child = max(root.children, key= lambda child: child.visits)
  return best_child.piece_position, best_child.move

def minimax(board, depth, color):
  minimax = MiniMax(board, depth, color)
  return minimax.getBestMove()

        
        
        
    
  
  
