from Piece import Piece
from Position import Position

class Knight(Piece):
  
  def __init__(self, position, isTeam):
    super().__init__(position, isTeam)
    if (self.isTeam):
      self.name = r"images\white-knight.png"
    else:
      self.name = r"images\black-knight.png"
      
  def __str__(self):
    return f'Piece: Position->[Row:{self.position.row}, Col: {self.position.col}], isTeam: {self.isTeam}, Name: {self.name}'
  
  def checkMove(self, board, next_position):
    if(super().checkMove(board, next_position)):
      
      row_diff = abs(self.position.row - next_position.row)
      col_diff = abs(self.position.col - next_position.col)

      # if its a L-shaped move
      if (row_diff, col_diff) in [(2, 1), (1, 2)]:
        target_cell = board.getCell(next_position)
        if target_cell.getPiece() is None or target_cell.getPiece().isTeam != self.isTeam:
          return True

        return False

  def getMoves(self, board):
    moves = []
    move_offsets = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]  # All possible L-shape moves
    
    for offset in move_offsets:
      row_offset, col_offset = offset
      next_row = self.position.row + row_offset
      next_col = self.position.col + col_offset
      
      if 0 <= next_row < 8 and 0 <= next_col < 8:
        next_position = Position(next_row, next_col)
        cell = board.getCell(next_position)
        if cell.getPiece() is None or cell.getPiece().isTeam != self.isTeam:
          moves.append(next_position)

    return moves
  
  def getPossibleMoves(self, board):
    possible_moves = []
    moves = self.getMoves(board)
    for next_position in moves:
      if (not board.checkMove(self, next_position)):
        possible_moves.append(next_position)
        
    return possible_moves