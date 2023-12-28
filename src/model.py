import random
from Board import Board
from King import King
from Position import Position
from Rook import Rook

def make_random_move(board, PlayerIsWhite):
    # Collect all black pieces that have legal moves
    pieces = []
    for row in range(8):
      for col in range(8):
        piece = board.getCell(Position(row, col)).getPiece()
        if piece is not None and piece.getIsWhite()!=PlayerIsWhite and len(piece.getPossibleMoves(board)) > 0:
          pieces.append(piece)

    # If no legal moves, return (e.g., checkmate or stalemate)
    if not pieces:
        return

    # Randomly select a black piece
    piece = random.choice(pieces)
            
    # Randomly select one of its legal moves
    move = random.choice(piece.getPossibleMoves(board))

    # Make the move
    piece.move(board, move)
    board.increment_turn()