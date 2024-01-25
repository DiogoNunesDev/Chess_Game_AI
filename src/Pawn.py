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
  
  def checkMove(self, board, next_position):
    if(super().checkMove(board, next_position)):
      if(self.isTeam==board.PlayerColor):
        #Player POSSIBLE MOVES
        #No targeting piece moves
        if(board.getCell(next_position).getPiece() is None):
          if(self.position.row==6 and next_position.row==4 and next_position.col==self.position.col and board.getCell(Position(5, self.position.col)).getPiece() is None):
            self.en_passant = board.getTurn_counter()
            #Possible initial play of advancing 2 squares 
            return True
          
          elif(next_position.row==self.position.row-1 and next_position.col==self.position.col):
            #1 Square forward movement
            return True
          
        else:
          if((board.getCell(next_position).getPiece().isTeam != self.isTeam) and 
              (next_position.row==(self.position.row-1)) and 
              ((abs(next_position.col - self.position.col)) == 1)):
            
            return True
          
      else:
        #Bot POSSIBLE MOVES
        if(board.getCell(next_position).getPiece() is None):
          if(self.position.row==1 and next_position.row==3 and next_position.col==self.position.col  and board.getCell(Position(2, self.position.col)).getPiece() is None):
            self.en_passant = board.getTurn_counter()
            #Possible initial play of advancing 2 squares 
            return True
          
          elif(next_position.row==self.position.row+1 and next_position.col==self.position.col):
            #1 square forward movement
            return True
          
        else:
          if((board.getCell(next_position).getPiece().isTeam != self.isTeam) and 
              (next_position.row==(self.position.row+1)) and 
              ((abs(next_position.col - self.position.col)) == 1)):
            return True
          
    return False
  
  def checkEn_Passant(self, board, next_position):
    row = 3 if self.isTeam else 4
    direction = -1 if self.isTeam else 1
    if((self.position.row==row) and (next_position.row == row + direction) and (next_position.col != self.position.col)):
      cell = board.getCell(Position(row, next_position.col))
      if (cell.getPiece() is not None) and isinstance(cell.getPiece(), Pawn) and (cell.getPiece().getEn_Passant() == board.getTurn_counter() - 1):
        return True
    return False
  
  @profile  
  def getMoves(self, board):
    moves = []
    direction = -1 if self.isTeam else 1  # Player moves up (-1), Bot moves down (+1)
    start_row = 6 if self.isTeam else 1   # Starting row for pawns (6 for Player, 1 for Bot)

    # Single square forward
    next_row = self.position.row + direction
    if 0 <= next_row < 8 and board.getCell(Position(next_row, self.position.col)).getPiece() is None:
      moves.append(Position(next_row, self.position.col))

    # Double square forward from start position
    if self.position.row == start_row:
      two_squares_row = self.position.row + 2 * direction
      if not board.getCell(Position(two_squares_row, self.position.col)).getPiece():
        moves.append(Position(two_squares_row, self.position.col))

    # Diagonal captures
    for col_offset in [-1, 1]:  # Check diagonally to the left and right
      next_col = self.position.col + col_offset
      if 0 <= next_col < 8 and 0 <= next_row < 8:
        diagonal_position = Position(next_row, next_col)
        diagonal_piece = board.getCell(diagonal_position).getPiece()
        if self.checkEn_Passant(board, diagonal_position):
          moves.append(diagonal_position)
        if diagonal_piece is not None and diagonal_piece.isTeam != self.isTeam:
          moves.append(diagonal_position)

    return moves
  
  @profile
  def getPossibleMoves(self, board):
    possible_moves = []
    moves = self.getMoves(board)
    for next_position in moves:
      if (not board.checkMove(self, next_position)):
        possible_moves.append(next_position)
        
    return possible_moves