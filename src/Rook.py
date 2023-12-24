from Piece import Piece

class Rook(Piece):
  
  def __init__(self, position, isWhite):
    super().__init__(position, isWhite)
    if (self.isWhite):
      self.name = r"images\white-rook.png"
    else:
      self.name = r"images\black-rook.png"
      
  def __str__(self):
    return f'Piece: Position->[Row:{self.position.row}, Col: {self.position.col}], isWhite: {self.isWhite}, Name: {self.name}'
  
