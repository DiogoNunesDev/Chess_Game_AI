from Piece import Piece

class Knight(Piece):
  
  def __init__(self, position, isWhite):
    super().__init__(position, isWhite)
    if (self.isWhite):
      self.name = r"images\white-knight.png"
    else:
      self.name = r"images\black-knight.png"
      
  def __str__(self):
    return f'Piece: Position->[Row:{self.position.row}, Col: {self.position.col}], isWhite: {self.isWhite}, Name: {self.name}'
  
  def checkMove(self, board, next_position):
    if(super().checkMove(board, next_position)):
      if(board.getCell(next_position).getPiece() is None):
          if((next_position.getRow()==self.getPosition().getRow()-2 and next_position.getCol()==self.getPosition().getCol()-1) or
             (next_position.getRow()==self.getPosition().getRow()-2 and next_position.getCol()==self.getPosition().getCol()+1) or
              (next_position.getRow()==self.getPosition().getRow()+2 and next_position.getCol()==self.getPosition().getCol()-1) or 
              (next_position.getRow()==self.getPosition().getRow()+2 and next_position.getCol()==self.getPosition().getCol()+1) or 
              (next_position.getRow()==self.getPosition().getRow()-1 and next_position.getCol()==self.getPosition().getCol()-2) or 
              (next_position.getRow()==self.getPosition().getRow()+1 and next_position.getCol()==self.getPosition().getCol()-2) or 
              (next_position.getRow()==self.getPosition().getRow()-1 and next_position.getCol()==self.getPosition().getCol()+2) or 
              (next_position.getRow()==self.getPosition().getRow()+1 and next_position.getCol()==self.getPosition().getCol()+2)):
              return True
      else:
        if(not board.getCell(next_position).getPiece().isWhite):
          if((next_position.getRow()==self.getPosition().getRow()-2 and next_position.getCol()==self.getPosition().getCol()-1) or
            (next_position.getRow()==self.getPosition().getRow()-2 and next_position.getCol()==self.getPosition().getCol()+1) or
            (next_position.getRow()==self.getPosition().getRow()+2 and next_position.getCol()==self.getPosition().getCol()-1) or 
            (next_position.getRow()==self.getPosition().getRow()+2 and next_position.getCol()==self.getPosition().getCol()+1) or 
            (next_position.getRow()==self.getPosition().getRow()-1 and next_position.getCol()==self.getPosition().getCol()-2) or 
            (next_position.getRow()==self.getPosition().getRow()+1 and next_position.getCol()==self.getPosition().getCol()-2) or 
            (next_position.getRow()==self.getPosition().getRow()-1 and next_position.getCol()==self.getPosition().getCol()+2) or 
            (next_position.getRow()==self.getPosition().getRow()+1 and next_position.getCol()==self.getPosition().getCol()+2)):
            return True
      