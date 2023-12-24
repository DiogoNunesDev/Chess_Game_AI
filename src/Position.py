class Position:
  
  def __init__(self, row, col):
    self.row = row
    self.col = col    
    
  def getRow(self):
    return self.row
  
  def getCol(self):
    return self.col
  
  def __str__(self):
    return f'Row: {self.row}, Col: {self.col}'
  
  