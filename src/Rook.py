from Piece import Piece

class Rook(Piece):
  
  def __init__(self, position, color, PlayerColor):
    super().__init__(position, color, PlayerColor)
    if (self.color):
      self.path = r"images\white-rook.png"
      self.value = 500
    else:
      self.path = r"images\black-rook.png"
      self.value = -500
    self.bitPosition = None
    self.board = "player_rooks" if self.color == self.PlayerColor else "enemy_rooks"
    self.piece_type = "Rook"

  
  def getAttackedSquares(self, board):
    self.attackedSquares = 0b0000000000000000000000000000000000000000000000000000000000000000
    position = self.bitPosition
    
    # Masks to prevent wrapping around the board
    top_row_mask = 0xFF00000000000000 # Excludes first rank
    bottom_row_mask = 0x00000000000000FF # Excludes last rank
    a_file_mask = 0x0101010101010101
    h_file_mask = 0x8080808080808080
    
    all_pieces_bitboard = board.get_all_pieces_bitboard()
    attackedSquares= 0b0000000000000000000000000000000000000000000000000000000000000000
    
    upward_moves = position
    downward_moves = position
    rightward_moves = position
    leftward_moves = position
    
    up_flag = True
    dn_flag = True
    r_flag = True
    l_flag = True
    
    for i in range(1, 8):

      if up_flag and (position & top_row_mask) == 0:
        upward_moves = (position << (8*i))
        if ((upward_moves & all_pieces_bitboard) != 0):
          up_flag = False
          attackedSquares |= upward_moves
        else:
          attackedSquares |= upward_moves
          if (upward_moves & top_row_mask) != 0:
            up_flag = False
      
      if dn_flag and (position & bottom_row_mask) == 0:
        downward_moves = (position >> (8*i))
        if ((downward_moves & all_pieces_bitboard) != 0):
          dn_flag = False
          attackedSquares |= downward_moves
        else:
          attackedSquares |= downward_moves
          if (downward_moves & bottom_row_mask) != 0:
            dn_flag = False
            
      if r_flag and (position & h_file_mask) == 0:
        rightward_moves = (position << i)
        if ((rightward_moves & all_pieces_bitboard) != 0):
          r_flag = False
          attackedSquares |= rightward_moves
        else:
          attackedSquares |= rightward_moves
          if (rightward_moves & h_file_mask) != 0:
            r_flag = False
      
      if l_flag and (position & a_file_mask) == 0:
        leftward_moves = (position >> i)
        if ((leftward_moves & all_pieces_bitboard) != 0):
          l_flag = False
          attackedSquares |= leftward_moves
        else:
          attackedSquares |= leftward_moves
          if (leftward_moves & a_file_mask) != 0:
            l_flag = False
            
      
    
    self.attackedSquares = attackedSquares & (position ^ 0xFFFFFFFFFFFFFFFF)
    
    return self.attackedSquares
  
              
  def getMoves(self, board):
    position = self.bitPosition
    
    # Masks to prevent wrapping around the board
    top_row_mask = 0xFF00000000000000 # Excludes first rank
    bottom_row_mask = 0x00000000000000FF # Excludes last rank
    a_file_mask = 0x0101010101010101
    h_file_mask = 0x8080808080808080
    
    all_pieces_bitboard = board.get_all_pieces_bitboard()
    enemyTeam_board_bitboard = board.get_enemy_bitboard() if self.color == board.PlayerColor else board.get_player_bitboard()
    team_board_bitboard =  board.get_player_bitboard() if self.color == board.PlayerColor else board.get_enemy_bitboard()
    moves = 0
    
    upward_moves = position
    downward_moves = position
    rightward_moves = position
    leftward_moves = position
    
    up_flag = True
    dn_flag = True
    r_flag = True
    l_flag = True
    
    for i in range(1, 8):

      if up_flag and (position & top_row_mask) == 0:
        upward_moves = (position << (8*i))
        if ((upward_moves & all_pieces_bitboard) != 0):
          up_flag = False
          if (upward_moves & enemyTeam_board_bitboard) != 0:
            moves |= upward_moves
        else:
          moves |= upward_moves
          if (upward_moves & top_row_mask) != 0:
            up_flag = False
      
      if dn_flag and (position & bottom_row_mask) == 0:
        downward_moves = (position >> (8*i))
        if ((downward_moves & all_pieces_bitboard) != 0):
          dn_flag = False
          if (downward_moves & enemyTeam_board_bitboard) != 0:
            moves |= downward_moves
        else:
          moves |= downward_moves
          if (downward_moves & bottom_row_mask) != 0:
            dn_flag = False
            
      if r_flag and (position & h_file_mask) == 0:
        rightward_moves = (position << i)
        if ((rightward_moves & all_pieces_bitboard) != 0):
          r_flag = False
          if (rightward_moves & enemyTeam_board_bitboard) != 0:
            moves |= rightward_moves
        else:
          moves |= rightward_moves
          if (rightward_moves & h_file_mask) != 0:
            r_flag = False
      
      if l_flag and (position & a_file_mask) == 0:
        leftward_moves = (position >> i)
        if ((leftward_moves & all_pieces_bitboard) != 0):
          l_flag = False
          if (leftward_moves & enemyTeam_board_bitboard) != 0:
            moves |= leftward_moves
        else:
          moves |= leftward_moves
          if (leftward_moves & a_file_mask) != 0:
            l_flag = False
            
      
    
    self.moves = (moves & (team_board_bitboard ^ 0xFFFFFFFFFFFFFFFF)) & (position ^ 0xFFFFFFFFFFFFFFFF)
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
      if move:
        possible_moves.add(move)
              
    return possible_moves
  
  def copy(self):
    rook = Rook(self.position, self.color, self.PlayerColor)
    rook.bitPosition = self.bitPosition
    rook.attackedSquares = self.attackedSquares
    rook.hasMoved = self.hasMoved
    rook.moves = self.moves
    return rook