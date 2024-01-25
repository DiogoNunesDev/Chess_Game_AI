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
  
  def checkMove(self, board, next_position):
    if(super().checkMove(board, next_position)):
      
      row_diff = next_position.row - self.position.row
      col_diff = next_position.col - self.position.col
      
      #Checking if its a diagonal move
      if abs(row_diff) != abs(col_diff):
        return False
      
      row_direction = 1 if row_diff > 0 else -1 #if row diff is positive, then the bishop is moving downwards. Else upwards. 
      col_direction = 1 if col_diff > 0 else -1 #if row diff is positive, then the bishop is moving rightwards. Else leftwards.
        
      #Checking each square along the diagonal, for pieces in intermediate squares
      for i in range(1, abs(row_diff)):
        intermediate_position = Position(self.position.row + i * row_direction, self.position.col + i * col_direction)
        
        if(board.getCell(intermediate_position).getPiece() is not None):
          return False
      
      if board.getCell(next_position).getPiece() is not None and board.getCell(next_position).getPiece().isTeam == self.isTeam:
        return False
      
      return True
    
  def getMoves(self, board):
    moves = []
    directions = [(1,1), (1,-1), (-1,1), (-1,-1)] #All 8 directions for the queens movement
    for dir in directions:
      row_dir, col_dir = dir
      next_row = self.position.row + row_dir
      next_col = self.position.col + col_dir
      
      while 0 <= next_row < 8 and 0 <= next_col < 8:
        next_position = Position(next_row, next_col)
        if board.getCell(next_position).getPiece() is not None:
          if board.getCell(next_position).getPiece().isTeam != self.isTeam:
            moves.append(next_position)
          break
        
        moves.append(next_position)
        next_row += row_dir
        next_col += col_dir
    
    return moves
  
  def getPossibleMoves(self, board):
    possible_moves = []
    moves = self.getMoves(board)
    for next_position in moves:
      if (not board.checkMove(self, next_position)):
        possible_moves.append(next_position)
        
    return possible_moves
  