from Board import Board
from King import King
from model import make_move, make_random_move, minimax
import pygame


def run_game():
  pygame.init()
  width, height = 720, 720
  window = pygame.display.set_mode((width, height))
  pygame.display.set_caption("Chess Game")
  
  PlayerColor = start_screen(window)
  board = Board(PlayerColor)
  board.initializeBoard()
  board.init_all_pieces_moves()
  board.updateBoardStateHistory()
  running = True
  endGame = False
  selected_piece = None
  surface = None
  
  update_game_state(window, board)
  
  while(running):
    pygame.display.update()
    """
    if PlayerColor and board.turn_counter % 2 == 0 and not board.endGame:
      #print("ok")
      #make_random_move(board, PlayerColor)
      
      position, move = minimax(board, 4, not PlayerColor)

      piece = board.getCell(position[0], position[1]).piece
      board.checkFiftyMoveRule(piece, move)
      promotion_row = 0 if piece.color == board.PlayerColor else 7
      board.movePiece(piece, move)
      if isinstance(piece, Pawn) and move[0]==promotion_row:
        board.promote(piece, "Queen")
      board.increment_turn()
      board.updateBoardStateHistory() 
      
      update_game_state(window, board)
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
        #break
    
    elif PlayerColor and board.turn_counter % 2 != 0: 
      
      make_random_move(board, not PlayerColor)
      #board.updateBoardStateHistory()
      update_game_state(window, board)
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
        #"""
        elif event.type == pygame.MOUSEBUTTONDOWN and not endGame:
            if not selected_piece:            # Select the piece
              selected_piece = get_selected_piece(event.pos, board)
              if selected_piece:
                #if PlayerColor == selected_piece.color:
                  possible_moves = selected_piece.getPossibleMoves(board)
                  update_game_state(window, board)
                  draw_possible_moves(window, possible_moves, board)
                  print(board.convert_state_to_fenString())

            else:
              
              target_square = get_square_from_position(event.pos)
              if target_square in possible_moves:  # Move the piece
                snap_piece_to_board(window, selected_piece, target_square, board)
                update_game_state(window, board)
                selected_piece = None  # Deselect after moving
                
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

              else: # Select or Deselect a piece
                if board.getCell(target_square[0], target_square[1]).piece is not None and selected_piece is not None and selected_piece.position != board.getCell(target_square[0], target_square[1]).piece.position: 
                  #(board.getCell(target_square[0], target_square[1]).piece.color == PlayerColor and
                  selected_piece = get_selected_piece(event.pos, board)
                  if selected_piece is not None: #and PlayerColor == selected_piece.color:
                    possible_moves = selected_piece.getPossibleMoves(board)
                    update_game_state(window, board)
                    draw_possible_moves(window, possible_moves, board) 
                    pygame.display.update()
                                  
                else:
                  selected_piece = None
                  update_game_state(window, board)
                #"""     
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

def draw_board(window, board):
  DARK = (50, 103, 74)
  LIGHT = (237, 236, 233)
  RED = (198, 98, 79, 255)
  tile_size = 720 // 8
  for row in range(8):
    for col in range(8):
      if board.PlayerColor:
        color = LIGHT if (row + col) % 2 == 0 else DARK
      else:
        color = DARK if (row + col) % 2 == 0 else LIGHT

      piece = board.getCell(row, col).piece
      if piece is not None and isinstance(piece, King) and board.kingInCheck[piece.color]:
          translucent_surface = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
          translucent_surface.fill(RED)  
          window.blit(translucent_surface, (col * tile_size, row * tile_size))
      
      else:
        pygame.draw.rect(window, color, (col * tile_size, row * tile_size, tile_size, tile_size))
 
def draw_pieces(window, board):
  tile_size = 90
  for row in range(8):
    for col in range(8):
      piece = board.cells[row][col].piece
      if piece:
        piece_image = pygame.image.load(piece.path).convert_alpha()
        piece_width, piece_height = piece_image.get_size()
        piece_x = piece.position[1] * tile_size + (tile_size - piece_width) // 2
        piece_y = piece.position[0] * tile_size + (tile_size - piece_height) // 2
        window.blit(piece_image, (piece_x, piece_y))

def draw_possible_moves(window, possible_moves, board):
  square_size = 720 // 8
  for pos in possible_moves:

    piece = board.getCell(pos[0], pos[1]).piece

    if piece:
      circle_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
      pygame.draw.circle(circle_surface, (0, 0, 0, 100), (square_size // 2, square_size // 2), square_size // 2 - 2, 5)
      window.blit(circle_surface, (pos[1] * square_size, pos[0] * square_size))
      
    else:
      translucent_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
      pygame.draw.circle(translucent_surface, (0, 0, 0, 100), (square_size // 2, square_size // 2), 10)
      window.blit(translucent_surface, (pos[1] * square_size, pos[0] * square_size))
  pygame.display.update()

def update_game_state(window, board):
  draw_board(window, board)
  draw_pieces(window, board)
  pygame.display.update()

def get_selected_piece(mouse_position, board):
  tile_size = 720 // 8
  col = mouse_position[0] // tile_size
  row = mouse_position[1] // tile_size
  cell = board.getCell(row, col)
  piece = cell.piece if cell else None
  return piece

def snap_piece_to_board(window, piece, position, board):
  if piece:
    if is_valid_turn(piece, board):
      board.movePiece(piece, position)
      if (piece.piece_type == "Player_Pawn" or piece.piece_type == "Enemy_Pawn") and position[0]==0:
        promotion_choice = promotion_screen(window, piece)
        board.promote(piece, promotion_choice)
      board.increment_turn()
      board.updateBoardStateHistory()        

  update_game_state(window, board)  # Redraw the board
 
def get_square_from_position(position):
  tile_size = 720 // 8
  col = position[0] // tile_size
  row = position[1] // tile_size
  return (row, col)

def promotion_screen(window, pawn):
  col = pawn.position[1]
  rect_x = col * 90

  # Choosing promotion piece buttons
  queen_button = pygame.Rect(rect_x, 0, 90, 90)
  knight_button = pygame.Rect(rect_x, 90, 90, 90)
  rook_button = pygame.Rect(rect_x, 180, 90, 90)
  bishop_button = pygame.Rect(rect_x, 270, 90, 90)
  
  color = "white" if pawn.color else "black"
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

def is_valid_turn(piece, board):
  is_odd_turn = board.turn_counter % 2 != 0
  return (is_odd_turn and piece.color) or (not is_odd_turn and not piece.color)


def main():
  run_game()

  
  
if __name__ == "__main__":
  main()
  
