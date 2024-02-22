from Piece import Piece

class Knight(Piece):
  
  def __init__(self, position, color, PlayerColor):
    super().__init__(position, color, PlayerColor)
    if (self.color):
      self.path = r"images\white-knight.png"
      self.value = 300
    else:
      self.path = r"images\black-knight.png"
      self.value = -300
    self.bitPosition = None
    self.board = "player_knights" if self.color == self.PlayerColor else "enemy_knights"
    self.piece_type = "Knight"

    
  def getAttackedSquares(self, board):
    self.attackedSquares = 0
    position = self.bitPosition

    # Masks to prevent wrapping around the board
    not_a_file = 0xfefefefefefefefe  # Excludes 'a' file
    not_ab_file = 0xfcfcfcfcfcfcfcfc  # Excludes 'a' and 'b' files
    not_h_file = 0x7f7f7f7f7f7f7f7f  # Excludes 'h' file
    not_gh_file = 0x3f3f3f3f3f3f3f3f  # Excludes 'g' and 'h' files

    # Possible moves
    left_moves = ((position << 6) & not_gh_file) | ((position << 15) & not_h_file) | ((position >> 10) & not_gh_file) | ((position >> 17) & not_h_file)
        
    right_moves = ((position << 10) & not_ab_file) | ((position << 17) & not_a_file) | ((position >> 6) & not_ab_file) | ((position >> 15) & not_ab_file)

    self.attackedSquares = (left_moves | right_moves)

    return self.attackedSquares
  
  def getMoves(self, board):
    position = self.bitPosition

    # Masks to prevent wrapping around the board
    not_a_file = 0xfefefefefefefefe  # Excludes 'a' file
    not_ab_file = 0xfcfcfcfcfcfcfcfc  # Excludes 'a' and 'b' files
    not_h_file = 0x7f7f7f7f7f7f7f7f  # Excludes 'h' file
    not_gh_file = 0x3f3f3f3f3f3f3f3f  # Excludes 'g' and 'h' files

    # Possible moves
    left_moves = ((position << 6) & not_gh_file) | ((position << 15) & not_h_file) | ((position >> 10) & not_gh_file) | ((position >> 17) & not_h_file)
        
    right_moves = ((position << 10) & not_ab_file) | ((position << 17) & not_a_file) | ((position >> 6) & not_ab_file) | ((position >> 15) & not_ab_file)

    self.moves = (left_moves | right_moves) & (board.get_player_bitboard() ^ 0xFFFFFFFFFFFFFFFF) if self.color == board.PlayerColor else (left_moves | right_moves) & (board.get_enemy_bitboard() ^ 0xFFFFFFFFFFFFFFFF)
    # Check for valid moves and add to the set
    
    #moves = board.translate_bitboard_to_positions(moves)

    return self.moves
   
  def getPossibleMoves(self, board):
    possible_moves = set()
    isPinned, move = board.isPiecePinned(self, self.color)
    if not isPinned:
      moves = self.getMoves(board)
      moves = board.translate_bitboard_to_positions(moves)
      if board.kingInCheck[self.color]:
        for next_position in set(moves):
          if (not board.checkMove(self, next_position)):
            possible_moves.add(next_position)
      else:
        return moves
    else:
      if move in moves:
        possible_moves.add(move)
              
    return possible_moves
  
  def copy(self):
    knight = Knight(self.position, self.color, self.PlayerColor)
    knight.bitPosition = self.bitPosition
    knight.attackedSquares = self.attackedSquares
    knight.hasMoved = self.hasMoved
    knight.moves = self.moves
    return knight
  