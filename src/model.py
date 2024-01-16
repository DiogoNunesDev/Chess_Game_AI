import random
from Board import Board
from King import King
from Position import Position
from Rook import Rook
from Pawn import Pawn

def make_random_move(board, PlayerColor):
    # Collect all pieces that have legal moves and color different to the player
    
    pieces = []
    for row in range(8):
      for col in range(8):
        piece = board.getCell(Position(row, col)).getPiece()
        if piece is not None and piece.getIsTeam()!=PlayerColor and len(piece.getPossibleMoves(board)) > 0:
          pieces.append(piece)

    # If no legal moves, return (e.g., checkmate or stalemate)
    if not pieces:
        return

    # Randomly select a black piece
    piece = random.choice(pieces)
            
    # Randomly select one of its legal moves
    next_position = random.choice(piece.getPossibleMoves(board))
    tempBoard = board.simulateMove(piece, next_position)
    if (not tempBoard.isKingInCheck()):
      if ((isinstance(piece, King) or isinstance(piece, Rook)) and piece.checkCastle(board, next_position)):
        board.castle(piece, next_position)
        board.increment_turn()
      elif isinstance(piece, Pawn) and piece.checkEn_Passant(board, next_position):
        board.En_Passant(piece, next_position)
        board.increment_turn()
      else:
        piece.move(board, next_position)
        board.increment_turn()
    
"""
possible_moves = piece.getPossibleMoves(board)
      if next_position in possible_moves:
          tempBoard = board.simulateMove(piece, next_position)
          if (not tempBoard.isKingInCheck(piece.isTeam)):
            if ((isinstance(piece, King) or isinstance(piece, Rook)) and piece.checkCastle(board, next_position)):
              board.castle(piece, next_position)
              board.increment_turn()
            elif isinstance(piece, Pawn) and piece.checkEn_Passant(board, next_position):
              board.En_Passant(piece, next_position)
              board.increment_turn()
            else:
              piece.move(board, next_position)
              board.increment_turn()

"""