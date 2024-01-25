import pygame
import math
from Board import Board
from King import King
from Pawn import Pawn
from Rook import Rook
from Position import Position
from model import make_move, make_random_move
import profile

selected_piece = None
selected_piece_position = (0, 0)
possible_moves = []

def run_game():
    global selected_piece, selected_piece_position, possible_moves, PlayerColor, endGame
    pygame.init()
    width, height = 720, 720
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Chess Game")

    PlayerColor = start_screen(window)
    board = Board(PlayerColor)
    board.doInitialPositioning()
    update_game_state(window, board, PlayerColor)
    
    surface = None 
    text = None
    text_rect = None
    
    selected_piece_info = None
    running = True
    endGame = False
    #player_color = input("Choose color: ")
    #PlayerisTeam = True if (int)(player_color) == 1 else False # true for white , false for black
    while running:
      pygame.display.update()
      if ((board.getTurn_counter() % 2 == 0 and PlayerColor) or (board.getTurn_counter() % 2 != 0 and not PlayerColor)) and not endGame:
          make_random_move(board, PlayerColor)
          board.updateBoardStateHistory()
          update_game_state(window, board, PlayerColor)
          pygame.display.update()
          #Check for End Game after each move
          gameResult = board.checkEndGame()
          if gameResult == 0:
            surface, text, text_rect = board.createEndGameScreen(result= "DRAW! - Stalemate")     
          elif gameResult == 1:
            surface, text, text_rect = board.createEndGameScreen(result= "CHECKMATE! AI Bot has Won!")
          elif gameResult == -1:
            surface, text, text_rect = board.createEndGameScreen(result= "CHECKMATE! Player has Won!")  
          
          if surface is not None and text is not None:
            window.blit(surface, (0, 0))
            window.blit(text, text_rect)
            pygame.display.update()
      else:
        """
        make_random_move(board, not PlayerColor)
        board.updateBoardStateHistory()        
        update_game_state(window, board, PlayerColor)
        pygame.display.update()
        #Check for End Game after each move
        gameResult = board.checkEndGame()
        if gameResult == 0:
          surface, text, text_rect = board.createEndGameScreen(result= "DRAW!")     
        elif gameResult == 1:
          surface, text, text_rect = board.createEndGameScreen(result= "CHECKMATE! AI Bot has Won!")
        elif gameResult == -1:
          surface, text, text_rect = board.createEndGameScreen(result= "CHECKMATE! Player has Won!")  
          
        if surface is not None and text is not None:
          window.blit(surface, (0, 0))
          window.blit(text, text_rect)
          pygame.display.update()
      """  
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not endGame:
          if not selected_piece:            # Select the piece
            selected_piece_info = get_selected_piece(event.pos, board)
            if selected_piece_info:
              selected_piece, _ = selected_piece_info
              if selected_piece is not None and PlayerColor == selected_piece.getIsTeam():
                possible_moves = selected_piece.getPossibleMoves(board)
                update_game_state(window, board, PlayerColor)
                draw_possible_moves(window, possible_moves, board)
          else:
            
            target_square = get_square_from_position(event.pos)
            if target_square in possible_moves:  # Move the piece
              snap_piece_to_board(window, selected_piece, target_square, board)
              update_game_state(window, board, PlayerColor)
              selected_piece = None  # Deselect after moving
                    
              #Check for End Game after each move
              gameResult = board.checkEndGame()
              if gameResult == 0:
                surface, text, text_rect = board.createEndGameScreen(result= "DRAW! - Stalemate")     
              elif gameResult == 1:
                surface, text, text_rect = board.createEndGameScreen(result= "CHECKMATE! AI Bot has Won!")
              elif gameResult == -1:
                surface, text, text_rect = board.createEndGameScreen(result= "CHECKMATE! Player has Won!")  
                       
              if surface is not None and text is not None:
                window.blit(surface, (0, 0))
                window.blit(text, text_rect)
                pygame.display.update()

            else: # Select or Deselect a piece
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
    exit()

def start_screen(window):
  font = pygame.font.SysFont(None, 48)
  text = font.render("Select a team:", True, (0, 0, 0))
  text_rect = text.get_rect(center=(360, 260))

  #Choosing team buttons
  black_button = pygame.Rect(200, 360, 100, 50)
  white_button = pygame.Rect(400, 360, 100, 50)
  
  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        pygame.quit()
        exit()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if black_button.collidepoint(event.pos):
          print("You'll be playing as BLACK")          
          return False  # Return False for black team
        elif white_button.collidepoint(event.pos):
          print("You'll be playing as WHITE")
          return True  # Return True for white team
        

    window.fill((250, 235, 215))
    window.blit(text, text_rect)

    # Draw buttons
    pygame.draw.rect(window, (0, 0, 0), black_button)
    pygame.draw.rect(window, (255, 255, 255), white_button)

    pygame.display.update()

