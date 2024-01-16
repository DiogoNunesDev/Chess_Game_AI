from Position import Position

class Piece:
  
  def __init__(self, position, isTeam):
    self.position = position
    self.isTeam = isTeam
    self.name= "None"
    self.hasMoved = False
    
  def getPosition(self):
    return self.position
  
  def setPosition(self, position):
    self.position = position
    
  def getName(self):
    return self.name
  
  def getIsTeam(self):
    return self.isTeam
  
  def getHasMoved(self):
    return self.hasMoved
  
  def setHasMoved(self, bool):
    self.hasMoved = bool
  
  def __str__(self):
    return f'Piece: Position->[Row:{self.position.row}, Col: {self.position.col}],  isTeam: {self.isTeam}'
  
  def __eq__(self, other):
    return self.position==other.position and self.isTeam==other.isTeam and self.name==other.name and self.hasMoved==other.hasMoved
  
  def move(self, board, next_position):
    board.getCell(self.position).setPiece(None)
    board.getCell(next_position).setPiece(self)
    self.setPosition(next_position)
    if not self.hasMoved:
      self.setHasMoved(True)
    
      
  def checkMove(self, board, next_position):
    if (board.getCell(next_position).getPiece() is None):
      return True
    elif (board.getCell(next_position).getPiece().isTeam != self.isTeam):
      return True
    return False
      
  def getPossibleMoves(self, board):
    pass
  
  