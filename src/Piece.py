from Position import Position

class Piece:
  
  def __init__(self, position, isWhite):
    self.position = position
    self.isWhite = isWhite
    self.name= "None"
    
  def getPosition(self):
    return self.position
  
  def setPosition(self, position):
    self.position = position
    
  def getName(self):
    return self.name
  
  def __str__(self):
    return f'Piece: Position->[Row:{self.position.row}, Col: {self.position.col}],  isWhite: {self.isWhite}'
  
  def move(self, board, next_position):
    if self.checkMove(board, next_position):
      board.getCell(self.position).setPiece(None)
      board.getCell(next_position).setPiece(self)
      self.setPosition(next_position)
      
  def checkMove(self, board, next_position):
    if (board.getCell(next_position).getPiece() == None):
      print('None')
      return True
    elif (board.getCell(next_position).getPiece().isWhite != self.isWhite):
      print('dif color')
      return True
    return False
      


  
  