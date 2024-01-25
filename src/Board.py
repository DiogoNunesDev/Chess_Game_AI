import copy
import pygame
from Cell import Cell
from Position import Position
from Bishop import Bishop
from King import King
from Knight import Knight
from Pawn import Pawn
from Queen import Queen
from Rook import Rook

class Board:
  
  def __init__(self, PlayerColor):
    self.cells = [[None for _ in range(8)] for _ in range(8)]
    for i in range(8):
      for j in range(8):
        position = Position(i, j)
        self.cells[i][j] = Cell(position, None)

    self.PlayerColor = PlayerColor
    self.turn_counter = 1
    self.endGame = False
    self.fiftyMoveRule_checker = 0
    self.boardStateHistory = {}
    self.attackedSquares = {True: set(), False: set()}
    self.kingPositions = {True: None, False: None}
    self.doInitialPositioning()
    self.updateBoardStateHistory()
    
  def getTurn_counter(self):
    return self.turn_counter
  
  def increment_turn(self):
    self.turn_counter += 1  
  
  def getCell(self, position):
    return self.cells[position.row][position.col]  
  
  def getCell_2(self, row, col):
    return self.cells[row][col] 
  
  def updateBoardStateHistory(self):
    current_state = self.__str__()

    if current_state in self.boardStateHistory:
      self.boardStateHistory[current_state] += 1
    else:
      self.boardStateHistory[current_state] = 1
  
  def getPieces(self):
    pieces = []
    for row in range(8):
      for col in range(8):
        piece = self.getCell_2(row, col).piece
        if piece is not None:# and len(piece.getPossibleMoves(self)) > 0:
          pieces.append(piece)

    # If no legal moves, return (e.g., checkmate or stalemate)
    if not pieces:
        return None

    return pieces
  
  def doInitialPositioning(self):
    
    for row in range(8):
      for col in range(8):
        #BLACK PIECES        
        if(row == 0):
          if(col == 0 or col == 7):
            rook = Rook(position=Position(row, col), isTeam= not self.PlayerColor)
            self.cells[row][col].piece = rook
          
          elif(col == 1 or col == 6):
            knight = Knight(position=Position(row, col), isTeam= not self.PlayerColor)
            self.cells[row][col].piece = knight
          
          elif(col == 2 or col == 5):
            bishop = Bishop(position=Position(row, col), isTeam= not self.PlayerColor)
            self.cells[row][col].piece = bishop
            
          elif(col == 3):
            queen = Queen(position=Position(row, col), isTeam= not self.PlayerColor)
            self.cells[row][col].piece = queen
            
          elif(col == 4):
            king = King(position=Position(row, col), isTeam= not self.PlayerColor)
            self.cells[row][col].piece = king
            self.kingPositions[not self.PlayerColor] = Position(row, col)
            
        elif(row == 1):
          pawn = Pawn(position=Position(row, col), isTeam= not self.PlayerColor)
          self.cells[row][col].piece = pawn
          
        #WHITE PIECES
        elif(row == 6):
          pawn = Pawn(position=Position(row, col), isTeam=self.PlayerColor)
          self.cells[row][col].piece = pawn
          
        elif(row == 7):
          if(col == 0 or col == 7):
            rook = Rook(position=Position(row, col), isTeam=self.PlayerColor)
            self.cells[row][col].piece = rook
          
          elif(col == 1 or col == 6):
            knight = Knight(position=Position(row, col), isTeam=self.PlayerColor)
            self.cells[row][col].piece = knight
          
          elif(col == 2 or col == 5):
            bishop = Bishop(position=Position(row, col), isTeam=self.PlayerColor)
            self.cells[row][col].piece = bishop
            
          elif(col == 4):
            king = King(position=Position(row, col), isTeam=self.PlayerColor)
            self.cells[row][col].piece = king
            self.kingPositions[self.PlayerColor] = Position(row, col)
            
          elif(col == 3):
            queen = Queen(position=Position(row, col), isTeam=self.PlayerColor)
            self.cells[row][col].piece = queen
    
  def getEnemyPieces(self):
    enemyPieces = []
    for row in range(8):
      for col in range(8):
        position = Position(row, col)
        piece = self.getCell_2(position.row, position.col).piece
        if piece is not None and piece.getIsTeam()!=self.PlayerColor:
          enemyPieces.append(piece)
          
    return enemyPieces
  
  def getTeamPieces(self):
    teamPieces = []
    for row in range(8):
      for col in range(8):
        position = Position(row, col)
        piece = self.getCell_2(position.row, position.col).piece
        if piece is not None and piece.getIsTeam()==self.PlayerColor:
          teamPieces.append(piece)
          
    return teamPieces

  def isSquareUnderAttack(self, position, isTeamAttacking):
    # Check if the position is in the set of attacked squares for the attacking team
    return position in self.attackedSquares[isTeamAttacking]
  @profile
  def updateAttackedSquares(self):
    self.attackedSquares = {True: set(), False: set()}  # Reset the cache
    for row in range(8):
      for col in range(8):
        piece = self.getCell_2(row, col).piece
        if piece is not None:          
          moves = piece.getMoves(self)
          self.attackedSquares[piece.isTeam].update(moves)
  
  def isKingInCheck(self, isTeam): 
    king = self.getCell_2(self.kingPositions[isTeam].row, self.kingPositions[isTeam].col)
    KingInCheck = king.position in self.attackedSquares[not isTeam]
    if KingInCheck:
      king.isInCheck=True 
    else: 
      king.isInCheck = False
      
    return KingInCheck
  
  def checkMove(self, piece, newPosition):
    checkFlag = False
    piece_OriginalHasMoved = piece.hasMoved
    original_position = piece.position
    captured_piece = self.getCell_2(newPosition.row, newPosition.col).piece
    self.movePiece(piece, newPosition)
    if (self.isKingInCheck(piece.isTeam)):
      checkFlag = True
    #Reversing the simulation
    self.movePiece(piece, original_position)
    piece.hasMoved = piece_OriginalHasMoved
    if captured_piece: #If the simulated move resulted in a capture, it is reversed
      self.getCell_2(newPosition.row, newPosition.col).piece = captured_piece
      captured_piece.position = newPosition
    
    return checkFlag
  
  def checkCastleUnderAttack(self, piece, row, col):
    print(col)
    if col==0:
      if (not (self.isSquareUnderAttack(self.getCell_2(row, 1), not piece.isTeam)) and 
          (not self.isSquareUnderAttack(self.getCell_2(row, 2), not piece.isTeam)) and 
          (not self.isSquareUnderAttack(self.getCell_2(row, 3), not piece.isTeam)) and 
          (not self.isSquareUnderAttack(self.getCell_2(row, 4), not piece.isTeam))):
          return True
    elif col==7:
     
      if (not (self.isSquareUnderAttack(self.getCell_2(row, 4), not piece.isTeam)) and 
          (not self.isSquareUnderAttack(self.getCell_2(row, 5), not piece.isTeam)) and 
          (not self.isSquareUnderAttack(self.getCell_2(row, 6), not piece.isTeam))):
          return True
    return False
  
  def castle(self, piece, next_position):
    if isinstance(piece, King) and not piece.hasMoved:
      row = 7 if piece.isTeam == self.PlayerColor else 0
      direction = 1 if (next_position.col > piece.getPosition().col) else -1
      rook_col = 7 if direction > 0 else 0
      if self.checkCastleUnderAttack(piece, row, rook_col):
        rook = self.getCell_2(row, rook_col).piece
        if isinstance(rook, Rook):
          if not rook.hasMoved:
            self.castleMove(row, direction, piece, rook)

  def castleMove(self, row, direction, king, rook):
    king_col = 6 if direction > 0 else 2
    rook_col = 5 if direction > 0 else 3
    self.movePiece(king, Position(row, king_col))
    self.kingPositions[king.isTeam] = Position(row, king_col)
    self.movePiece(rook, Position(row, rook_col))
  
  def movePiece(self, piece, new_position):
    start_row = 6 if piece.isTeam==self.PlayerColor else 1
    end_row = 4 if piece.isTeam==self.PlayerColor else 3
    if isinstance(piece, Pawn) and piece.position.row == start_row and new_position.row == end_row:
      piece.setEn_Passant(self.turn_counter)
      
    self.cells[piece.position.row][piece.position.col].piece = None  
    self.cells[new_position.row][new_position.col].piece = piece
    piece.position = new_position  
    piece.hasMoved = True
    if isinstance(piece, King):
      self.kingPositions[piece.isTeam] = new_position
      
    self.updateAttackedSquares()
            
  def En_Passant(self, piece, next_position):
    direction = 1 if piece.getIsTeam() else -1
    self.getCell_2(piece.position.row, piece.position.col).piece = None
    self.getCell_2(next_position.row, next_position.col).piece = piece
    self.getCell_2(next_position.row + direction, next_position.col).piece = None
    
  def promote(self, piece, choice):
    if piece is not None and isinstance(piece, Pawn):
      row = piece.position.row
      col = piece.position.col
      if choice == "Queen":
        self.getCell_2(row, col).piece = None
        queen = Queen(position=piece.position, isTeam=piece.isTeam)
        self.getCell_2(row, col).piece = queen
      elif choice == "Knight":
        self.getCell_2(row, col).piece = None
        knight = Knight(position=piece.position, isTeam=piece.isTeam)
        self.getCell_2(row, col).piece = knight
      elif choice == "Rook":
        self.getCell_2(row, col).piece = None
        rook = Rook(position=piece.position, isTeam=piece.isTeam)
        self.getCell_2(row, col).piece = rook
      elif choice == "Bishop":
        self.getCell_2(row, col).piece = None
        bishop = Bishop(position=piece.position, isTeam=piece.isTeam)
        self.getCell_2(row, col).piece = bishop
     
  def __str__(self):
    board_str = ""
    for row in range(8):
        row_str = " | ".join(self.cells[row][col].piece.getName() if self.cells[row][col].piece else "Empty" for col in range(8))
        board_str += row_str + "\n" + ("-" * 50) + "\n"
    return board_str
  
  def checkFiftyMoveRule(self, piece, next_position):
    if isinstance(piece, Pawn) or (self.getCell_2(next_position.row, next_position.col).piece is not None and self.getCell_2(next_position.row, next_position.col).piece.isTeam != self.PlayerColor):
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
    if len(self.getPieces()) == 3:
      for piece in self.getPieces():
        if isinstance(piece, Bishop) or isinstance(piece, Knight):
          return True
        
    elif len(self.getPieces()) == 2:
      return True
    
    elif len(self.getPieces()) == 4: #Draw if there is a king and a bishop on both sides
      #Since even when the bishops are of oposite square colors, it is extremly dificult to lead to checkmate so lets consider it a draw
      count = 0
      for piece in self.getTeamPieces():
        if isinstance(piece, Bishop):
          count+=1
      for piece in self.getEnemyPieces():
        if isinstance(piece, Bishop):
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
        pieces = self.getTeamPieces()
        for piece in pieces:
          if len(piece.getPossibleMoves(self)) != 0:
            return False
        
        return True
    
    #STALEMATE
    elif not self.isKingInCheck(not self.PlayerColor):
        pieces = self.getEnemyPieces()
        for piece in pieces:
          if len(piece.getPossibleMoves(self)) != 0:
            return False
        
        return True

    return False
      
  def checkEndGame(self):
    if self.isKingInCheck(self.PlayerColor):
      pieces = self.getTeamPieces()
      for piece in pieces:
        if len(piece.getPossibleMoves(self)) != 0:
          return None
         
      self.endGame = True
      return 1
    
    elif self.isKingInCheck(not self.PlayerColor):
      pieces = self.getEnemyPieces()
      for piece in pieces:
        if len(piece.getPossibleMoves(self)) != 0:
          return None
      
      self.endGame = True
      return -1
    
    elif self.checkDraw():
      self.endGame = True
      return 0
    
    #DRAW
    
    
    return None
    
