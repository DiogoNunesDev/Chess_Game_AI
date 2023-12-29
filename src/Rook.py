from King import King
from Piece import Piece
from Position import Position

class Rook(Piece):
  
  def __init__(self, position, isWhite):
    super().__init__(position, isWhite)
    if (self.isWhite):
      self.name = r"images\white-rook.png"
    else:
      self.name = r"images\black-rook.png"
    self.hasMoved = False
    
  def getHasMoved(self):
    return self.hasMoved
  
  def setHasMoved(self, bool):
    self.hasMoved = bool
          
  def __str__(self):
    return f'Piece: Position->[Row:{self.position.row}, Col: {self.position.col}], isWhite: {self.isWhite}, Name: {self.name}'
  
  def checkMove(self, board, next_position):
    if(super().checkMove(board, next_position)):
      row_diff = next_position.getRow() - self.position.getRow()
      col_diff = next_position.getCol() - self.position.getCol() 
      
      #Checking if the move along an axis
      if row_diff != 0 and col_diff != 0:
        return False       
      
      row_direction = 1 if row_diff > 0 else (-1 if row_diff < 0 else 0) # 1 if downward movement, -1 if upward movement and 0 if no vertical movement
      col_direction = 1 if col_diff > 0 else (-1 if col_diff < 0 else 0) # 1 if rightward movement, -1 if leftward movement and 0 if no horizontal movement
      
      #Checking each square along the axis, for pieces in intermediate squares
      for i in range(1, max(abs(row_diff), abs(col_diff))):
        intermediate_position = Position(self.position.getRow() + i * row_direction, self.position.getCol() + i * col_direction)
        
        if board.getCell(intermediate_position).getPiece() is not None:
          return False
        
      if board.getCell(next_position).getPiece() is not None and board.getCell(next_position).getPiece().isWhite == self.isWhite:
        return False

            
      return True
    
  def getMoves(self, board):
    moves = []
    next_position = None
    for row in range(8):
      for col in range(8):
        next_position = Position(row, col)
        if(self.checkMove(board, next_position)):
          moves.append(next_position)
        elif self.checkCastle(board, next_position):
          moves.append(next_position)
    return moves
  
  def checkCastle(self, board, next_position):
    if not self.hasMoved:
      if next_position.getRow()==self.position.getRow():
        if next_position.getCol() in {2, 3}:
          if (board.getCell(Position(self.position.getRow(), 1)).getPiece() is None and
            board.getCell(Position(self.position.getRow(), 2)).getPiece() is None and
            board.getCell(Position(self.position.getRow(), 3)).getPiece() is None):
            return True
        elif next_position.getCol()==5:
          if (board.getCell(Position(self.position.getRow(), 5)).getPiece() is None and
            board.getCell(Position(self.position.getRow(), 6)).getPiece() is None):
            return True
        
        elif next_position.getCol()==4:
          if self.position.getCol()==7 and (board.getCell(Position(self.position.getRow(), 5)).getPiece() is None and
            board.getCell(Position(self.position.getRow(), 6)).getPiece() is None):
            return True
          
          elif (self.position.getCol()==0 and board.getCell(Position(self.position.getRow(), 1)).getPiece() is None and
            board.getCell(Position(self.position.getRow(), 2)).getPiece() is None and
            board.getCell(Position(self.position.getRow(), 3)).getPiece() is None):
            return True
            
  def getPossibleMoves(self, board):
    possible_moves = []
    moves = self.getMoves(board)
    for next_position in moves:
      tempBoard = board.simulateMove(self, next_position)
      if (not tempBoard.isKingInCheck(self.isWhite)):
        possible_moves.append(next_position)
        
    return possible_moves
