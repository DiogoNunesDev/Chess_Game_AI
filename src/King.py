from Piece import Piece
from Position import Position
from Rook import Rook

class King(Piece):
  
  def __init__(self, position, isWhite):
    super().__init__(position, isWhite)
    if (self.isWhite):
      self.name = r"images\white-king.png"
    else:
      self.name = r"images\black-king.png"
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

      # Check for standard King move (one square in any direction)
      if abs(row_diff) <= 1 and abs(col_diff) <= 1:
        return True

      

  def getPossibleMoves(self, board):
    possible_moves = []
    next_position = None
    for row in range(8):
      for col in range(8):
        next_position = Position(row, col)
        if(self.checkMove(board, next_position)):
          possible_moves.append(next_position)
        elif self.checkCastle(board, next_position):
          possible_moves.append(next_position)
    
    return possible_moves
  
  def checkCastle(self, board, next_position):
    if next_position.getRow()==self.position.getRow():
      if next_position.getCol() in {0, 1, 2}:
        if (board.getCell(Position(self.position.getRow(), 1)).getPiece() is None and
          board.getCell(Position(self.position.getRow(), 2)).getPiece() is None and
          board.getCell(Position(self.position.getRow(), 3)).getPiece() is None):
          return True
                    
      elif next_position.getCol() in {6, 7}:
        if (board.getCell(Position(self.position.getRow(), 5)).getPiece() is None and
          board.getCell(Position(self.position.getRow(), 6)).getPiece() is None):
          return True
        
        
        """
        if (not (board.isSquareUnderAttack(board.getCell(Position(self.position.getRow(), 1)), self.isWhite)) and 
          (not board.isSquareUnderAttack(board.getCell(Position(self.position.getRow(), 2)), self.isWhite)) and 
          (not board.isSquareUnderAttack(board.getCell(Position(self.position.getRow(), 3)), self.isWhite)) and 
          (not board.isSquareUnderAttack(board.getCell(self.position), self.isWhite))):
          return True
        
        if (not (board.isSquareUnderAttack(board.getCell(Position(self.position.getRow(), 5)), self.isWhite)) and 
          (not board.isSquareUnderAttack(board.getCell(Position(self.position.getRow(), 6)), self.isWhite)) and
          (not board.isSquareUnderAttack(board.getCell(self.position), self.isWhite))):
          return True
        """