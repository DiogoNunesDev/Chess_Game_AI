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
        #No targetting piece moves
        if(board.getCell(next_position).getPiece() is None):
          if(self.position.getRow()==6 and next_position.getRow()==4 and next_position.getCol()==self.position.getCol()):
            #Possible initial play of advancing 2 squares 
            return True
          elif(next_position.getRow()==self.position.getRow()-1 and next_position.getCol()==self.position.getCol()):
            return True
        else:
          if((board.getCell(next_position).getPiece() is not None) and 
              (board.getCell(next_position).getPiece().isWhite==False) and 
              (next_position.getRow()==(self.position.getRow()+1)) and 
              (next_position.getCol()==(self.position.getCol()+1 or self.position.getCol()-1))):
            #Plays for eating black pieces
            return True
          elif(self.position.getRow()==6 and next_position.getRow()==4 and next_position.getCol()==self.position.getCol()):
            black_piece_position = Position(self.position.getRow()-1, self.position.getCol())
            if(board.getCell(black_piece_position).getPiece().isWhite==False):
              #En-paissant
              return True

      else:
        #BLACK POSSIBLE MOVES
        return True
    return False
  
