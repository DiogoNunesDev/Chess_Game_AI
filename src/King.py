from Piece import Piece

class King(Piece):
  
  def __init__(self, position, isWhite):
    super().__init__(position, isWhite)
    if (self.isWhite):
      self.name = r"images\white-king.png"
    else:
      self.name = r"images\black-king.png"
      
  def __str__(self):
    return f'Piece: Position->[Row:{self.position.row}, Col: {self.position.col}], isWhite: {self.isWhite}, Name: {self.name}'
  
  def checkMove(self, board, next_position):
    if(super().checkMove(board, next_position)):
      if((next_position.getRow()==self.getPosition().getRow()+1 and next_position.getCol()==self.getPosition().getCol()) or
         (next_position.getRow()==self.getPosition().getRow()+1 and next_position.getCol()==self.getPosition().getCol()+1) or
         (next_position.getRow()==self.getPosition().getRow()+1 and next_position.getCol()==self.getPosition().getCol()-1) or
         (next_position.getRow()==self.getPosition().getRow()-1 and next_position.getCol()==self.getPosition().getCol()) or
         (next_position.getRow()==self.getPosition().getRow()-1 and next_position.getCol()==self.getPosition().getCol()+1) or
         (next_position.getRow()==self.getPosition().getRow()-1 and next_position.getCol()==self.getPosition().getCol()-1) or
         (next_position.getRow()==self.getPosition().getRow() and next_position.getCol()==self.getPosition().getCol()+1) or
         (next_position.getRow()==self.getPosition().getRow() and next_position.getCol()==self.getPosition().getCol()-1)):
        return True