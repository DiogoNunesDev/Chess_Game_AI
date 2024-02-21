class Cell:
  
  def __init__(self, row, col, piece):
    self.position = (row, col)
    self.piece = piece
    self.bitPosition = 1 << ((7 - row) * 8 + col)
    self.precomputed_AttackMap = {}
    self.initialize_precomputed_AttackMap()
    
  def __str__(self):
    if self.piece:
      return f'Cell: Position->[Row:{self.position[0]}, Col: {self.position[1]}], Piece: {self.piece.__str__()}'
    else:
      return f'Cell: Position->[Row:{self.position[0]}, Col: {self.position[1]}], Piece: None'
   
  def  initialize_precomputed_AttackMap(self):
    
    """
      KING ATTACK MAP
    """
    self.precomputed_AttackMap['king'] = 0
    not_a_file = 0xfefefefefefefefe # Excludes 'a' file
    not_h_file = 0x7f7f7f7f7f7f7f7f # Excludes 'h' file
    top_row_mask = 0xFF00000000000000 # Excludes first rank
    bottom_row_mask = 0x00000000000000FF # Excludes last rank
    upwards_moves = 0
    downwards_moves = 0
    
    if (self.bitPosition & top_row_mask) != 0:
      upwards_moves = self.bitPosition
    else:
      upwards_moves = (self.bitPosition << 8) | ((self.bitPosition << 9) & not_a_file) | ((self.bitPosition << 7) & not_h_file)
      
    if (self.bitPosition & bottom_row_mask) != 0:
      downwards_moves = self.bitPosition
    else:
      downwards_moves = (self.bitPosition >> 8) | ((self.bitPosition >> 7) & not_a_file) | ((self.bitPosition >> 9) & not_h_file)
    
    # Possible moves
    self.precomputed_AttackMap['King'] = (((self.bitPosition << 1) & not_a_file) | ((self.bitPosition >> 1) & not_h_file) | upwards_moves | downwards_moves) & (self.bitPosition ^ 0xFFFFFFFFFFFFFFFF) 

    """
      KNIGHT ATTACK MAP
    """
    self.precomputed_AttackMap['Knight'] = 0
        # Masks to prevent wrapping around the board
    not_ab_file = 0xfcfcfcfcfcfcfcfc  # Excludes 'a' and 'b' files
    not_gh_file = 0x3f3f3f3f3f3f3f3f  # Excludes 'g' and 'h' files

    # Possible moves
    left_moves = ((self.bitPosition << 6) & not_gh_file) | ((self.bitPosition << 15) & not_h_file) | ((self.bitPosition >> 10) & not_gh_file) | ((self.bitPosition >> 17) & not_h_file)
        
    right_moves = ((self.bitPosition << 10) & not_ab_file) | ((self.bitPosition << 17) & not_a_file) | ((self.bitPosition >> 6) & not_ab_file) | ((self.bitPosition >> 15) & not_ab_file)

    self.precomputed_AttackMap['Knight'] = (left_moves | right_moves)
    
    """
      PLAYER PAWN ATTACK MAP
    """
    self.precomputed_AttackMap['Player_Pawn'] = 0
    self.precomputed_AttackMap['Player_Pawn'] |= ((self.bitPosition << 7) & not_h_file) #Attack left
      
    self.precomputed_AttackMap['Player_Pawn'] |= ((self.bitPosition << 9) & not_a_file) #Attack right
       
    """
      AI BOT PAWN ATTACK MAP
    """
    self.precomputed_AttackMap['Enemy_Pawn'] = 0
    self.precomputed_AttackMap['Enemy_Pawn'] |= ((self.bitPosition >> 7) & not_a_file) #Attack right

    self.precomputed_AttackMap['Enemy_Pawn'] |= ((self.bitPosition >> 9) & not_h_file) #Attack left
    
    
    
    
   
   
  def copy(self):
    if self.piece is not None:
      new_piece = self.piece.copy()
      return Cell(self.position[0], self.position[1], new_piece)
    else:
      return Cell(self.position[0], self.position[1], None)

