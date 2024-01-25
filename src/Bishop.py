from Piece import Piece
from Position import Position


class Bishop(Piece):
  
  def __init__(self, position, isTeam):
    super().__init__(position, isTeam)
    if (self.isTeam):
      self.name = r"images\white-bishop.png"
    else:
      self.name = r"images\black-bishop.png"
      
  def __str__(self):
    return f'Piece: Position->[Row:{self.position.row}, Col: {self.position.col}], isTeam: {self.isTeam}, Name: {self.name}'
  @profile    
  def getMoves(self, board):
    self.moves.clear()
    directions = [(1,1), (1,-1), (-1,1), (-1,-1)] #All 8 directions for the queens movement
    for dir in directions:
      row_dir, col_dir = dir
      next_row = self.position.row + row_dir
      next_col = self.position.col + col_dir
      
      while 0 <= next_row < 8 and 0 <= next_col < 8:
        next_position = Position(next_row, next_col)
        piece = board.getCell_2(next_position.row, next_position.col).piece
        if piece is not None:
          if piece.isTeam != self.isTeam:
            self.moves.add(next_position)
          break
        
        self.moves.add(next_position)
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
  