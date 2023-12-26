from Board import Board
import pygame
from King import King
from Pawn import Pawn
from Position import Position
import math

from Rook import Rook

selected_piece = None
selected_piece_position = (0, 0)
is_dragging = False
possible_moves = []

def run_game():
    global selected_piece, selected_piece_position, is_dragging, dragging_offset, possible_moves
    board = Board()
    board.doInitialPositioning()
    pygame.init()
    width, height = 720, 720
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Chess Game")
    dragging_offset = (0, 0)  # Initialize dragging offset
    # Main game loop
    running = True
    update_game_state(window, board)
    while running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
          print(board.getTurn_counter())
          is_dragging = True
          # Handle piece selection
          selected_piece_info = get_selected_piece(event.pos, board)
          if selected_piece_info:
            selected_piece, selected_piece_position = selected_piece_info
            if selected_piece is not None:
              possible_moves = selected_piece.getPossibleMoves(board)
              draw_possible_moves(window, possible_moves)
            
        elif event.type == pygame.MOUSEMOTION and is_dragging:
          # Handle piece dragging
          selected_piece_position = event.pos
          update_game_state(window, board)  # Update the entire board state
          draw_possible_moves(window, possible_moves)
          draw_dragged_piece(window, selected_piece, selected_piece_position)
                  
        elif event.type == pygame.MOUSEBUTTONUP:
          # Handle piece dropping
          is_dragging = False
          snap_piece_to_board(window, selected_piece, selected_piece_position, board)

        pygame.display.update()
    # Quit Pygame
    pygame.quit()


def update_game_state(window, board):
  WHITE = (255, 255, 255)
  window.fill(WHITE)
  draw_board(window)
  draw_pieces(window, board)
  
def draw_board(window):
  LIGHT = (238, 238, 210)
  DARK = (118, 150, 86)
  tile_size = 720 // 8
  
  for row in range(8):
    for col in range(8):
      color = LIGHT if (row + col) % 2 == 0 else DARK
      pygame.draw.rect(window, color, (col * tile_size, row * tile_size, tile_size, tile_size))

def draw_pieces(window, board):
  board_str = str(board)
  lines = board_str.strip().split("\n") # lines of the __str__ board method 
  tile_size = 720 // 8
  for row_index, row in enumerate(lines):
    if row_index % 2 == 0:  # Process only the lines of text that are rows of the board
      pieces = row.split(" | ")
      for col_index, piece_path in enumerate(pieces):
        if piece_path != "Empty":
        # Load and scale the piece image
          piece_image = pygame.image.load(piece_path)
          piece_image = pygame.transform.scale(piece_image, (tile_size, tile_size))
          # Draw the piece
          window.blit(piece_image, (col_index * tile_size, (row_index // 2) * tile_size))

def get_selected_piece(mouse_position, board):
  tile_size = 720 // 8
  col = mouse_position[0] // tile_size
  row = mouse_position[1] // tile_size

  # Check if there's a piece at the clicked position
  cell = board.getCell(Position(row, col))
  piece = cell.getPiece() if cell else None

  if piece:
    
    x_center = (int)((col * tile_size) + tile_size / 2)
    y_center = (int)((row * tile_size) + tile_size / 2)
    dragging_offset = (x_center, y_center)
  else:
    dragging_offset = (0, 0)
  
  return piece, dragging_offset

def draw_possible_moves(window, possible_moves):
  square_size = 720 // 8
  for pos in possible_moves:
    # Calculate the center of the square
    x_center = pos.getCol() * square_size + square_size // 2
    y_center = pos.getRow() * square_size + square_size // 2

    # Draw a small circle at the center
    pygame.draw.circle(window, (200, 200, 200), (x_center, y_center), 10)  

def snap_piece_to_board(window, piece, position, board):
  if piece:
    tile_size = 720 // 8
    col = position[0] // tile_size
    row = position[1] // tile_size
    next_position = Position(row, col)
    if is_valid_turn(piece, board):
      possible_moves = piece.getPossibleMoves(board)
      if next_position in possible_moves:
          tempBoard = board.simulateMove(piece, next_position)
          if (not tempBoard.isKingInCheck(piece.isWhite)):
            if ((isinstance(piece, King) or isinstance(piece, Rook)) and piece.checkCastle(board, next_position)):
              board.castle(piece, next_position)
            elif isinstance(piece, Pawn) and piece.checkEn_Passant(board, next_position):
              board.En_Passant(piece, next_position)
            else:
              piece.move(board, next_position)
            
            board.increment_turn()
  update_game_state(window, board)  # Redraw the board
       
def draw_dragged_piece(window, piece, position):
    if piece:
      tile_size = 720 // 8
      # Clear the original position
      clear_square(window, piece.getPosition().getRow(), piece.getPosition().getCol())

      # Draw the piece at new position
      x = position[0] - tile_size // 2
      y = position[1] - tile_size // 2
      piece_image_path = piece.getName()
      piece_image = pygame.image.load(piece_image_path)
      piece_image = pygame.transform.scale(piece_image, (tile_size, tile_size))
      window.blit(piece_image, (x, y))
      pygame.display.update()

def clear_square(window, row, col):
  tile_size = 720 // 8
  LIGHT = (238, 238, 210)
  DARK = (118, 150, 86)
  color = LIGHT if (row + col) % 2 == 0 else DARK
  pygame.draw.rect(window, color, (col * tile_size, row * tile_size, tile_size, tile_size))
  pygame.display.update()
  
def is_in_bounds(position):
  return 0 <= position[0] <= 720 and 0 <= position[1] <= 720

def is_valid_turn(piece, board):
    is_odd_turn = board.turn_counter % 2 != 0
    return (is_odd_turn and piece.isWhite) or (not is_odd_turn and not piece.isWhite)

def main():
  run_game()
  
if __name__ == "__main__":
  main()
  


