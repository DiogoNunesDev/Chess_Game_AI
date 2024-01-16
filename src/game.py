import pygame
import math
from Board import Board
from King import King
from Pawn import Pawn
from Rook import Rook
from Position import Position
from model import make_random_move

selected_piece = None
selected_piece_position = (0, 0)
is_dragging = False
possible_moves = []
player_color = None

def run_game():
    global selected_piece, selected_piece_position, is_dragging, dragging_offset, possible_moves, player_color
    PlayerColor = False
    board = Board(PlayerColor)
    board.doInitialPositioning()
    selected_piece_info = None
    pygame.init()
    width, height = 720, 720
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Chess Game")
    dragging_offset = (0, 0)  # Initialize dragging offset
    # Main game loop
    running = True
    update_game_state(window, board, PlayerColor)
    #player_color = input("Choose color: ")
    #PlayerisTeam = True if (int)(player_color) == 1 else False # true for white , false for black
    while running:
      if (board.getTurn_counter() % 2 == 0 and PlayerColor) or (board.getTurn_counter() % 2 != 0 and not PlayerColor):
          make_random_move(board, PlayerColor)
          update_game_state(window, board, PlayerColor)
          pygame.display.update()
          #Check for End Game after each move
          #TO-DO         
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not selected_piece:
                # Select the piece
                selected_piece_info = get_selected_piece(event.pos, board)
                if selected_piece_info:
                    selected_piece, _ = selected_piece_info
                    if selected_piece is not None and PlayerColor == selected_piece.getIsTeam():
                        possible_moves = selected_piece.getPossibleMoves(board)
                        update_game_state(window, board, PlayerColor)
                        draw_possible_moves(window, possible_moves, board)
            else:
                # Move the piece
                target_square = get_square_from_position(event.pos)
                if target_square in possible_moves:
                  snap_piece_to_board(window, selected_piece, target_square, board)
                  update_game_state(window, board, PlayerColor)
                  selected_piece = None  # Deselect after moving
                  
                  #Check for End Game after each move
                  #TO-DO                     
                else:
                  #selected_piece = None # Deselect if invalid move
                  if board.getCell(target_square).getPiece() is not None and selected_piece is not None and (board.getCell(target_square).getPiece().getIsTeam() == PlayerColor and selected_piece.getPosition() != board.getCell(target_square).getPiece().getPosition()): 
                    selected_piece_info = get_selected_piece(event.pos, board)
                    if selected_piece_info:
                      selected_piece, _ = selected_piece_info
                      if selected_piece is not None and PlayerColor == selected_piece.getIsTeam():
                        possible_moves = selected_piece.getPossibleMoves(board)
                        update_game_state(window, board, PlayerColor)
                        draw_possible_moves(window, possible_moves, board) 
                  else:
                    selected_piece = None
                    update_game_state(window, board, PlayerColor)
            
                    

        pygame.display.update()

      
    # Quit Pygame
    pygame.quit()

def update_game_state(window, board, PlayerColor):
  WHITE = (255, 255, 255)
  window.fill(WHITE)
  draw_board(window, board, PlayerColor)    
  draw_pieces(window, board, PlayerColor)
  
def draw_board(window, board, PlayerColor):
  LIGHT = (50, 103, 74)
  DARK = (237, 236, 233)
  RED = (198, 98, 79, 255)
  tile_size = 720 // 8
  isTeam = True if board.getTurn_counter() % 2 != 0 else False
  for row in range(8):
    for col in range(8):
      if PlayerColor:
        color = DARK if (row + col) % 2 == 0 else LIGHT
      else:
        color = LIGHT if (row + col) % 2 == 0 else DARK

      
      piece = board.getCell(Position(row, col)).getPiece()
      if piece is not None and isinstance(piece, King) and piece.getIsTeam()==isTeam and board.isKingInCheck() and piece.getPosition()==Position(row, col):
        translucent_surface = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
        translucent_surface.fill(RED)  
        window.blit(translucent_surface, (col * tile_size, row * tile_size))
      else:
        pygame.draw.rect(window, color, (col * tile_size, row * tile_size, tile_size, tile_size))
    
