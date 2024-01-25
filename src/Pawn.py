from Piece import Piece
from Position import Position

class Pawn(Piece):
  
  def __init__(self, position, isTeam):
    super().__init__(position, isTeam)
    if (self.isTeam):
      self.name = r"images\white-pawn.png"
    else:
      self.name = r"images\black-pawn.png"
    self.en_passant = None
    
  def getEn_Passant(self):
    return self.en_passant
  
  def setEn_Passant(self, turn):
    self.en_passant = turn
      
  def __str__(self):
    return f'Piece: Position->[Row:{self.position.row}, Col: {self.position.col}], isTeam: {self.isTeam}, Name: {self.name}'

  def checkEn_Passant(self, board, next_position):
    row = 3 if self.isTeam else 4
    direction = -1 if self.isTeam else 1
    if((self.position.row==row) and (next_position.row == row + direction) and (next_position.col != self.position.col)):
      cell = board.getCell_2(row, next_position.col)
      if (cell.piece is not None) and isinstance(cell.piece, Pawn) and (cell.piece.getEn_Passant() == board.getTurn_counter() - 1):
        return True
    return False
  
  @profile  
  def getMoves(self, board):
    self.moves.clear()
    direction = -1 if self.isTeam==board.PlayerColor else 1  # Player moves up (-1), Bot moves down (+1)
    start_row = 6 if self.isTeam==board.PlayerColor else 1   # Starting row for pawns

    # Check single and double square forward
    next_row = self.position.row + direction
    if 0 <= next_row < 8:
      # Single square
      pos = Position(next_row, self.position.col)
      if not board.getCell_2(pos.row, pos.col).piece:
        self.moves.add(pos)

        # Double square
        if self.position.row == start_row:
          two_squares_row = self.position.row + 2 * direction
          pos = Position(two_squares_row, self.position.col)
          if not board.getCell_2(pos.row, pos.col).piece:
            self.moves.add(pos)

    # Diagonal captures - only check adjacent columns
    for col_offset in [-1, 1]:
      next_col = self.position.col + col_offset
      if 0 <= next_col < 8 and 0 <= next_row < 8:
        diagonal_position = Position(next_row, next_col)
        diagonal_piece = board.getCell_2(diagonal_position.row, diagonal_position.col).piece

        if self.checkEn_Passant(board, diagonal_position):
          self.moves.add(diagonal_position)
        elif diagonal_piece and diagonal_piece.isTeam != self.isTeam:
          self.moves.add(diagonal_position)

    return self.moves
  
  @profile
  def getPossibleMoves(self, board):
    possible_moves = set()
    moves = self.getMoves(board)
    for next_position in set(moves):
      if (not board.checkMove(self, next_position)):
        possible_moves.add(next_position)
        
    return possible_moves