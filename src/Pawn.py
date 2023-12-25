from Piece import Piece
from Position import Position

class Pawn(Piece):
  
  def __init__(self, position, isWhite):
    super().__init__(position, isWhite)
    if (self.isWhite):
      self.name = r"images\white-pawn.png"
    else:
      self.name = r"images\black-pawn.png"
      
  def __str__(self):
    return f'Piece: Position->[Row:{self.position.row}, Col: {self.position.col}], isWhite: {self.isWhite}, Name: {self.name}'
  
  def checkMove(self, board, next_position):
    if(super().checkMove(board, next_position)):
      if(self.isWhite):
        #WHITE POSSIBLE MOVES
        #No targeting piece moves
        if(board.getCell(next_position).getPiece() is None):
          if(self.position.getRow()==6 and next_position.getRow()==4 and next_position.getCol()==self.position.getCol()):
            #Possible initial play of advancing 2 squares 
            return True
          elif(next_position.getRow()==self.position.getRow()-1 and next_position.getCol()==self.position.getCol()):
            #1 Square forward movement
            return True
        else:
          if((board.getCell(next_position).getPiece().isWhite==False) and 
              (next_position.getRow()==(self.position.getRow()-1)) and 
              (next_position.getCol()==(self.position.getCol()+1 or self.position.getCol()-1))):
            print("this")
            #Plays for eating black pieces
            return True
          elif(self.position.getRow()==6 and next_position.getRow()==4 and next_position.getCol()==self.position.getCol()):
            black_piece_position = Position(self.position.getRow()-1, self.position.getCol())
            if(board.getCell(black_piece_position).getPiece().isWhite==False):
              #En-paissant
              return True

      else:
        #BLACK POSSIBLE MOVES
        if(board.getCell(next_position).getPiece() is None):
          if(self.position.getRow()==1 and next_position.getRow()==3 and next_position.getCol()==self.position.getCol()):
            #Possible initial play of advancing 2 squares 
            return True
          elif(next_position.getRow()==self.position.getRow()+1 and next_position.getCol()==self.position.getCol()):
            #1 square forward movement
            return True
        else:
          if((board.getCell(next_position).getPiece().isWhite==True) and 
              (next_position.getRow()==(self.position.getRow()+1)) and 
              (next_position.getCol()==(self.position.getCol()+1 or self.position.getCol()-1))):
            print("this")
            #Plays for eating white pieces
            return True
          elif(self.position.getRow()==1 and next_position.getRow()==3 and next_position.getCol()==self.position.getCol()):
            black_piece_position = Position(self.position.getRow()-1, self.position.getCol())
            if(board.getCell(black_piece_position).getPiece().isWhite==False):
              #En-paissant
              return True
    return False
  
