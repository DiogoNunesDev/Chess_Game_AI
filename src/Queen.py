from Piece import Piece
from Position import Position

class Queen(Piece):
  
  def __init__(self, position, isTeam):
    super().__init__(position, isTeam)
    if (self.isTeam):
      self.name = r"images\white-queen.png"
    else:
      self.name = r"images\black-queen.png"
      
  def __str__(self):
    return f'Piece: Position->[Row:{self.position.row}, Col: {self.position.col}], isTeam: {self.isTeam}, Name: {self.name}'
  
  
  @profile
  def getMoves(self, board): 
    self.moves.clear()
    directions = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)] #All 8 directions for the queens movement
    for row_dir, col_dir in directions:
      next_row, next_col = self.position.row + row_dir, self.position.col + col_dir

      while 0 <= next_row < 8 and 0 <= next_col < 8:
        cell = board.getCell_2(next_row, next_col)
        if cell.isOccupied():
          if cell.piece.isTeam != self.isTeam:
            self.moves.add((next_row, next_col))  # Using tuples for positions to avoid creating new objects
            break  # Stop searching this direction if a piece is encountered
        else:
          self.moves.add((next_row, next_col))

        next_row += row_dir
        next_col += col_dir

        return self.moves

    
    return self.moves
  
  @profile
  def getPossibleMoves(self, board):
    possible_moves = set()
    moves = self.getMoves(board)
    for next_position in set(moves):
      if (not board.checkMove(self, next_position)):
        possible_moves.add(next_position)
        
    return possible_moves