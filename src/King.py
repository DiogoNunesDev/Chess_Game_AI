from Piece import Piece
from Position import Position

class King(Piece):
  
  def __init__(self, position, isTeam):
    super().__init__(position, isTeam)
    if (self.isTeam):
      self.name = r"images\white-king.png"
    else:
      self.name = r"images\black-king.png"
          
  def __str__(self):
    return f'Piece: Position->[Row:{self.position.row}, Col: {self.position.col}], isTeam: {self.isTeam}, Name: {self.name}'
  
  def checkMove(self, board, next_position):
    if(super().checkMove(board, next_position)):
      row_diff = next_position.getRow() - self.position.getRow()
      col_diff = next_position.getCol() - self.position.getCol()

      # Check for standard King move (one square in any direction)
      if abs(row_diff) <= 1 and abs(col_diff) <= 1:
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
    if next_position.getRow()==self.position.getRow():
      if next_position.getCol() in {0, 1, 2}:
        if (board.getCell(Position(self.position.getRow(), 1)).getPiece() is None and
          board.getCell(Position(self.position.getRow(), 2)).getPiece() is None and
          board.getCell(Position(self.position.getRow(), 3)).getPiece() is None and board.getCell(Position(self.position.getRow(), 0)).getPiece() is not None and 
          not board.getCell(Position(self.position.getRow(), 0)).getPiece().getHasMoved()):
          return True
                    
      elif next_position.getCol() in {6, 7}:
        if (board.getCell(Position(self.position.getRow(), 5)).getPiece() is None and
          board.getCell(Position(self.position.getRow(), 6)).getPiece() is None and board.getCell(Position(self.position.getRow(), 7)).getPiece() is not None and 
          not board.getCell(Position(self.position.getRow(), 7)).getPiece().getHasMoved()):
          return True
    
    return False
        
  def getPossibleMoves(self, board):
    possible_moves = []
    moves = self.getMoves(board)
    for next_position in moves:
      tempBoard = board.simulateMove(self, next_position)
      if (not tempBoard.isKingInCheck()):
        possible_moves.append(next_position)
        
    return possible_moves