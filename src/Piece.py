class Piece:
  _id_counter = 0  # Class-level attribute for unique ID generation

  def __init__(self, position, color, PlayerColor):
    self.id = Piece._id_counter  # Assign a unique ID to each piece instance
    Piece._id_counter += 1       # Increment ID counter for next piece

    self.color = color
    self.position = position
    self.path = None
    self.PlayerColor = PlayerColor
    self.hasMoved = False
    self.moves = 0
    self.attackedSquares = 0
    
  def __eq__(self, other):
    if not isinstance(other, Piece):
      return NotImplemented
    return self.id == other.id  # Equality now based on unique ID

  def __hash__(self):
    return hash(self.id)  # Hash based on unique ID

  def __str__(self):
    return f'Position: {self.position}, Color: {self.color}, Path: {self.path}'

  
  
  