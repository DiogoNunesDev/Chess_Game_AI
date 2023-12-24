from Piece import Piece
from Position import Position

class Cell:
  
  def __init__(self, position, piece):
    self.position = position
    self.piece = piece
    
  def __str__(self):
    return f'Cell: Position->[Row:{self.position.row}, Col: {self.position.col}], Piece: {self.piece}'
  
  def getPiece(self):
    return self.piece
  
  def setPiece(self, piece):
    self.piece = piece
  
  def getPosition(self):
    return self.position