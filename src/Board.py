from copy import deepcopy
import math

import pygame
from Cell import Cell
from Bishop import Bishop
from King import King
from Knight import Knight
from Pawn import Pawn
from Queen import Queen
from Rook import Rook


class Board:
  
  def __init__(self, PlayerColor):
    self.cells = [[None for _ in range(8)] for _ in range(8)]
    for row in range(8):
      for col in range(8):
        self.cells[row][col] = Cell(row, col, None)
    
    # Bitboards for initial position for player and enemy
    self.bit_boards={
      'player_pawns': 0b0000000000000000000000000000000000000000000000001111111100000000,
      'player_rooks': 0b0000000000000000000000000000000000000000000000000000000010000001,
      'player_knights': 0b0000000000000000000000000000000000000000000000000000000001000010,
      'player_bishops': 0b0000000000000000000000000000000000000000000000000000000000100100,
      'player_queen': 0b0000000000000000000000000000000000000000000000000000000000001000,
      'player_king':  0b0000000000000000000000000000000000000000000000000000000000010000,

      'enemy_pawns': 0b0000000011111111000000000000000000000000000000000000000000000000,
      'enemy_rooks': 0b1000000100000000000000000000000000000000000000000000000000000000,
      'enemy_knights': 0b0100001000000000000000000000000000000000000000000000000000000000,
      'enemy_bishops': 0b0010010000000000000000000000000000000000000000000000000000000000,
      'enemy_queen': 0b0000100000000000000000000000000000000000000000000000000000000000,
      'enemy_king': 0b0001000000000000000000000000000000000000000000000000000000000000,
    }
    
    self.piece_position_values={
      'player_pawns': [100, 100, 100, 100, 100, 100, 100, 100, 50, 50, 50, 50, 50, 50, 50, 50, 10, 10, 20, 30, 30, 20, 10, 10, 5, 5, 10, 25, 25, 10, 5, 5,
                      0, 0, 0, 20, 20, 0, 0, 0, 5, -5, -10, 0, 0, -10, -5, 5, 5, 10, 10, -20, -20, 10, 10, 5, 0, 0, 0, 0, 0, 0, 0, 0 ],
      
      'player_rooks': [0, 0, 0, 5, 5, 0, 0, 0, 5, 10, 10, 10, 10, 10, 10, 5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5,
                      -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, 5, 10, 10, 10, 10, 10, 10, 5, 0, 0, 0, 0, 0, 0, 0, 0],
      
      'player_knights': [-50, -40, -30, -30, -30, -30, -40, -50,
                         -40, -20, 0, 5, 5, 0, -20, -40,
                         -30, 5, 10, 15, 15, 10, 5, -30, 
                         -30, 0, 15, 20, 20, 15, 0, -30, 
                        -30, 5, 15, 20, 20, 15, 5, -30, 
                        -30, 0, 10, 15, 15, 10, 0, -30,
                        -40, -20, 0, 0, 0, 0, -20, -40,
                        -50, -40, -30, -30, -30, -30, -40, -50],
      
     'player_bishops': [-20, -10, -10, -10, -10, -10, -10, -20, -10, 5, 0, 0, 0, 0, 5, -10, -10, 10, 10, 10, 10, 10, 10, -10, -10, 0, 10, 10, 10, 10, 0, -10,
                      -10, 5, 5, 10, 10, 5, 5, -10, -10, 0, 5, 10, 10, 5, 0, -10, -10, 0, 0, 0, 0, 0, 0, -10, -20, -10, -10, -10, -10, -10, -10, -20],
      
      'player_queen': [-20, -10, -10, -5, -5, -10, -10, -20, -10, 0, 5, 0, 0, 0, 0, -10, -10, 5, 5, 5, 5, 5, 0, -10, 0, 0, 5, 5, 5, 5, 0, -5,
                      -5, 0, 5, 5, 5, 5, 0, -5, -10, 0, 5, 5, 5, 5, 0, -10, -10, 0, 0, 0, 0, 0, 0, -10, -20, -10, -10, -5, -5, -10, -10, -20],
      
      'player_king': [20, 30, 10, 0, 0, 10, 30, 20, 20, 20, 0, -5, -5, 0, 20, 20, 10, 10, -10,-20,-20,-10, 10, 10, 0, 0, -20,-30,-30,-20, 0, 0,
                      0, 0, -20,-30,-30,-20, 0, 0, 10, 10, -10,-20,-20,-10, 10, 10, 20, 20, 0, 0, 0, 0, 20, 20, 20, 30, 10, 0, 0, 10, 30, 20],

      'enemy_pawns': [0, 0, 0, 0, 0, 0, 0, 0, 5, 10, 10, -20, -20, 10, 10, 5, 5, -5, -10, 0, 0, -10, -5, 5, 0, 0, 0, 20, 20, 0, 0, 0, 
                      5, 5, 10, 25, 25, 10, 5, 5, 10, 10, 20, 30, 30, 20, 10, 10, 50, 50, 50, 50, 50, 50, 50, 50, 100, 100, 100, 100, 100, 100, 100, 100],
      
      'enemy_rooks': [0, 0, 0, 0, 0, 0, 0, 0, 5, 10, 10, 10, 10, 10, 10, 5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5,
                    -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, 5, 10, 10, 10, 10, 10, 10, 5, 0, 0, 0, 5, 5, 0, 0, 0],
      
      'enemy_knights': [-50, -40, -30, -30, -30, -30, -40, -50, -40, -20, 0, 5, 5, 0, -20, -40, -30, 5, 10, 15, 15, 10, 5, -30, -30, 0, 15, 20, 20, 15, 0, -30, 
                        -30, 5, 15, 20, 20, 15, 5, -30, -30, 0, 10, 15, 15, 10, 0, -30, -40, -20, 0, 0, 0, 0, -20, -40, -50, -40, -30, -30, -30, -30, -40, -50],
      
      'enemy_bishops': [-20, -10, -10, -10, -10, -10, -10, -20, -10, 5, 0, 0, 0, 0, 5, -10, -10, 10, 10, 10, 10, 10, 10, -10, -10, 0, 10, 10, 10, 10, 0, -10,
                      -10, 5, 5, 10, 10, 5, 5, -10, -10, 0, 5, 10, 10, 5, 0, -10, -10, 0, 0, 0, 0, 0, 0, -10, -20, -10, -10, -10, -10, -10, -10, -20],
      
      'enemy_queen': [-20, -10, -10, -5, -5, -10, -10, -20, -10, 0, 5, 0, 0, 0, 0, -10, -10, 5, 5, 5, 5, 5, 0, -10, 0, 0, 5, 5, 5, 5, 0, -5,
                      -5, 0, 5, 5, 5, 5, 0, -5, -10, 0, 5, 5, 5, 5, 0, -10, -10, 0, 0, 0, 0, 0, 0, -10, -20, -10, -10, -5, -5, -10, -10, -20],
       
      'enemy_king': [20, 30, 10, 0, 0, 10, 30, 20, 20, 20, 0, 0, 0, 0, 20, 20, 10, 10, -10,-20,-20,-10, 10, 10, 0, 0, -20,-30,-30,-20, 0, 0,
                      0, 0, -20,-30,-30,-20, 0, 0, 10, 10, -10,-20,-20,-10, 10, 10, 20, 20, 0, -5, -5, 0, 20, 20, 20, 30, 10, 0, 0, 10, 30, 20],
    }
    
    self.PlayerColor = PlayerColor
    self.turn_counter = 1
    self.endGame = False
    self.fiftyMoveRule_checker = 0
    self.kingPositions = {True: None, False: None}
    self.kingInCheck = {True: False, False: False}
    self.boardStateHistory = {}
    self.pieces = set()
    self.slidingPieces = set()
    self.piecesByColor = {True: set(), False: set()}
    self.bit_to_pos = [(7 - (i // 8), i % 8) for i in range(64)]
    
  def print_bitboard(self, binary_number):
    # To ensure the binary number has 64 bits
    binary_string = f"{binary_number:064b}"
    board_representation = []
    # Iterate through the binary string from the least significant bit to the most
    for i in range(63, -1, -8):  # Start from the bottom row and move upwards
        row = binary_string[i-7:i+1]  # Select 8 bits for the current row
        row_representation = ' '.join(['1' if bit == '1' else '.' for bit in reversed(row)])
        board_representation.append(row_representation)

    print('\n'.join(reversed(board_representation)))
    print("-----------")

  def initializeBoard(self):    
    for row in range(8):
      for col in range(8):       
        if(row == 0):
          if(col == 0 or col == 7):
            piece = Rook(position=(row, col), color=not self.PlayerColor, PlayerColor=self.PlayerColor)
            self.cells[row][col].piece = piece
            self.pieces.add(piece)
            piece.position = (row, col)
            piece.bitPosition = self.translate_position_to_binary(row, col)
            self.slidingPieces.add(piece)
            self.piecesByColor[piece.color].add(piece)
          
          elif(col == 1 or col == 6):
            piece = Knight(position=(row, col), color= not self.PlayerColor, PlayerColor=self.PlayerColor)
            self.cells[row][col].piece = piece
            self.pieces.add(piece)
            piece.position = (row, col)
            piece.bitPosition = self.translate_position_to_binary(row, col)
            self.piecesByColor[piece.color].add(piece)
          
          elif(col == 2 or col == 5):
            piece = Bishop(position=(row, col), color= not self.PlayerColor, PlayerColor=self.PlayerColor)
            self.cells[row][col].piece = piece
            self.pieces.add(piece)
            piece.position = (row, col)
            piece.bitPosition = self.translate_position_to_binary(row, col)
            self.slidingPieces.add(piece)
            self.piecesByColor[piece.color].add(piece)
            
          elif(col == 3):
            piece = Queen(position=(row, col), color= not self.PlayerColor, PlayerColor=self.PlayerColor)
            self.cells[row][col].piece = piece
            self.pieces.add(piece)
            piece.position = (row, col)
            piece.bitPosition = self.translate_position_to_binary(row, col)
            self.slidingPieces.add(piece)
            self.piecesByColor[piece.color].add(piece)
            
          elif(col == 4):
            piece = King(position=(row, col), color= not self.PlayerColor, PlayerColor=self.PlayerColor)
            self.cells[row][col].piece = piece
            self.kingPositions[not self.PlayerColor] = (row, col)
            self.pieces.add(piece)
            piece.position = (row, col)
            piece.bitPosition = self.translate_position_to_binary(row, col)
            self.piecesByColor[piece.color].add(piece)
            
        elif(row == 1):
          piece = Pawn(position=(row, col), color= not self.PlayerColor, PlayerColor=self.PlayerColor)
          self.cells[row][col].piece = piece
          self.pieces.add(piece)
          piece.position = (row, col)
          piece.starting_bitPosition = self.translate_position_to_binary(row, col)
          piece.bitPosition = self.translate_position_to_binary(row, col)
          self.piecesByColor[piece.color].add(piece)
          
        elif(row == 6):
          piece = Pawn(position=(row, col), color=self.PlayerColor, PlayerColor=self.PlayerColor)
          self.cells[row][col].piece = piece
          self.pieces.add(piece)
          piece.position = (row, col)
          piece.starting_bitPosition = self.translate_position_to_binary(row, col)
          piece.bitPosition = self.translate_position_to_binary(row, col)
          self.piecesByColor[piece.color].add(piece)
          
        elif(row == 7):
          if(col == 0 or col == 7):
            piece = Rook(position=(row, col), color=self.PlayerColor, PlayerColor=self.PlayerColor)
            self.cells[row][col].piece = piece
            self.pieces.add(piece)
            piece.position = (row, col)
            piece.bitPosition = self.translate_position_to_binary(row, col)
            self.slidingPieces.add(piece)
            self.piecesByColor[piece.color].add(piece)
            
          elif(col == 1 or col == 6):
            piece = Knight(position=(row, col), color=self.PlayerColor, PlayerColor=self.PlayerColor)
            self.cells[row][col].piece = piece
            self.pieces.add(piece)
            piece.position = (row, col)
            piece.bitPosition = self.translate_position_to_binary(row, col)
            self.piecesByColor[piece.color].add(piece)
            
          elif(col == 2 or col == 5):
            piece = Bishop(position=(row, col), color=self.PlayerColor, PlayerColor=self.PlayerColor)
            self.cells[row][col].piece = piece
            self.pieces.add(piece)
            piece.position = (row, col)
            piece.bitPosition = self.translate_position_to_binary(row, col)
            self.slidingPieces.add(piece)
            self.piecesByColor[piece.color].add(piece)
            
          elif(col == 4):
            piece = King(position=(row, col), color=self.PlayerColor, PlayerColor=self.PlayerColor)
            self.cells[row][col].piece = piece
            self.kingPositions[self.PlayerColor] = (row, col)
            self.pieces.add(piece)
            piece.position = (row, col)
            piece.bitPosition = self.translate_position_to_binary(row, col)
            self.piecesByColor[piece.color].add(piece)
            
          elif(col == 3):
            piece = Queen(position=(row, col), color=self.PlayerColor, PlayerColor=self.PlayerColor)
            self.cells[row][col].piece = piece
            self.pieces.add(piece)
            piece.position = (row, col)
            piece.bitPosition = self.translate_position_to_binary(row, col)
            self.slidingPieces.add(piece)
            self.piecesByColor[piece.color].add(piece)
            
  def updateBoardStateHistory(self):
    current_state = self.__str__()

    if current_state in self.boardStateHistory:
      self.boardStateHistory[current_state] += 1
    else:
      self.boardStateHistory[current_state] = 1
  
  def init_all_pieces_moves(self):
    for piece in self.pieces:
      piece.getMoves(self)
  
  @profile
  def update_AttackMap_of_AffectedPieces(self, moved_piece, original_position, new_position):
    for piece in self.slidingPieces:
      #if piece.piece_type == "Bishop" or piece.piece_type == "Rook" or piece.piece_type == "Queen":
        if (original_position & piece.attackedSquares) > 0 or (new_position & piece.attackedSquares) > 0:
          piece.getAttackedSquares(self)
        
  def update_AttackMap_of_AffectedPieces_En_Passant(self, moved_piece, original_position, new_position, en_passanted_piece_square): #to be updated
    moved_piece.getAttackedSquares(self)
    for piece in self.pieces:
      if (original_position & piece.attackedSquares) > 0 or (new_position & piece.attackedSquares) > 0 or (en_passanted_piece_square & piece.attackedSquares) > 0:
        piece.getAttackedSquares(self)
  
  def getCell(self, row, col):
    return self.cells[row][col]
  
  def increment_turn(self):
    self.turn_counter += 1  

  def get_all_pieces_bitboard(self):
    return (self.bit_boards['enemy_pawns'] |
            self.bit_boards['enemy_rooks'] |
            self.bit_boards['enemy_knights'] |
            self.bit_boards['enemy_bishops'] |
            self.bit_boards['enemy_queen'] |
            self.bit_boards['enemy_king'] | 
            self.bit_boards['player_pawns'] |
            self.bit_boards['player_rooks'] |
            self.bit_boards['player_knights'] |
            self.bit_boards['player_bishops'] |
            self.bit_boards['player_queen'] |
            self.bit_boards['player_king'])
  
  def get_enemy_bitboard(self):
    return (self.bit_boards['enemy_pawns'] |
            self.bit_boards['enemy_rooks'] |
            self.bit_boards['enemy_knights'] |
            self.bit_boards['enemy_bishops'] |
            self.bit_boards['enemy_queen'] |
            self.bit_boards['enemy_king'])

  def get_player_bitboard(self):
    return (self.bit_boards['player_pawns'] |
            self.bit_boards['player_rooks'] |
            self.bit_boards['player_knights'] |
            self.bit_boards['player_bishops'] |
            self.bit_boards['player_queen'] |
            self.bit_boards['player_king'])
  
  def translate_bit_to_position(self, binary_number):
    #Used when there is only 1 digit set to '1'.
    if binary_number:
      index = int(math.log2(binary_number)) 
      row = 7 - (index // 8)  # Row needs to be inverted for correct orientation
      col = index % 8   
      return (row, col)

  def translate_bitboard_to_positions(self, bitboard):
    positions = set()
    while bitboard:
      # Extract the position of the least significant set bit (LSB)
      lsb_index = bitboard & -bitboard

      # Check if lsb_index is zero (which should not happen)
      if lsb_index == 0:
        print(f"Unexpected lsb_index=0 for bitboard={bitboard}")
        break

      # Find the index of the LSB (0-63)
      index = (lsb_index.bit_length() - 1)

      # Check if the index is within the bounds of self.bit_to_pos
      if index < 0 or index >= len(self.bit_to_pos):
        print(f"Index out of range: index={index}, bitboard={bitboard}")
        break

      # Use the precomputed position for this index
      positions.add(self.bit_to_pos[index])

      # Clear the least significant set bit
      bitboard &= bitboard - 1

    return positions

  def translate_position_to_binary(self, row, col):
    # Inverting the row and column for correct orientation and calculating the index in the binary number
    index = (7 - row) * 8 + col
    # Set the specific bit
    return 1 << index
  
  def updateBitBoards(self, piece_bitboard, captured_piece_bitboard, old_pos, new_pos):
    
    old_pos_binaryPosition = self.translate_position_to_binary(old_pos[0], old_pos[1])
    new_pos_binaryPosition = self.translate_position_to_binary(new_pos[0], new_pos[1])  
    self.bit_boards[piece_bitboard] = (self.bit_boards[piece_bitboard] & (old_pos_binaryPosition ^ 0xFFFFFFFFFFFFFFFF)) | new_pos_binaryPosition
    
    if captured_piece_bitboard:
      self.bit_boards[captured_piece_bitboard] = self.bit_boards[captured_piece_bitboard] & (new_pos_binaryPosition ^ 0xFFFFFFFFFFFFFFFF)
  
  def updateBitBoards_En_Passant(self, captured_piece_bitboard, position):
    
    self.bit_boards[captured_piece_bitboard] = self.bit_boards[captured_piece_bitboard] & (position ^ 0xFFFFFFFFFFFFFFFF)
  
  def updateBitBoards_Promotion(self, piece):
    #Since now the piece is not a pawn...
    self.bit_boards[piece.board] |= piece.bitPosition 
    old_board = "player_pawns" if piece.color == self.PlayerColor else "enemy_pawns"
    self.bit_boards[old_board] = (self.bit_boards[old_board] & (piece.bitPosition ^ 0xFFFFFFFFFFFFFFFF))
  
  def isSquareUnderAttack(self, position, color):
    bit_position = self.translate_position_to_binary(position[0], position[1])
    pieces = self.piecesByColor[color]
    for piece in pieces:
      if (piece.attackedSquares & bit_position) != 0:
        return True
    
    return False
  
  @profile
  def movePiece(self, piece, next_position):
    if (piece.piece_type == "King" and piece.checkCastle(self, next_position)):
      self.castle(piece, next_position)

    elif (piece.piece_type == "Player_Pawn" or piece.piece_type == "Enemy_Pawn") and piece.checkEn_Passant(self, next_position):
      self.En_Passant(piece, next_position)
    
    else:    
      
      original_bit_position = piece.bitPosition
      
      start_row = 6 if piece.color == self.PlayerColor else 1
      end_row = 4 if piece.color == self.PlayerColor else 3
      if (piece.piece_type == "Player_Pawn" or piece.piece_type == "Enemy_Pawn") and piece.position[0] == start_row and next_position[0] == end_row:
        piece.en_passant = self.turn_counter
      
      self.cells[piece.position[0]][piece.position[1]].piece = None
      captured_cell = self.cells[next_position[0]][next_position[1]]
      piece.bitPosition = self.translate_position_to_binary(next_position[0], next_position[1])
      
      #dar update depois da cena
      if captured_cell.piece:
        self.updateBitBoards(piece.board, captured_cell.piece.board, piece.position, next_position)
      
        if captured_cell.piece in self.pieces:
          self.pieces.remove(captured_cell.piece)
          self.piecesByColor[captured_cell.piece.color].remove(captured_cell.piece)
          if captured_cell.piece in self.slidingPieces:
            self.slidingPieces.remove(captured_cell.piece)

      
      else:
        self.updateBitBoards(piece.board, None, piece.position, next_position)
        
      captured_cell.piece = piece
      piece.position = next_position
      piece.hasMoved = True
      if piece.piece_type == "King":
        self.kingPositions[piece.color] = next_position
      
      next_bit_position = self.translate_position_to_binary(next_position[0], next_position[1])
      self.update_AttackMap_of_AffectedPieces(piece, original_bit_position, next_bit_position)
              
    if self.isKingInCheck(not piece.color):
      self.kingInCheck[not piece.color] = True   
    
    self.kingInCheck[piece.color] = False 
        
  def simulateMove(self, piece, next_position):
    self.cells[piece.position[0]][piece.position[1]].piece = None
    captured_cell = self.cells[next_position[0]][next_position[1]]
    piece.bitPosition = self.translate_position_to_binary(next_position[0], next_position[1])
        
    if captured_cell.piece:
      self.updateBitBoards(piece.board, captured_cell.piece.board, piece.position, next_position)
        
      if captured_cell.piece in self.pieces:
        self.pieces.remove(captured_cell.piece)
        self.piecesByColor[captured_cell.piece.color].remove(captured_cell.piece)
        if captured_cell.piece in self.slidingPieces:
            self.slidingPieces.remove(captured_cell.piece)
        
    else:
      self.updateBitBoards(piece.board, None, piece.position, next_position)
          
    captured_cell.piece = piece
    piece.position = next_position    
    if piece.piece_type == "King":
      self.kingPositions[piece.color] = next_position
  
  @profile
  def checkMove(self, piece, newPosition):
    checkFlag = False
    original_position = piece.position
    original_bit_position = piece.bitPosition
    original_bitboards = self.copy_dict(self.bit_boards)
    original_hasMoved = piece.hasMoved
    captured_piece = self.getCell(newPosition[0], newPosition[1]).piece
    new_bit_position = self.translate_position_to_binary(newPosition[0], newPosition[1])
    
    self.simulateMove(piece, newPosition)
      
    if (self.isKingInCheck(piece.color)):
      checkFlag = True
    
    #Reversing the simulation
    self.simulateMove(piece, original_position)   
    piece.position = original_position 
    piece.bitPosition = original_bit_position
    piece.hasMoved = original_hasMoved
    self.bit_boards = original_bitboards   
            
    if captured_piece: #If the simulated move resulted in a capture, it is reversed
      self.getCell(newPosition[0], newPosition[1]).piece = captured_piece
      captured_piece.position = newPosition
      self.pieces.add(captured_piece)
      self.piecesByColor[captured_piece.color].add(captured_piece)
      if captured_piece in self.slidingPieces:
        self.slidingPieces.add(captured_piece)
      
    self.update_AttackMap_of_AffectedPieces(piece, new_bit_position, original_bit_position)
    
    return checkFlag

  @profile
  def isKingInCheck(self, color):
    king_pos = self.translate_position_to_binary(self.kingPositions[color][0], self.kingPositions[color][1])
    for piece in self.piecesByColor[not color]:
      if piece.piece_type == "King" or piece.piece_type == "Knight" or piece.piece_type == "Pawn":
        if (self.getCell(piece.position[0], piece.position[1]).precomputed_AttackMap[piece.piece_type] & king_pos) > 0:
          return True
        
      else:
        if (piece.attackedSquares & king_pos) > 0:
          return True
      
    return False
    """
    kingPosition = self.kingPositions[color]
    if self.isSquareUnderAttack(kingPosition, color): 
      return True
    return False
    """
  
  def castle(self, piece, next_position):
    row = piece.position[0]
    king_col = 6 if next_position[1] > 4 else 2
    rook_init_col = 7 if next_position[1] > 4 else 0
    rook_col = 5 if next_position[1] > 4 else 3
    rook = self.getCell(row, rook_init_col).piece
        
    self.cells[row][4].piece = None
    self.cells[row][king_col].piece = piece
    piece.hasMoved = True
    piece.position = (row, king_col)
    self.kingPositions[piece.color] = (row, king_col)
    
    self.cells[row][rook_init_col].piece = None
    self.cells[row][rook_col].piece = rook
    rook.hasMoved = True
    rook.position = (row, rook_col)
        
    self.updateBitBoards(piece.board, None, (row, 4), (row, king_col))
    piece.bitPosition = self.translate_position_to_binary(row, king_col)
    self.updateBitBoards(rook.board, None, (row, rook_init_col), (row, rook_col))
    rook.bitPosition = self.translate_position_to_binary(row, rook_col)
    
    rook.getAttackedSquares(self) 
        
  def En_Passant(self, piece, next_position):
    
    direction = 1 if piece.color==self.PlayerColor else -1
    
    next_bitPosition = self.translate_position_to_binary(next_position[0], next_position[1])
    original_bitPosition = piece.bitPosition
    self.getCell(piece.position[0], piece.position[1]).piece = None
    self.getCell(next_position[0], next_position[1]).piece = piece
    self.updateBitBoards(piece.board, None, piece.position, next_position)
    piece.position = next_position
    piece.bitPosition = next_bitPosition
    
    
    captured_piece = self.getCell(next_position[0] + direction, next_position[1]).piece
    en_passanted_piece_square = captured_piece.bitPosition
    self.updateBitBoards_En_Passant(captured_piece.board, en_passanted_piece_square)
    self.pieces.remove(captured_piece)
    self.piecesByColor[captured_piece.color].remove(captured_piece)
    self.getCell((next_position[0] + direction), next_position[1]).piece = None
        
    self.update_AttackMap_of_AffectedPieces_En_Passant(piece, original_bitPosition, next_bitPosition, en_passanted_piece_square)
          
  def promote(self, piece, choice):
    self.pieces.remove(piece)
    self.piecesByColor[piece.color].remove(piece)
    if piece is not None and (piece.piece_type == "Player_Pawn" or piece.piece_type == "Enemy_Pawn"):
      row = piece.position[0]
      col = piece.position[1]
      bitPosition = piece.bitPosition
      if choice == "Queen":
        self.getCell(row, col).piece = None
        piece = Queen(position=piece.position, color=piece.color, PlayerColor=self.PlayerColor)
        self.getCell(row, col).piece = piece
        piece.bitPosition = bitPosition
        self.updateBitBoards_Promotion(piece)
        piece.getAttackedSquares(self)
      elif choice == "Knight":
        self.getCell(row, col).piece = None
        piece = Knight(position=piece.position, color=piece.color, PlayerColor=self.PlayerColor)
        self.getCell(row, col).piece = piece
        piece.bitPosition = bitPosition
        self.updateBitBoards_Promotion(piece)
      elif choice == "Rook":
        self.getCell(row, col).piece = None
        piece = Rook(position=piece.position, color=piece.color, PlayerColor=self.PlayerColor)
        self.getCell(row, col).piece = piece
        piece.bitPosition = bitPosition
        self.updateBitBoards_Promotion(piece)
        piece.getAttackedSquares(self)
      elif choice == "Bishop":
        self.getCell(row, col).piece = None
        piece = Bishop(position=piece.position, color=piece.color, PlayerColor=self.PlayerColor)
        self.getCell(row, col).piece = piece
        piece.bitPosition = bitPosition
        self.updateBitBoards_Promotion(piece)
        piece.getAttackedSquares(self)
        
      self.pieces.add(piece)
      self.piecesByColor[piece.color].add(piece)

  def checkFiftyMoveRule(self, piece, next_position):
    if (piece.piece_type == "Player_Pawn" or piece.piece_type == "Enemy_Pawn") or (self.getCell(next_position[0], next_position[1]).piece is not None and self.getCell(next_position[0], next_position[1]).piece.color != self.PlayerColor):
      self.fiftyMoveRule_checker = 0
    else: 
      self.fiftyMoveRule_checker += 1
  
  def checkThreeFoldRepetition(self):
    current_state = self.__str__()
    return self.boardStateHistory.get(current_state, 0) >= 3

  def createEndGameScreen(self, result):
    translucent_surface = pygame.Surface((720, 720), pygame.SRCALPHA)
    translucent_surface.fill((255, 255, 255, 128))  # White color with half transparency

    # Set up the font and render the text
    font = pygame.font.SysFont(None, 48)
    text = font.render(result, True, (0, 0, 0))  # Black text
    text_rect = text.get_rect(center=(720/2, 720/2))  
      
    return translucent_surface, text, text_rect
   
  def checkDraw(self):
    #INSUFFICIENT MATERIAL 
    if len(self.pieces) == 3:
      for piece in self.pieces:
        if piece.piece_type == "Bishop" or piece.piece_type == "Knight":
          return True
        
    elif len(self.pieces) == 2:
      return True
    
    elif len(self.pieces) == 4: #Draw if there is a king and a bishop on both sides
      #Since even when the bishops are of oposite square colors, it is extremly dificult to lead to checkmate so lets consider it a draw
      count = 0
      for piece in self.piecesByColor[True]:
        if piece.piece_type == "Bishop":
          count+=1
      for piece in self.piecesByColor[False]:
        if piece.piece_type == "Bishop":
          count+=1
      if count == 2:
        return True
    
    #50 MOVE RULE
    if self.fiftyMoveRule_checker >= 50:
      return True
    
    
    #Threefold repetition
    if self.checkThreeFoldRepetition():
      return True
    
         
    #STALEMATE
    if not self.isKingInCheck(self.PlayerColor):
      pieces = self.piecesByColor[True]
      for piece in pieces:
        possible_moves = piece.getPossibleMoves(self)
        if possible_moves:
          return False
      return True
    
    #STALEMATE
    elif not self.isKingInCheck(not self.PlayerColor):
      pieces = self.piecesByColor[False]
      for piece in pieces:
        possible_moves = piece.getPossibleMoves(self)
        if possible_moves:
          return False
      return True

    return False

  def checkEndGame(self):
    if self.isKingInCheck(self.PlayerColor):
      pieces = self.piecesByColor[True]
      for piece in pieces:
        possible_moves = piece.getPossibleMoves(self)
        if possible_moves:
          return None
         
      self.endGame = True
      return 1
    
    elif self.isKingInCheck(not self.PlayerColor):
      pieces = self.piecesByColor[False]
      for piece in pieces:
        possible_moves = piece.getPossibleMoves(self)
        if possible_moves:
          return None
      
      self.endGame = True
      return -1
    
    elif self.checkDraw():
      self.endGame = True
      return 0
    
    #DRAW
    return None

  @profile
  def getPositionValue(self, piece):
    n = 1 if piece.color else -1
    value = self.piece_position_values[piece.board][piece.position[0] * 8 + piece.position[1]]
    return value * n
  
  @profile
  def evaluationFunction(self):
    eval=0
    for piece in self.pieces:
      if not piece.piece_type == "King":
        eval += piece.value
      eval += self.getPositionValue(piece)
    return eval

  def __str__(self):
    board_str = ""
    for row in range(8):
        row_str = " | ".join(self.cells[row][col].piece.path if self.cells[row][col].piece else "Empty" for col in range(8))
        board_str += row_str + "\n" + ("-" * 50) + "\n"
    return board_str
  
  def copy_dict(self, dictionary):
    return {key: value for key, value in dictionary.items()}
  
  def copy(self):
    new_board = Board(self.PlayerColor)
    new_board.turn_counter = self.turn_counter
    new_board.endGame = self.endGame
    new_board.fiftyMoveRule_checker = self.fiftyMoveRule_checker
    new_board.kingPositions = self.copy_dict(self.kingPositions)
    new_board.kingInCheck = self.copy_dict(self.kingInCheck)
    new_board.boardStateHistory = self.copy_dict(self.boardStateHistory)
    new_board.pieces = set()
    new_board.piecesByColor[True] = set()
    new_board.piecesByColor[False] = set()
    
    for row in range(8):
      for col in range(8):  
        cell_copy = self.cells[row][col].copy()
        new_board.cells[row][col] = cell_copy
        
        if cell_copy.piece:
          new_piece = cell_copy.piece.copy()
          cell_copy.piece = new_piece
          new_board.pieces.add(new_piece)
          new_board.piecesByColor[new_piece.color].add(new_piece)

        
    return new_board

  def is_Piece_Aligned_With_King(self, piece_position, color):
    king_posiiton = self.kingPositions[color]
    if piece_position[0] == king_posiiton[0] or piece_position[1] == king_posiiton[1]:
      return True
    
    if abs(piece_position[0] - king_posiiton[0]) == abs(piece_position[1] - piece_position[1]):
        return True
          
    return False
  
  def isPiecePinned(self, pinned_piece, color):
    if self.is_Piece_Aligned_With_King(pinned_piece.position, color):
      pinned_piece_bitPosition = pinned_piece.bitPosition
      for piece in self.piecesByColor[color]:
        if (piece.piece_type == "Rook" or piece.piece_type == "Bishop" or piece.piece_type == "Queen") and (piece.attackedSquares & pinned_piece_bitPosition > 0):
          king_pos = self.kingPositions[color]
          king_bitPosition = self.translate_position_to_binary(king_pos[0], king_pos[1])
          if self.is_Piece_Aligned_With_King(piece.position, color) and (piece.attackedSquares & king_bitPosition == 0): 
            return True, piece.position
          
          
    return False, None
      
  @profile
  def storeStateBeforeMove(self, piece, newPosition):
    original_position = piece.position
    original_bit_position = piece.bitPosition
    original_bitboards = self.copy_dict(self.bit_boards)
    original_hasMoved = piece.hasMoved
    captured_piece = self.getCell(newPosition[0], newPosition[1]).piece
    en_passant_flag = False
    if (piece.piece_type == "Player_Pawn" or piece.piece_type == "Enemy_Pawn"):
      en_passant_flag = True if piece.checkEn_Passant(self, newPosition) else False
      if en_passant_flag:
        direction = 1 if piece.color==self.PlayerColor else -1
        captured_piece = self.getCell(newPosition[0] + direction, newPosition[1]).piece
    new_bit_position = self.translate_position_to_binary(newPosition[0], newPosition[1])
    return (original_position, original_bit_position, original_bitboards, original_hasMoved, captured_piece, en_passant_flag, new_bit_position)
    
  def reverseMove(self, piece, original_position, original_bit_position, captured_piece):
    
    self.cells[piece.position[0]][piece.position[1]].piece = None
    self.cells[original_position[0]][original_position[1]].piece = piece
    piece.bitPosition = original_bit_position
    piece.position = original_position    
        
    if captured_piece:
      self.cells[captured_piece.position[0]][captured_piece.position[1]].piece = captured_piece
              
    if piece.piece_type == "King":
      self.kingPositions[piece.color] = original_position
     
  @profile
  def unmakeMove(self, piece, newPosition, storedState):
    original_position, original_bit_position, original_bitboards, original_hasMoved, captured_piece, en_passant_flag, new_bit_position = storedState
    if en_passant_flag:
      self.reverseMove(piece, original_position, original_bit_position, captured_piece)
      self.updateBitBoards(piece.board, captured_piece.board, piece.position, newPosition)
      en_passanted_piece_square = None
      direction = 1 if piece.color==self.PlayerColor else -1
      en_passanted_piece_square = self.translate_position_to_binary(newPosition[0] + direction, newPosition[1])
      self.updateBitBoards_En_Passant(captured_piece.board, en_passanted_piece_square)
      self.getCell(newPosition[0] + direction, newPosition[1]).piece = captured_piece
      self.pieces.add(captured_piece)
      self.piecesByColor[captured_piece.color].add(captured_piece)
          
      self.update_AttackMap_of_AffectedPieces_En_Passant(piece, original_bit_position, new_bit_position, en_passanted_piece_square)
      
    else:
      self.reverseMove(piece, original_position, original_bit_position, captured_piece)   
      piece.position = original_position 
      piece.bitPosition = original_bit_position
      piece.hasMoved = original_hasMoved
      self.bit_boards = original_bitboards   
            
      if captured_piece: #If the simulated move resulted in a capture, it is reversed
        self.updateBitBoards(piece.board, captured_piece.board, piece.position, newPosition)
        if captured_piece.piece_type == "Bishop" or captured_piece.piece_type == "Rook" or captured_piece.piece_type == "Queen":
            self.slidingPieces.add(captured_piece)
        self.getCell(newPosition[0], newPosition[1]).piece = captured_piece
        captured_piece.position = newPosition
        self.pieces.add(captured_piece)
        self.piecesByColor[captured_piece.color].add(captured_piece)
      else:
        self.updateBitBoards(piece.board, None, piece.position, newPosition)
  
    self.turn_counter -= 1
  
  
  
  """
  
  
  
  
  def checkMove(self, piece, newPosition):
    checkFlag = False
    original_position = piece.position
    original_bit_position = piece.bitPosition
    original_bitboards = self.copy_dict(self.bit_boards)
    original_hasMoved = piece.hasMoved
    captured_piece = self.getCell(newPosition[0], newPosition[1]).piece
    en_passant_flag = False
    new_bit_position = self.translate_position_to_binary(newPosition[0], newPosition[1])
    
    
    if isinstance(piece, Pawn):
      if piece.checkEn_Passant(self, newPosition):
        direction = 1 if piece.color==self.PlayerColor else -1
        captured_piece = self.getCell(newPosition[0] + direction, newPosition[1]).piece
        en_passanted_piece_square = self.translate_position_to_binary(newPosition[0] + direction, newPosition[1])
        self.En_Passant(piece, newPosition)
        self.update_AttackMap_of_AffectedPieces_En_Passant(piece, original_bit_position, new_bit_position, en_passanted_piece_square)
        en_passant_flag = True
        self.pieces.add(piece)
      else:
        self.simulateMove(piece, newPosition)
        self.update_AttackMap_of_AffectedPieces(piece, original_bit_position, new_bit_position)
        self.pieces.add(piece)
    else:
      self.simulateMove(piece, newPosition)
      self.update_AttackMap_of_AffectedPieces(piece, original_bit_position, new_bit_position)
      self.pieces.add(piece)
      
    if (self.isKingInCheck(piece.color)):
      checkFlag = True
    
    #Reversing the simulation
    if isinstance(piece, Pawn):
      if en_passant_flag:
        self.simulateMove(piece, original_position)
        
        if captured_piece: #If the simulated move resulted in a capture, it is reversed
          direction = 1 if piece.color==self.PlayerColor else -1
          en_passanted_piece_square = self.translate_position_to_binary(newPosition[0] + direction, newPosition[1])
          self.getCell(newPosition[0] + direction, newPosition[1]).piece = captured_piece
          captured_piece.position = (newPosition[0] + direction, newPosition[1])
          self.pieces.add(captured_piece)
          
        self.update_AttackMap_of_AffectedPieces_En_Passant(piece, original_bit_position, new_bit_position, en_passanted_piece_square)
      else:
        self.simulateMove(piece, original_position)   
        piece.position = original_position 
        piece.bitPosition = original_bit_position
        piece.hasMoved = original_hasMoved
        self.pieces.add(piece)
        self.bit_boards = original_bitboards  
        
        if captured_piece: #If the simulated move resulted in a capture, it is reversed
          self.getCell(newPosition[0], newPosition[1]).piece = captured_piece
          captured_piece.position = newPosition
          self.pieces.add(captured_piece)
        
        self.update_AttackMap_of_AffectedPieces(piece, new_bit_position, original_bit_position)
    else:
      self.simulateMove(piece, original_position)   
      piece.position = original_position 
      piece.bitPosition = original_bit_position
      piece.hasMoved = original_hasMoved
      self.pieces.add(piece)
      self.bit_boards = original_bitboards   
            
      if captured_piece: #If the simulated move resulted in a capture, it is reversed
        self.getCell(newPosition[0], newPosition[1]).piece = captured_piece
        captured_piece.position = newPosition
        self.pieces.add(captured_piece)
      
      self.update_AttackMap_of_AffectedPieces(piece, new_bit_position, original_bit_position)
    return checkFlag
  
  
  """  
    
      