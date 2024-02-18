class Cell:
  
  def __init__(self, row, col, piece):
    self.position = (row, col)
    self.piece = piece
    
  def __str__(self):
    if self.piece:
      return f'Cell: Position->[Row:{self.position[0]}, Col: {self.position[1]}], Piece: {self.piece.__str__()}'
    else:
      return f'Cell: Position->[Row:{self.position[0]}, Col: {self.position[1]}], Piece: None'
    
  def copy(self):
    if self.piece is not None:
      new_piece = self.piece.copy()
      return Cell(self.position[0], self.position[1], new_piece)
    else:
      return Cell(self.position[0], self.position[1], None)

