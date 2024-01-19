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
  
  def checkMove(self, board, next_position):
    if(super().checkMove(board, next_position)):
      row_diff = next_position.getRow() - self.position.getRow()
      col_diff = next_position.getCol() - self.position.getCol()

      # Check if the move is along a rank, file, or diagonal
      if not (row_diff == 0 or col_diff == 0 or abs(row_diff) == abs(col_diff)):
        return False  # The move is not horizontal, vertical, or diagonal

      # Determine move direction
      row_direction = 0 if row_diff == 0 else (1 if row_diff > 0 else -1) # 0 if not a vertical movement. 1 if moving downwards. -1 if moving upwards
      col_direction = 0 if col_diff == 0 else (1 if col_diff > 0 else -1) # 0 if no horizontal movement. 1 if moving rightwards. -1 if moving leftwards

      #Checking each square along the path, for pieces in intermediate squares
      steps = max(abs(row_diff), abs(col_diff))
      for i in range(1, steps):
        intermediate_position = Position(self.position.getRow() + i * row_direction, self.position.getCol() + i * col_direction)
        
        if board.getCell(intermediate_position).getPiece() is not None:
          return False
      
      if board.getCell(next_position).getPiece() is not None and board.getCell(next_position).getPiece().isTeam == self.isTeam:
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
    
    return moves
  
  def getPossibleMoves(self, board):
    possible_moves = []
    moves = self.getMoves(board)
    for next_position in moves:
      tempBoard = board.simulateMove(self, next_position)
      if (not tempBoard.isKingInCheck(self.isTeam)):
        possible_moves.append(next_position)
        
    return possible_moves