def update_game_state(window, board, PlayerColor):
  WHITE = (255, 255, 255)
  window.fill(WHITE)
  draw_board(window, board, PlayerColor)    
  draw_pieces(window, board, PlayerColor)
  
def draw_board(window, board, PlayerColor):
  DARK = (50, 103, 74)
  LIGHT = (237, 236, 233)
  RED = (198, 98, 79, 255)
  tile_size = 720 // 8
  isTeam = True if board.getTurn_counter() % 2 != 0 else False
  for row in range(8):
    for col in range(8):
      if PlayerColor:
        color = LIGHT if (row + col) % 2 == 0 else DARK
      else:
        color = DARK if (row + col) % 2 == 0 else LIGHT

      piece = board.getCell(Position(row, col)).getPiece()
      if piece is not None and isinstance(piece, King) and piece.getIsTeam()==isTeam and board.isKingInCheck(isTeam) and piece.getPosition()==Position(row, col):
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
      window.blit(circle_surface, (pos.col * square_size, pos.row * square_size))
      
    else:
      translucent_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
      pygame.draw.circle(translucent_surface, (130, 130, 130, 100), (square_size // 2, square_size // 2), 10)
      window.blit(translucent_surface, (pos.col * square_size, pos.row * square_size))

def snap_piece_to_board(window, piece, position, board):
  if piece:
    col = position.col
    row = position.row
    next_position = Position(row, col)
    if is_valid_turn(piece, board):
      possible_moves = piece.getPossibleMoves(board)
      if next_position in possible_moves:
          if (not board.checkMove(piece, next_position)):
            board.checkFiftyMoveRule(piece, next_position)
            if (isinstance(piece, King) and piece.checkCastle(board, next_position)):
              board.castle(piece, next_position)
              board.increment_turn()
            elif isinstance(piece, Pawn) and piece.checkEn_Passant(board, next_position):
              board.En_Passant(piece, next_position)
              board.increment_turn()
            else:
              board.movePiece(piece, next_position)
              if isinstance(piece, Pawn) and next_position.row==0:
                promotion_choice = promotion_screen(window, piece)
                board.promote(piece, promotion_choice)
              board.increment_turn()
            
            board.updateBoardStateHistory()
    
                
              
              
            
            
  update_game_state(window, board, PlayerColor)  # Redraw the board
 
def get_square_from_position(position):
    tile_size = 720 // 8
    col = position[0] // tile_size
    row = position[1] // tile_size
    return Position(row, col)
        
def is_valid_turn(piece, board):
    is_odd_turn = board.turn_counter % 2 != 0
    return (is_odd_turn and piece.isTeam) or (not is_odd_turn and not piece.isTeam)

def promotion_screen(window, pawn):
  col = pawn.position.col
  rect_x = col * 90

  # Choosing promotion piece buttons
  queen_button = pygame.Rect(rect_x, 0, 90, 90)
  knight_button = pygame.Rect(rect_x, 90, 90, 90)
  rook_button = pygame.Rect(rect_x, 180, 90, 90)
  bishop_button = pygame.Rect(rect_x, 270, 90, 90)
  
  color = "white" if pawn.isTeam else "black"
  queen_img = pygame.image.load(f"images/{color}-queen.png")
  knight_img = pygame.image.load(f"images/{color}-knight.png")
  rook_img = pygame.image.load(f"images/{color}-rook.png")
  bishop_img = pygame.image.load(f"images/{color}-bishop.png")
  
  # Get the piece's width and height (the pieces image size are all the same)
  piece_width, piece_height = queen_img.get_size()
  
  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        pygame.quit()
        exit()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if queen_button.collidepoint(event.pos):
          return "Queen"
        elif knight_button.collidepoint(event.pos):
          return "Knight"
        elif rook_button.collidepoint(event.pos):
          return "Rook"
        elif bishop_button.collidepoint(event.pos):
          return "Bishop"
        
    # Draw buttons
    pygame.draw.rect(window, (255, 255, 255), queen_button)
    piece_x = col * 90 + (90 - piece_width) // 2
    piece_y = 0 * 90 + (90 - piece_height) // 2
    window.blit(queen_img, (piece_x, piece_y))
    
    pygame.draw.rect(window, (255, 255, 255), knight_button)
    piece_x = col * 90 + (90 - piece_width) // 2
    piece_y = 1 * 90 + (90 - piece_height) // 2  
    window.blit(knight_img, (piece_x, piece_y))
    
    pygame.draw.rect(window, (255, 255, 255), rook_button)
    piece_x = col * 90 + (90 - piece_width) // 2
    piece_y = 2 * 90 + (90 - piece_height) // 2
    window.blit(rook_img, (piece_x, piece_y))
    
    pygame.draw.rect(window, (255, 255, 255), bishop_button)
    piece_x = col * 90 + (90 - piece_width) // 2
    piece_y = 3 * 90 + (90 - piece_height) // 2
    window.blit(bishop_img, (piece_x, piece_y))

    pygame.display.update()

def main():
  run_game()
  
if __name__ == "__main__":
  main()
  