def draw_pieces(window, board, PlayerColor):
  board_str = str(board)
  lines = board_str.strip().split("\n")  # lines of the __str__ board method
  tile_size = 720 // 8
  for row_index, row in enumerate(lines):
    if row_index % 2 == 0:  # Process only the lines of text that are rows of the board
      pieces = row.split(" | ")
      for col_index, piece_path in enumerate(pieces):
        if piece_path != "Empty":

          piece_image = pygame.image.load(piece_path).convert_alpha()

          # Get the piece's width and height
          piece_width, piece_height = piece_image.get_size()

          # Calculate the position to center the piece on the square
          piece_x = col_index * tile_size + (tile_size - piece_width) // 2
          piece_y = (row_index // 2) * tile_size + (tile_size - piece_height) // 2

          # Draw the piece
          window.blit(piece_image, (piece_x, piece_y))

def get_selected_piece(mouse_position, board):
  tile_size = 720 // 8
  col = mouse_position[0] // tile_size
  row = mouse_position[1] // tile_size

  cell = board.getCell(Position(row, col))
  piece = cell.getPiece() if cell else None

  if piece:
    
    x_center = (int)((col * tile_size) + tile_size / 2)
    y_center = (int)((row * tile_size) + tile_size / 2)
    dragging_offset = (x_center, y_center)
  else:
    dragging_offset = (0, 0)
  
  return piece, dragging_offset

def draw_possible_moves(window, possible_moves, board):
  square_size = 720 // 8
  for pos in possible_moves:

    piece = board.getCell(pos).getPiece()

    if piece:
      circle_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
      pygame.draw.circle(circle_surface, (130, 130, 130, 100), (square_size // 2, square_size // 2), square_size // 2 - 2, 5)
      window.blit(circle_surface, (pos.getCol() * square_size, pos.getRow() * square_size))
      
    else:
      translucent_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
      pygame.draw.circle(translucent_surface, (130, 130, 130, 100), (square_size // 2, square_size // 2), 10)
      window.blit(translucent_surface, (pos.getCol() * square_size, pos.getRow() * square_size))

def snap_piece_to_board(window, piece, position, board):
  if piece:
    col = position.getCol()
    row = position.getRow()
    next_position = Position(row, col)
    if is_valid_turn(piece, board):
      possible_moves = piece.getPossibleMoves(board)
      if next_position in possible_moves:
          tempBoard = board.simulateMove(piece, next_position)
          if (not tempBoard.isKingInCheck()):
            if ((isinstance(piece, King) or isinstance(piece, Rook)) and piece.checkCastle(board, next_position)):
              board.castle(piece, next_position)
              board.increment_turn()
            elif isinstance(piece, Pawn) and piece.checkEn_Passant(board, next_position):
              board.En_Passant(piece, next_position)
              board.increment_turn()
            else:
              piece.move(board, next_position)
              board.increment_turn()
            
            
  update_game_state(window, board, player_color)  # Redraw the board
 
def get_square_from_position(position):
    tile_size = 720 // 8
    col = position[0] // tile_size
    row = position[1] // tile_size
    return Position(row, col)
        
def draw_dragged_piece(window, piece, position, board):
    if piece:
      tile_size = 720 // 8
      # Clear the original position
      clear_square(window, piece.getPosition().getRow(), piece.getPosition().getCol(), board)

      # Draw the piece at new position
      x = position[0] - tile_size // 2
      y = position[1] - tile_size // 2
      piece_image_path = piece.getName()
      piece_image = pygame.image.load(piece_image_path)
      piece_image = pygame.transform.scale(piece_image, (tile_size, tile_size))
      window.blit(piece_image, (x, y))
      pygame.display.update()

def clear_square(window, row, col, board):
  tile_size = 720 // 8
  LIGHT = (50, 103, 74)
  DARK = (237, 236, 233)
  RED = (198, 98, 79, 255)
  isTeam = True if board.getTurn_counter() % 2 != 0 else False
  color = DARK if (row + col) % 2 == 0 else LIGHT
  
  piece = board.getCell(Position(row, col)).getPiece()
  if piece is not None and isinstance(piece, King) and piece.getIsTeam()==isTeam and board.isKingInCheck(isTeam) and piece.getPosition()==Position(row, col):
    translucent_surface = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
    translucent_surface.fill(RED)  
    window.blit(translucent_surface, (col * tile_size, row * tile_size))
  else:
    pygame.draw.rect(window, color, (col * tile_size, row * tile_size, tile_size, tile_size))
  pygame.display.update()
  
def is_in_bounds(position):
  return 0 <= position[0] <= 720 and 0 <= position[1] <= 720

def is_valid_turn(piece, board):
    is_odd_turn = board.turn_counter % 2 != 0
    return (is_odd_turn and piece.isTeam) or (not is_odd_turn and not piece.isTeam)









def main():
  run_game()
  
if __name__ == "__main__":
  main()
  


