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
  
  @profile
  def getMoves(self, board):
    self.moves.clear()
    move_offsets = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]  # All possible L-shape moves
    
    for offset in move_offsets:
      row_offset, col_offset = offset
      next_row = self.position.row + row_offset
      next_col = self.position.col + col_offset
      
      if 0 <= next_row < 8 and 0 <= next_col < 8:
        piece = board.getCell_2(next_row, next_col).piece
        if piece is None or piece.isTeam != self.isTeam:
          self.moves.add(Position(next_row, next_col))

    return self.moves
  @profile
  def getPossibleMoves(self, board):
    possible_moves = set()
    moves = self.getMoves(board)
    for next_position in set(moves):
      if (not board.checkMove(self, next_position)):
        possible_moves.add(next_position)
        
    return possible_moves