from Piece import Piece
from Position import Position
from Rook import Rook

class King(Piece):
  
  def __init__(self, position, isTeam):
    super().__init__(position, isTeam)
    if (self.isTeam):
      self.name = r"images\white-king.png"
    else:
      self.name = r"images\black-king.png"
      
    self.isInCheck = False
          
  def __str__(self):
    return f'Piece: Position->[Row:{self.position.row}, Col: {self.position.col}], isTeam: {self.isTeam}, Name: {self.name}'

  def checkCastle(self, board, next_position):
    if not self.hasMoved and next_position.row == self.position.row:
      row = self.position.row
      direction = 1 if next_position.col > self.position.col else -1
      path_clear = self.isPathClearForCastle(board, row, direction)
      rook_col = 7 if direction > 0 else 0
      rook = board.getCell_2(row, rook_col).piece
            
      return path_clear and isinstance(rook, Rook) and not rook.hasMoved

  def isPathClearForCastle(self, board, row, direction):
    col_start = 4 + direction
    col_end = 7 if direction > 0 else 0
    step = 1 if direction > 0 else -1

    for col in range(col_start, col_end, step):
      if board.getCell_2(row, col).piece is not None:
        return False

    return True
  @profile
  def getMoves(self, board):
    self.moves.clear()
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]  # Adjacent squares in all directions

    for dir in directions:
      row_dir, col_dir = dir
      next_row = self.position.row + row_dir
      next_col = self.position.col + col_dir

      if 0 <= next_row < 8 and 0 <= next_col < 8:
        cell = board.getCell_2(next_row, next_col)
        if cell.piece is None or cell.piece.isTeam != self.isTeam:
          self.moves.add(Position(next_row, next_col))

    # Include castling moves if applicable
    if self.checkCastle(board, Position(self.position.row, 2)):  # Queenside
      self.moves.add(Position(self.position.row, 2))
    if self.checkCastle(board, Position(self.position.row, 6)):  # Kingside
      self.moves.add(Position(self.position.row, 6))

    return self.moves
  @profile  
  def getPossibleMoves(self, board):
    possible_moves = set()
    moves = self.getMoves(board)
    for next_position in set(moves):
      if (not board.checkMove(self, next_position)):
        possible_moves.add(next_position)
        
    return possible_moves