from Piece import Piece
from Position import Position

class Knight(Piece):
  
  def __init__(self, position, isTeam):
    super().__init__(position, isTeam)
    if (self.isTeam):
      self.name = r"images\white-knight.png"
    else:
      self.name = r"images\black-knight.png"
      
  def __str__(self):
    return f'Piece: Position->[Row:{self.position.row}, Col: {self.position.col}], isTeam: {self.isTeam}, Name: {self.name}'
  
  def checkMove(self, board, next_position):
    if(super().checkMove(board, next_position)):
      
      row_diff = abs(self.position.getRow() - next_position.getRow())
      col_diff = abs(self.position.getCol() - next_position.getCol())

      # if its a L-shaped move
      if (row_diff, col_diff) in [(2, 1), (1, 2)]:
        target_cell = board.getCell(next_position)
        if target_cell.getPiece() is None or target_cell.getPiece().isTeam != self.isTeam:
          return True

        return False

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