from Piece import Piece

class Queen(Piece):
  
  def __init__(self, position, color, PlayerColor):
    super().__init__(position, color, PlayerColor)
    if (self.color):
      self.path = r"images\white-queen.png"
      self.value = 900
      
    else:
      self.path = r"images\black-queen.png"
      self.value = -900
    self.bitPosition = None
    self.board = "player_queen" if self.color == self.PlayerColor else "enemy_queen"
    self.piece_type = "Queen"



  def getAttackedSquares(self, board):
    self.attackedSquares = 0b0000000000000000000000000000000000000000000000000000000000000000
    position = self.bitPosition

    # Masks to prevent wrapping around the board
    top_row_mask = 0xFF00000000000000 # Excludes first rank
    bottom_row_mask = 0x00000000000000FF # Excludes last rank
    not_a_file = 0xfefefefefefefefe  # Excludes 'a' file
    not_h_file = 0x7f7f7f7f7f7f7f7f  # Excludes 'h' file
    a_file_mask = 0x0101010101010101
    h_file_mask = 0x8080808080808080
    
    all_pieces_bitboard = board.get_all_pieces_bitboard()
    attackedSquares = 0b0000000000000000000000000000000000000000000000000000000000000000
    
    upper_left_moves = position
    upper_right_moves = position
    lower_left_moves = position
    lower_right_moves = position
    upward_moves = position
    downward_moves = position
    rightward_moves = position
    leftward_moves = position

    up_r_flag = True
    up_l_flag = True
    dn_r_flag = True
    dn_l_flag = True
    up_flag = True
    dn_flag = True
    r_flag = True
    l_flag = True
    
    for i in range(1, 8):
      if (position & top_row_mask) == 0:
      
        if up_r_flag and ((position & h_file_mask) == 0 and (position & top_row_mask) == 0): 
          upper_right_moves = (position << 9*i) & not_a_file
          if ((upper_right_moves & all_pieces_bitboard) != 0):
            up_r_flag = False
            attackedSquares |= upper_right_moves
          else:
            attackedSquares |= upper_right_moves
            if (upper_right_moves & h_file_mask) != 0 or (upper_right_moves & top_row_mask) != 0:
              up_r_flag = False

        if up_l_flag and ((position & a_file_mask) == 0 and (position & top_row_mask) == 0):
          upper_left_moves = (position << 7*i) & not_h_file
          if ((upper_left_moves & all_pieces_bitboard) != 0):
            up_l_flag = False
            attackedSquares |= upper_left_moves
          else:
            attackedSquares |= upper_left_moves
            if (upper_left_moves & a_file_mask) != 0 or (upper_left_moves & top_row_mask) != 0:
              up_l_flag = False
        
        if up_flag and (position & top_row_mask) == 0:
          upward_moves = (position << (8*i))
          if ((upward_moves & all_pieces_bitboard) != 0):
            up_flag = False
            attackedSquares |= upward_moves
          else:
            attackedSquares |= upward_moves
            if (upward_moves & top_row_mask) != 0:
              up_flag = False
        
      if (position & bottom_row_mask) == 0:
          
        if dn_r_flag and ((position & h_file_mask) == 0 and (position & bottom_row_mask) == 0):
          lower_right_moves = (position >> 7*i) & not_a_file
          if ((lower_right_moves & all_pieces_bitboard) != 0):
            dn_r_flag = False
            attackedSquares |= lower_right_moves
          else:
            attackedSquares |= lower_right_moves
            if (lower_right_moves & h_file_mask) != 0 or (lower_right_moves & bottom_row_mask) != 0:
              dn_r_flag = False
          
        if dn_l_flag and ((position & a_file_mask) == 0 and (position & bottom_row_mask) == 0):
          lower_left_moves = (position >> 9*i) & not_h_file
          if ((lower_left_moves & all_pieces_bitboard) != 0):
            dn_l_flag = False
            attackedSquares |= lower_left_moves
          else:
            attackedSquares |= lower_left_moves
            if (lower_left_moves & a_file_mask) != 0 or (lower_left_moves & bottom_row_mask) != 0:
              dn_l_flag = False

        if dn_flag and (position & bottom_row_mask) == 0:
          downward_moves = (position >> (8*i))
          if ((downward_moves & all_pieces_bitboard) != 0):
            dn_flag = False
            attackedSquares |= downward_moves
          else:
            attackedSquares |= downward_moves
            if (downward_moves & bottom_row_mask) != 0:
              dn_flag = False
            
      if (position & 0x8080808080808080) == 0:
        if r_flag and (position & h_file_mask) == 0:
          rightward_moves = (position << i)
          if ((rightward_moves & all_pieces_bitboard) != 0):
            r_flag = False
            attackedSquares |= rightward_moves
          else:
            attackedSquares |= rightward_moves
            if (rightward_moves & h_file_mask) != 0:
              r_flag = False
        
      if (position & 0x0101010101010101) == 0:
        if l_flag and (position & a_file_mask) == 0:
          leftward_moves = (position >> i)
          if ((leftward_moves & all_pieces_bitboard) != 0):
            l_flag = False
            attackedSquares |= leftward_moves
          else:
            attackedSquares |= leftward_moves
            if (leftward_moves & a_file_mask) != 0:
              l_flag = False
        

      attackedSquares |= (upper_left_moves | upper_right_moves | lower_left_moves | lower_right_moves | upward_moves | downward_moves | leftward_moves | rightward_moves)

    self.attackedSquares = attackedSquares & (position ^ 0xFFFFFFFFFFFFFFFF)
    
    return self.attackedSquares 
  
  def getMoves(self, board):
    position = self.bitPosition

    # Masks to prevent wrapping around the board
    top_row_mask = 0xFF00000000000000 # Excludes first rank
    bottom_row_mask = 0x00000000000000FF # Excludes last rank
    not_a_file = 0xfefefefefefefefe  # Excludes 'a' file
    not_h_file = 0x7f7f7f7f7f7f7f7f  # Excludes 'h' file
    a_file_mask = 0x0101010101010101
    h_file_mask = 0x8080808080808080
    
    enemyTeam_board_bitboard = board.get_enemy_bitboard() if self.color == board.PlayerColor else board.get_player_bitboard()
    team_board_bitboard =  board.get_player_bitboard() if self.color == board.PlayerColor else board.get_enemy_bitboard()
    all_pieces_bitboard = board.get_all_pieces_bitboard()
    moves = 0
    
    upper_left_moves = position
    upper_right_moves = position
    lower_left_moves = position
    lower_right_moves = position
    upward_moves = position
    downward_moves = position
    rightward_moves = position
    leftward_moves = position

    up_r_flag = True
    up_l_flag = True
    dn_r_flag = True
    dn_l_flag = True
    up_flag = True
    dn_flag = True
    r_flag = True
    l_flag = True
    
    for i in range(1, 8):
      if (position & top_row_mask) == 0:
      
        if up_r_flag and ((position & h_file_mask) == 0 and (position & top_row_mask) == 0): 
          upper_right_moves = (position << 9*i) & not_a_file
          if ((upper_right_moves & all_pieces_bitboard) != 0):
            up_r_flag = False
            if (upper_right_moves & enemyTeam_board_bitboard) != 0:
              moves |= upper_right_moves
          else:
            moves |= upper_right_moves
            if (upper_right_moves & h_file_mask) != 0 or (upper_right_moves & top_row_mask) != 0:
              up_r_flag = False

        if up_l_flag and ((position & a_file_mask) == 0 and (position & top_row_mask) == 0):
          upper_left_moves = (position << 7*i) & not_h_file
          if ((upper_left_moves & all_pieces_bitboard) != 0):
            up_l_flag = False
            if (upper_left_moves & enemyTeam_board_bitboard) != 0:
              moves |= upper_left_moves
          else:
            moves |= upper_left_moves
            if (upper_left_moves & a_file_mask) != 0 or (upper_left_moves & top_row_mask) != 0:
              up_l_flag = False
        
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
        
      if (position & bottom_row_mask) == 0:
          
        if dn_r_flag and ((position & h_file_mask) == 0 and (position & bottom_row_mask) == 0):
          lower_right_moves = (position >> 7*i) & not_a_file
          if ((lower_right_moves & all_pieces_bitboard) != 0):
            dn_r_flag = False
            if (lower_right_moves & enemyTeam_board_bitboard) != 0:
              moves |= lower_right_moves
          else:
            moves |= lower_right_moves
            if (lower_right_moves & h_file_mask) != 0 or (lower_right_moves & bottom_row_mask) != 0:
              dn_r_flag = False
          
        if dn_l_flag and ((position & a_file_mask) == 0 and (position & bottom_row_mask) == 0):
          lower_left_moves = (position >> 9*i) & not_h_file
          if ((lower_left_moves & all_pieces_bitboard) != 0):
            dn_l_flag = False
            if (lower_left_moves & enemyTeam_board_bitboard) != 0:
              moves |= lower_left_moves
          else:
            moves |= lower_left_moves
            if (lower_left_moves & a_file_mask) != 0 or (lower_left_moves & bottom_row_mask) != 0:
              dn_l_flag = False

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
            
      if (position & 0x8080808080808080) == 0:
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
        
      if (position & 0x0101010101010101) == 0:
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
        

      moves |= (upper_left_moves | upper_right_moves | lower_left_moves | lower_right_moves | upward_moves | downward_moves | leftward_moves | rightward_moves)

    self.moves = (moves & (team_board_bitboard ^ 0xFFFFFFFFFFFFFFFF)) & (position ^ 0xFFFFFFFFFFFFFFFF)
    
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
    queen = Queen(self.position, self.color, self.PlayerColor)
    queen.bitPosition = self.bitPosition
    queen.attackedSquares = self.attackedSquares
    queen.hasMoved = self.hasMoved
    queen.moves = self.moves
    return queen