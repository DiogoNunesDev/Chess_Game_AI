from Piece import Piece
from Rook import Rook

class King(Piece):
  
  def __init__(self, position, color, PlayerColor):
    super().__init__(position, color, PlayerColor)
    if (self.color):
      self.path = r"images\white-king.png"
      self.value = float('inf')
    else:
      self.path = r"images\black-king.png"
      self.value = float('-inf')
      
    self.isInCheck = False
    self.bitPosition = None
    self.bitboard = "player_king" if self.color == self.PlayerColor else "enemy_king"
  
  
  def isPathClearForCastle(self, board, row, direction):
    col_start = 4
    col_end = 7 if direction > 0 else 0
    step = 1 if direction > 0 else -1

    for col in range(col_start, col_end, step):
      if col == 4:
        if board.isSquareUnderAttack((row, col), self.color):
          return False
      elif board.getCell(row, col).piece is not None or board.isSquareUnderAttack((row, col), self.color):
        return False

    return True

  def checkCastle(self, board, next_position):
    if not self.hasMoved and next_position[0] == self.position[0]:
      row = self.position[0]
      direction = 1 if next_position[1] > self.position[1] else -1
      path_clear = self.isPathClearForCastle(board, row, direction)
      rook_col = 7 if direction > 0 else 0
      rook = board.getCell(row, rook_col).piece
            
      return path_clear and isinstance(rook, Rook) and not rook.hasMoved

  def getAttackedSquares(self, board):
    self.attackedSquares = 0
    position = self.bitPosition

    # Masks to prevent wrapping around the board
    not_a_file = 0xfefefefefefefefe # Excludes 'a' file
    not_h_file = 0x7f7f7f7f7f7f7f7f # Excludes 'h' file
    top_row_mask = 0xFF00000000000000 # Excludes first rank
    bottom_row_mask = 0x00000000000000FF # Excludes last rank
    upwards_moves = 0
    downwards_moves = 0
    
    if (position & top_row_mask) != 0:
      upwards_moves = position
    else:
      upwards_moves = (position << 8) | ((position << 9) & not_a_file) | ((position << 7) & not_h_file)
      
    if (position & bottom_row_mask) != 0:
      downwards_moves = position
    else:
      downwards_moves = (position >> 8) | ((position >> 7) & not_a_file) | ((position >> 9) & not_h_file)
    
    # Possible moves
    attackedSquares = (((position << 1) & not_a_file) | ((position >> 1) & not_h_file) | upwards_moves | downwards_moves) & (position ^ 0xFFFFFFFFFFFFFFFF) 
    self.attackedSquares = attackedSquares

    return self.attackedSquares

  def getMoves(self, board):
    position = self.bitPosition

    # Masks to prevent wrapping around the board
    not_a_file = 0xfefefefefefefefe # Excludes 'a' file
    not_h_file = 0x7f7f7f7f7f7f7f7f # Excludes 'h' file
    top_row_mask = 0xFF00000000000000 # Excludes first rank
    bottom_row_mask = 0x00000000000000FF # Excludes last rank
    upwards_moves = 0
    downwards_moves = 0
    
    if (position & top_row_mask) != 0:
      upwards_moves = position
    else:
      upwards_moves = (position << 8) | ((position << 9) & not_a_file) | ((position << 7) & not_h_file)
      
    if (position & bottom_row_mask) != 0:
      downwards_moves = position
    else:
      downwards_moves = (position >> 8) | ((position >> 7) & not_a_file) | ((position >> 9) & not_h_file)
    
    # Possible moves
    moves = (((position << 1) & not_a_file) | ((position >> 1) & not_h_file) | upwards_moves | downwards_moves) & (position ^ 0xFFFFFFFFFFFFFFFF) 
    self.moves = moves & (board.get_player_bitboard() ^ 0xFFFFFFFFFFFFFFFF) if self.color == board.PlayerColor else moves & (board.get_enemy_bitboard() ^ 0xFFFFFFFFFFFFFFFF)

    return self.moves
  
  
  def getPossibleMoves(self, board):
    possible_moves = set()
    moves = self.getMoves(board)
    moves = board.translate_bitboard_to_positions(moves)
    for next_position in set(moves):
      if (not board.checkMove(self, next_position)):
        possible_moves.add(next_position)
        
    # Include castling moves if applicable
    if self.checkCastle(board, (self.position[0], 2)):  # Queenside
      possible_moves.add((self.position[0], 2))
    if self.checkCastle(board, (self.position[0], 6)):  # Kingside
      possible_moves.add((self.position[0], 6))

                
    return possible_moves
     
  def copy(self):
    king = King(self.position, self.color, self.PlayerColor)
    king.bitPosition = self.bitPosition
    king.attackedSquares = self.attackedSquares
    king.hasMoved = self.hasMoved
    king.moves = self.moves
    king.isInCheck = self.isInCheck
    return king