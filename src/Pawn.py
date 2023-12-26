from Piece import Piece
from Position import Position

class Pawn(Piece):
  
  def __init__(self, position, isWhite):
    super().__init__(position, isWhite)
    if (self.isWhite):
      self.name = r"images\white-pawn.png"
    else:
      self.name = r"images\black-pawn.png"
    self.en_passant = None
    
  def getEn_Passant(self):
    return self.en_passant
  
  def setEn_Passant(self, turn):
    self.en_passant = turn
      
  def __str__(self):
    return f'Piece: Position->[Row:{self.position.row}, Col: {self.position.col}], isWhite: {self.isWhite}, Name: {self.name}'
  
  def checkMove(self, board, next_position):
    if(super().checkMove(board, next_position)):
      if(self.isWhite):
        #WHITE POSSIBLE MOVES
        #No targeting piece moves
        if(board.getCell(next_position).getPiece() is None):
          if(self.position.getRow()==6 and next_position.getRow()==4 and next_position.getCol()==self.position.getCol()):
            self.en_passant = board.getTurn_counter()
            #Possible initial play of advancing 2 squares 
            return True
          
          elif(next_position.getRow()==self.position.getRow()-1 and next_position.getCol()==self.position.getCol()):
            #1 Square forward movement
            return True
          
        else:
          if((board.getCell(next_position).getPiece().isWhite==False) and 
              (next_position.getRow()==(self.position.getRow()-1)) and 
              (next_position.getCol()==(self.position.getCol()+1 or self.position.getCol()-1))):
            #Plays for eating black pieces
            return True

      else:
        #BLACK POSSIBLE MOVES
        if(board.getCell(next_position).getPiece() is None):
          if(self.position.getRow()==1 and next_position.getRow()==3 and next_position.getCol()==self.position.getCol()):
            self.en_passant = board.getTurn_counter()
            #Possible initial play of advancing 2 squares 
            return True
          
          elif(next_position.getRow()==self.position.getRow()+1 and next_position.getCol()==self.position.getCol()):
            #1 square forward movement
            return True
          
        else:
          if((board.getCell(next_position).getPiece().isWhite==True) and 
              (next_position.getRow()==(self.position.getRow()+1)) and 
              (next_position.getCol()==(self.position.getCol()+1 or self.position.getCol()-1))):
            #Plays for eating white pieces
            return True
          
    return False
  
  def checkEn_Passant(self, board, next_position):
    row = 3 if self.isWhite else 4
    direction = -1 if self.isWhite else 1
    if(self.position.getRow()==row and next_position.getRow()==row+direction and next_position.getCol()!=self.position.getCol()):
      cell = board.getCell(Position(row, next_position.getCol()))
      if cell.getPiece() is not None and isinstance(cell.getPiece(), Pawn) and cell.getPiece().getEn_Passant() == board.getTurn_counter() - 1:
        return True
    return False
   
  def getPossibleMoves(self, board):
    possible_moves = []
    next_position = None
    for row in range(8):
      for col in range(8):
        next_position = Position(row, col)
        if(self.checkMove(board, next_position)):
          possible_moves.append(next_position)
        elif self.checkEn_Passant(board, next_position):
          possible_moves.append(next_position)
    
    return possible_moves