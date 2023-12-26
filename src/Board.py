import copy
from Cell import Cell
from Position import Position
from Bishop import Bishop
from King import King
from Knight import Knight
from Pawn import Pawn
from Queen import Queen
from Rook import Rook
from Piece import Piece


class Board:
  
  def __init__(self):
    self.cells = [[None for _ in range(8)] for _ in range(8)]
    for i in range(8):
      for j in range(8):
        position = Position(i, j)
        self.cells[i][j] = Cell(position, None)
        
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
            rook = Rook(position=Position(row, col), isWhite=False)
            self.cells[row][col].setPiece(rook)
          
          elif(col == 1 or col == 6):
            knight = Knight(position=Position(row, col), isWhite=False)
            self.cells[row][col].setPiece(knight)
          
          elif(col == 2 or col == 5):
            bishop = Bishop(position=Position(row, col), isWhite=False)
            self.cells[row][col].setPiece(bishop)
            
          elif(col == 3):
            queen = Queen(position=Position(row, col), isWhite=False)
            self.cells[row][col].setPiece(queen)
            
          elif(col == 4):
            king = King(position=Position(row, col), isWhite=False)
            self.cells[row][col].setPiece(king)
            
        elif(row == 1):
          pawn = Pawn(position=Position(row, col), isWhite=False)
          self.cells[row][col].setPiece(pawn)
          
        #WHITE PIECES
        elif(row == 6):
          pawn = Pawn(position=Position(row, col), isWhite=True)
          self.cells[row][col].setPiece(pawn)
          
        elif(row == 7):
          if(col == 0 or col == 7):
            rook = Rook(position=Position(row, col), isWhite=True)
            self.cells[row][col].setPiece(rook)
          
          elif(col == 1 or col == 6):
            knight = Knight(position=Position(row, col), isWhite=True)
            self.cells[row][col].setPiece(knight)
          
          elif(col == 2 or col == 5):
            bishop = Bishop(position=Position(row, col), isWhite=True)
            self.cells[row][col].setPiece(bishop)
            
          elif(col == 4):
            king = King(position=Position(row, col), isWhite=True)
            self.cells[row][col].setPiece(king)
            
          elif(col == 3):
            queen = Queen(position=Position(row, col), isWhite=True)
            self.cells[row][col].setPiece(queen)
    
  def getBlackPieces(self):
    blackPieces = []
    for row in range(8):
      for col in range(8):
        position = Position(row, col)
        piece = self.getCell(position).getPiece()
        if piece is not None and not piece.getIsWhite():
          blackPieces.append(piece)
          
    return blackPieces
  
  def getWhitePieces(self):
    whitePieces = []
    for row in range(8):
      for col in range(8):
        position = Position(row, col)
        piece = self.getCell(position).getPiece()
        if piece is not None and piece.getIsWhite():
          whitePieces.append(piece)
          
    return whitePieces
  
  def getKingPosition(self, isWhite):
    kingPosition = None
    for row in range(8):
      for col in range(8):
        position = Position(row, col)
        piece = self.getCell(position).getPiece()
        if piece is not None and piece.getIsWhite()==isWhite and isinstance(piece, King):
          kingPosition = position
    
    return kingPosition
  
  def isSquareUnderAttack(self, cell, isWhiteAttacking):
    pieces = self.getWhitePieces() if isWhiteAttacking else self.getBlackPieces()
    for piece in pieces:
      if cell.getPosition() in piece.getPossibleMoves(self):
        return True
    return False
  
  def isKingInCheck(self, isWhite):
    kingPosition = self.getKingPosition(isWhite)
    kingCell = self.getCell(kingPosition)
    opponentColor = not isWhite
    return self.isSquareUnderAttack(kingCell, opponentColor)
  
  def simulateMove(self, piece, newPosition):
    tempBoard = copy.deepcopy(self)
    tempPiece = tempBoard.getCell(piece.getPosition()).getPiece()
    tempPiece.move(tempBoard, newPosition)  
    return tempBoard
  
  def checkCastleUnderAttack(self, piece, row, col):
    if col==0:
      if (not (self.isSquareUnderAttack(self.getCell(Position(row, 1)), piece.isWhite)) and 
          (not self.isSquareUnderAttack(self.getCell(Position(row, 2)), piece.isWhite)) and 
          (not self.isSquareUnderAttack(self.getCell(Position(row, 3)), piece.isWhite)) and 
          (not self.isSquareUnderAttack(self.getCell(Position(row, 4)), self.isWhite))):
          return True
    elif col==7:
      if (not (self.isSquareUnderAttack(self.getCell(Position(row, 4)), piece.isWhite)) and 
          (not self.isSquareUnderAttack(self.getCell(Position(row, 5)), piece.isWhite)) and 
          (not self.isSquareUnderAttack(self.getCell(Position(row, 6)), piece.isWhite))):
          return True
    return False
  
  def castle(self, piece, next_position):
    if piece is not None and isinstance(piece, King) and not piece.hasMoved: #If piece is a King
      row = 7 if piece.isWhite else 0
      col = 7 if (next_position.getCol() > piece.getPosition().getCol()) else 0 
      if self.checkCastleUnderAttack(piece, row, col):
        rook = self.getCell(Position(row,col)).getPiece()
        if rook is not None and isinstance(rook, Rook) and not rook.getHasMoved():
          #if piece.checkCastle(self, next_position):
          self.castleMove(row, col, piece, rook)
    
    elif piece is not None and isinstance(piece, Rook) and not piece.hasMoved:  #If piece is a Rook
      row = 7 if piece.isWhite else 0
      col = 4
      if self.checkCastleUnderAttack(piece, row, piece.getPosition().getCol()):
        king = self.getCell(Position(row, col)).getPiece()
        if king is not None and isinstance(king, King) and not king.getHasMoved():
          #if piece.checkCastle(self, next_position):
          self.castleMove(row, col, piece, rook)
  
  def castleMove(self, row, col, king, rook):
    king_col = 2 if col == 0 else 6
    rook_col = 3 if col == 0 else 5
    self.getCell(king.getPosition()).setPiece(None)
    self.getCell(rook.getPosition()).setPiece(None)
    king.setPosition(Position(row, king_col))  
    rook.setPosition(Position(row, rook_col))
    self.getCell(king.getPosition()).setPiece(king)
    self.getCell(rook.getPosition()).setPiece(rook)
            
  def En_Passant(self, piece, next_position):
    direction = 1 if piece.getIsWhite() else -1
    self.getCell(piece.getPosition()).setPiece(None)
    self.getCell(next_position).setPiece(piece)
    self.getCell(Position(next_position.getRow()+direction, next_position.getCol())).setPiece(None)
    
  def __str__(self):
    board_str = ""
    for row in range(8):
        row_str = " | ".join(self.cells[row][col].getPiece().getName() if self.cells[row][col].getPiece() else "Empty" for col in range(8))
        board_str += row_str + "\n" + ("-" * 50) + "\n"
    return board_str
