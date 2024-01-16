import copy
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
    self.doInitialPositioning()
    
  def getTurn_counter(self):
    return self.turn_counter
  
  def increment_turn(self):
    self.turn_counter += 1  
  
  def getCell(self, position):
    return self.cells[position.getRow()][position.getCol()]     
  
  def doInitialPositioning(self):
    
    for row in range(8):
      for col in range(8):
        #BLACK PIECES        
        if(row == 0):
          if(col == 0 or col == 7):
            rook = Rook(position=Position(row, col), isTeam= not self.PlayerColor)
            self.cells[row][col].setPiece(rook)
          
          elif(col == 1 or col == 6):
            knight = Knight(position=Position(row, col), isTeam= not self.PlayerColor)
            self.cells[row][col].setPiece(knight)
          
          elif(col == 2 or col == 5):
            bishop = Bishop(position=Position(row, col), isTeam= not self.PlayerColor)
            self.cells[row][col].setPiece(bishop)
            
          elif(col == 3):
            queen = Queen(position=Position(row, col), isTeam= not self.PlayerColor)
            self.cells[row][col].setPiece(queen)
            
          elif(col == 4):
            king = King(position=Position(row, col), isTeam= not self.PlayerColor)
            self.cells[row][col].setPiece(king)
            
        elif(row == 1):
          pawn = Pawn(position=Position(row, col), isTeam= not self.PlayerColor)
          self.cells[row][col].setPiece(pawn)
          
        #WHITE PIECES
        elif(row == 6):
          pawn = Pawn(position=Position(row, col), isTeam=self.PlayerColor)
          self.cells[row][col].setPiece(pawn)
          
        elif(row == 7):
          if(col == 0 or col == 7):
            rook = Rook(position=Position(row, col), isTeam=self.PlayerColor)
            self.cells[row][col].setPiece(rook)
          
          elif(col == 1 or col == 6):
            knight = Knight(position=Position(row, col), isTeam=self.PlayerColor)
            self.cells[row][col].setPiece(knight)
          
          elif(col == 2 or col == 5):
            bishop = Bishop(position=Position(row, col), isTeam=self.PlayerColor)
            self.cells[row][col].setPiece(bishop)
            
          elif(col == 4):
            king = King(position=Position(row, col), isTeam=self.PlayerColor)
            self.cells[row][col].setPiece(king)
            
          elif(col == 3):
            queen = Queen(position=Position(row, col), isTeam=self.PlayerColor)
            self.cells[row][col].setPiece(queen)
    
  def getEnemyPieces(self):
    enemyPieces = []
    for row in range(8):
      for col in range(8):
        position = Position(row, col)
        piece = self.getCell(position).getPiece()
        if piece is not None and piece.getIsTeam()!=self.PlayerColor:
          enemyPieces.append(piece)
          
    return enemyPieces
  
  def getTeamPieces(self):
    teamPieces = []
    for row in range(8):
      for col in range(8):
        position = Position(row, col)
        piece = self.getCell(position).getPiece()
        if piece is not None and piece.getIsTeam()==self.PlayerColor:
          teamPieces.append(piece)
          
    return teamPieces
  
  def getKingPosition(self, isTeam):
    kingPosition = None
    for row in range(8):
      for col in range(8):
        position = Position(row, col)
        piece = self.getCell(position).getPiece()
        if piece is not None and piece.isTeam==isTeam and isinstance(piece, King):
          kingPosition = position
    
    return kingPosition
  
  def isSquareUnderAttack(self, cell, isTeamAttacking):
    pieces = self.getTeamPieces() if isTeamAttacking==self.PlayerColor else self.getEnemyPieces()
    for piece in pieces:
      if cell.getPosition() in piece.getMoves(self):
        return True
    return False
  
  def isKingInCheck(self, isTeam):
    kingPosition = self.getKingPosition(isTeam)
    if kingPosition is not None:
      kingCell = self.getCell(kingPosition)
      opponentColor = not isTeam
      return self.isSquareUnderAttack(kingCell, opponentColor)
    
  def simulateMove(self, piece, newPosition):
    tempBoard = copy.deepcopy(self)
    tempPiece = tempBoard.getCell(piece.getPosition()).getPiece()
    tempPiece.move(tempBoard, newPosition)  
    return tempBoard
  
  def checkCastleUnderAttack(self, piece, row, col):
    if col==0:
      if (not (self.isSquareUnderAttack(self.getCell(Position(row, 1)), not piece.isTeam)) and 
          (not self.isSquareUnderAttack(self.getCell(Position(row, 2)), not piece.isTeam)) and 
          (not self.isSquareUnderAttack(self.getCell(Position(row, 3)), not piece.isTeam)) and 
          (not self.isSquareUnderAttack(self.getCell(Position(row, 4)), not piece.isTeam))):
          return True
    elif col==7:
      if (not (self.isSquareUnderAttack(self.getCell(Position(row, 4)), not piece.isTeam)) and 
          (not self.isSquareUnderAttack(self.getCell(Position(row, 5)), not piece.isTeam)) and 
          (not self.isSquareUnderAttack(self.getCell(Position(row, 6)), not piece.isTeam))):
          return True
    return False
  
  def castle(self, piece, next_position):
    if piece is not None and isinstance(piece, King) and not piece.hasMoved: #If piece is a King
      row = 7 if piece.isTeam==self.PlayerColor else 0
      col = 7 if (next_position.getCol() > piece.getPosition().getCol()) else 0 
      if self.checkCastleUnderAttack(piece, row, col):
        rook = self.getCell(Position(row,col)).getPiece()
        if rook is not None and isinstance(rook, Rook) and not rook.getHasMoved():
          self.castleMove(row, col, piece, rook)
    
    elif piece is not None and isinstance(piece, Rook) and not piece.hasMoved:  #If piece is a Rook
      row = 7 if piece.isTeam==self.PlayerColor else 0
      king_col = 4
      col = piece.getPosition().getCol()
      if self.checkCastleUnderAttack(piece, row, piece.getPosition().getCol()):
        king = self.getCell(Position(row, king_col)).getPiece()
        if king is not None and isinstance(king, King) and not king.getHasMoved():
          self.castleMove(row, col, king, piece)
  
  def castleMove(self, row, col, king, rook):
    king_col = 2 if col == 0 else 6
    rook_col = 3 if col == 0 else 5
    self.getCell(king.getPosition()).setPiece(None)
    self.getCell(rook.getPosition()).setPiece(None)
    king.setPosition(Position(row, king_col))  
    rook.setPosition(Position(row, rook_col))
    self.getCell(king.getPosition()).setPiece(king)
    self.getCell(rook.getPosition()).setPiece(rook)
    king.setHasMoved(True)
    rook.setHasMoved(True)
            
  def En_Passant(self, piece, next_position):
    direction = 1 if piece.getIsTeam() else -1
    self.getCell(piece.getPosition()).setPiece(None)
    self.getCell(next_position).setPiece(piece)
    self.getCell(Position(next_position.getRow()+direction, next_position.getCol())).setPiece(None)
    
  def __str__(self):
    board_str = ""
    for row in range(8):
        row_str = " | ".join(self.cells[row][col].getPiece().getName() if self.cells[row][col].getPiece() else "Empty" for col in range(8))
        board_str += row_str + "\n" + ("-" * 50) + "\n"
    return board_str

  def checkEndGame(self):
    
    if self.isKingInCheck(self.PlayerColor):
      pieces = self.getTeamPieces()
      for piece in pieces:
        if piece.getPossibleMoves() is not None:
          return False
            
      print("CHECKMATE! AI Bot has Won!")    
      return True
    
    elif self.isKingInCheck(not self.PlayerColor):
      pieces = self.getTeamPieces()
      for piece in pieces:
        if piece.getPossibleMoves() is not None:
          return False
      
      print("CHECKMATE! Player has Won!")    
      return True
    
    elif not self.isKingInCheck(self.PlayerColor):
      pieces = self.getTeamPieces()
      if len(pieces) == 1:
        if pieces[0].getPossibleMoves() is not None:
          return False  
        
        print("DRAW! No possible moves left!")    
        return True
    
    elif not self.isKingInCheck(not self.PlayerColor):
      pieces = self.getTeamPieces()
      if len(pieces) == 1:
        if pieces[0].getPossibleMoves() is not None:
          return False  
        
        print("DRAW! No possible moves left!")    
        return True
    
    return False
    