from Piece import Piece
from Position import Position

class Bishop(Piece):
  
  def __init__(self, position, isWhite):
    super().__init__(position, isWhite)
    if (self.isWhite):
      self.name = r"images\white-bishop.png"
    else:
      self.name = r"images\black-bishop.png"
      
  def __str__(self):
    return f'Piece: Position->[Row:{self.position.row}, Col: {self.position.col}], isWhite: {self.isWhite}, Name: {self.name}'
  
  def checkMove(self, board, next_position):
    if(super().checkMove(board, next_position)):
      
      row_diff = next_position.getRow() - self.position.getRow()
      col_diff = next_position.getCol() - self.position.getCol()
      
      #Checking if its a diagonal move
      if abs(row_diff) != abs(col_diff):
        return False
      
      row_direction = 1 if row_diff > 0 else -1 #if row diff is positive, then the bishop is moving downwards. Else upwards. 
      col_direction = 1 if col_diff > 0 else -1 #if row diff is positive, then the bishop is moving rightwards. Else leftwards.
        
      #Checking each square along the diagonal, for pieces in intermediate squares
      for i in range(1, abs(row_diff)):
        intermediate_position = Position(self.position.getRow() + i * row_direction, self.position.getCol() + i * col_direction)
        
        if(board.getCell(intermediate_position).getPiece() is not None):
          return False
      
      if board.getCell(next_position).getPiece() is not None and board.getCell(next_position).getPiece().isWhite == self.isWhite:
        return False
      
      return True
    
  def getPossibleMoves(self, board):
    possible_moves = []
    next_position = None
    for row in range(8):
      for col in range(8):
        next_position = Position(row, col)
        if(self.checkMove(board, next_position)):
          possible_moves.append(next_position)
    
    return possible_moves