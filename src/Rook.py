from Piece import Piece
from Position import Position

class Rook(Piece):
  
  def __init__(self, position, isTeam):
    super().__init__(position, isTeam)
    if (self.isTeam):
      self.name = r"images\white-rook.png"
    else:
      self.name = r"images\black-rook.png"
              
  def __str__(self):
    return f'Piece: Position->[Row:{self.position.row}, Col: {self.position.col}], Name: {self.name}'
  
  @profile  
  def getMoves(self, board):
    self.moves.clear()
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    for dir in directions:
      row_dir, col_dir = dir
      next_row = self.position.row + row_dir
      next_col = self.position.col + col_dir
      
      while 0 <= next_row < 8 and 0 <= next_col < 8:
        piece = board.getCell_2(next_row, next_col).piece
        if piece is not None:
          if piece.isTeam != self.isTeam:
            self.moves.add(Position(next_row, next_col))
          break
        
        self.moves.add(Position(next_row, next_col))
        next_row += row_dir
        next_col += col_dir
    return self.moves
  
  @profile      
  def getPossibleMoves(self, board):
    possible_moves = set()
    moves = self.getMoves(board)
    for next_position in set(moves):
      if (not board.checkMove(self, next_position)):
        possible_moves.add(next_position)
        
    return possible_moves