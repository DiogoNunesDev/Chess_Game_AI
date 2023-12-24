from Piece import Piece

class Bishop(Piece):
  
  def __init__(self, position, isWhite):
    super().__init__(position, isWhite)
    if (self.isWhite):
      self.name = r"images\white-bishop.png"
    else:
      self.name = r"images\black-bishop.png"
      
  def __str__(self):
    return f'Piece: Position->[Row:{self.position.row}, Col: {self.position.col}], isWhite: {self.isWhite}, Name: {self.name}'
  
