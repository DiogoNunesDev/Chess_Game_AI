class Position:
  
  def __init__(self, row, col):
    self.row = row
    self.col = col    
    
  def __str__(self):
    return f'Row: {self.row}, Col: {self.col}'
  
  def __hash__(self):
        return hash((self.row, self.col))

  def __eq__(self, other):
    return isinstance(other, Position) and self.row == other.row and self.col == other.col
  
  