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
  
  def checkMove(self, board, next_position):
    if(super().checkMove(board, next_position)):
      row_diff = next_position.row - self.position.row
      col_diff = next_position.col - self.position.col 
      
      #Checking if the move along an axis
      if row_diff != 0 and col_diff != 0:
        return False       
      
      row_direction = 1 if row_diff > 0 else (-1 if row_diff < 0 else 0) # 1 if downward movement, -1 if upward movement and 0 if no vertical movement
      col_direction = 1 if col_diff > 0 else (-1 if col_diff < 0 else 0) # 1 if rightward movement, -1 if leftward movement and 0 if no horizontal movement
      
      #Checking each square along the axis, for pieces in intermediate squares
      for i in range(1, max(abs(row_diff), abs(col_diff))):
        intermediate_position = Position(self.position.row + i * row_direction, self.position.col + i * col_direction)
        
        if board.getCell(intermediate_position).getPiece() is not None:
          return False
        
      if board.getCell(next_position).getPiece() is not None and board.getCell(next_position).getPiece().isTeam == self.isTeam:
        return False

            
      return True
  @profile  
  def getMoves(self, board):
    moves = []
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
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
  
  @profile      
  def getPossibleMoves(self, board):
    possible_moves = []
    moves = self.getMoves(board)
    for next_position in moves:
      if (not board.checkMove(self, next_position)):
        possible_moves.append(next_position)
        
    return possible_moves