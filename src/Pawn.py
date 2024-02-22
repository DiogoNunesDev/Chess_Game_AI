from Piece import Piece

class Pawn(Piece):
  
  def __init__(self, position, color, PlayerColor):
    super().__init__(position, color, PlayerColor)
    if (self.color):
      self.path = r"images\white-pawn.png"
      self.value = 100
      
    else:
      self.path = r"images\black-pawn.png"
      self.value = -100
    self.en_passant = None
    self.bitPosition = None
    self.starting_bitPosition = None
    self.board = "player_pawns" if self.color == self.PlayerColor else "enemy_pawns"
    self.piece_type = "Player_Pawn" if self.color == self.PlayerColor else "Enemy_Pawn"
    
  def checkEn_Passant(self, board, next_position):
    row = 3 if self.color==self.PlayerColor else 4
    direction = -1 if self.color==self.PlayerColor else 1
    if((self.position[0]==row) and (next_position[0] == row + direction) and (next_position[1] != self.position[1])):
      cell = board.getCell(row, next_position[1])
      if (cell.piece is not None) and isinstance(cell.piece, Pawn) and (cell.piece.en_passant == board.turn_counter - 1):
        return True
    return False


  def getAttackedSquares(self, board):
    self.attackedSquares = 0
    not_a_file = 0xfefefefefefefefe  # Excludes 'a' file
    not_h_file = 0x7f7f7f7f7f7f7f7f  # Excludes 'h' file
    attackedSquares = 0
    if self.color == board.PlayerColor:
      # 0x7f7f7f7f7f7f7f7f - binary: 0111 1111 ... (excludes first col) 
      #0xfefefefefefefefe - binary: 1111 1110 ... (excludes last col)
      
      # Attack moves
      attackedSquares |= ((self.bitPosition << 7) & not_h_file) #Attack left
      
      attackedSquares |= ((self.bitPosition << 9) & not_a_file) #Attack right
        
    else:
      # 0x7f7f7f7f7f7f7f7f - binary: 0111 1111 ... (excludes a col) 
      #0xfefefefefefefefe - binary: 1111 1110 ... (excludes h col)
      # Attack moves
      attackedSquares |= ((self.bitPosition >> 7) & not_a_file) #Attack right

      attackedSquares |= ((self.bitPosition >> 9) & not_h_file) #Attack left


    row = 2 if self.color == self.PlayerColor else 5
    for col_offset in [-1, 1]:
      diagonal_position = (row, self.position[1] + col_offset)
      if 0 <= diagonal_position[1] <= 7  and self.checkEn_Passant(board, diagonal_position):
        diagonal_position = board.translate_position_to_binary(diagonal_position[0], diagonal_position[1])
        attackedSquares |= diagonal_position
    
    self.attackedSquares |= attackedSquares

    return attackedSquares


  def getMoves(self, board):
    moves = 0
    if self.color == board.PlayerColor:
      if ((self.bitPosition << 8) & board.get_all_pieces_bitboard()) == 0:
        moves |= (self.bitPosition << 8) & 0xFFFFFFFFFFFFFFFF
      
        if self.starting_bitPosition == self.bitPosition:
          if ((self.bitPosition << 16) & board.get_all_pieces_bitboard()) == 0:
            #Advance 2 squares upwards
            moves |= (self.bitPosition << 16) & 0xFFFFFFFFFFFFFFFF
            self.en_passant = board.turn_counter
      # 0x7f7f7f7f7f7f7f7f - binary: 0111 1111 ... (excludes first col) 
      #0xfefefefefefefefe - binary: 1111 1110 ... (excludes last col)
      
      # Attack moves
      if (((self.bitPosition << 7) & 0x7f7f7f7f7f7f7f7f) & board.get_enemy_bitboard()) != 0:
        moves |= ((((self.bitPosition << 7) & 0x7f7f7f7f7f7f7f7f) & board.get_enemy_bitboard())) & 0xFFFFFFFFFFFFFFFF #Attack left
      
      if (((self.bitPosition << 9) & 0xfefefefefefefefe) & board.get_enemy_bitboard()) != 0:
        moves |= (((self.bitPosition << 9) & 0xfefefefefefefefe) & board.get_enemy_bitboard()) & 0xFFFFFFFFFFFFFFFF #Attack right
        
    else:
      if ((self.bitPosition >> 8) & board.get_all_pieces_bitboard()) == 0:
        moves |= self.bitPosition >> 8
      
        if self.starting_bitPosition == self.bitPosition:
          if ((self.bitPosition >> 16) & board.get_all_pieces_bitboard()) == 0:
            #Advance 2 squares downwards
            moves |= self.bitPosition >> 16
            self.en_passant = board.turn_counter
      # 0x7f7f7f7f7f7f7f7f - binary: 0111 1111 ... (excludes first col) 
      #0xfefefefefefefefe - binary: 1111 1110 ... (excludes last col)
      
      # Attack moves
      if (((self.bitPosition >> 7) & 0xfefefefefefefefe) & board.get_player_bitboard()) != 0:
        moves |= (((self.bitPosition >> 7) & 0xfefefefefefefefe) & board.get_player_bitboard()) & 0xFFFFFFFFFFFFFFFF #Attack right
        
      if (((self.bitPosition >> 9) & 0x7f7f7f7f7f7f7f7f) & board.get_player_bitboard()) != 0:
        moves |= (((self.bitPosition >> 9) & 0x7f7f7f7f7f7f7f7f) & board.get_player_bitboard()) & 0xFFFFFFFFFFFFFFFF #Attack left


    row = 2 if self.color == self.PlayerColor else 5
    for col_offset in [-1, 1]:
      diagonal_position = (row, self.position[1] + col_offset)
      if 0 <= diagonal_position[1] <= 7  and self.checkEn_Passant(board, diagonal_position):
        diagonal_position = board.translate_position_to_binary(diagonal_position[0], diagonal_position[1])
        moves |= diagonal_position & 0xFFFFFFFFFFFFFFFF
    
    self.moves = moves
    return self.moves
  
  
  def getPossibleMoves(self, board):
    possible_moves = set()
    isPinned, move = board.isPiecePinned(self, self.color)
    if not isPinned:
      print("ok")
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
    pawn = Pawn(self.position, self.color, self.PlayerColor)
    pawn.bitPosition = self.bitPosition
    pawn.starting_bitPosition = self.starting_bitPosition
    pawn.attackedSquares = self.attackedSquares
    pawn.hasMoved = self.hasMoved
    pawn.moves = self.moves
    pawn.en_passant = self.en_passant
    
    return pawn
      