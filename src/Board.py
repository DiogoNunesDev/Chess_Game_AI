from Cell import Cell
from Position import Position
from Bishop import Bishop
from King import King
from Knight import Knight
from Pawn import Pawn
from Queen import Queen
from Rook import Rook


class Board:
  
  def __init__(self):
    self.cells = [[None for _ in range(8)] for _ in range(8)]
    for i in range(8):
      for j in range(8):
        position = Position(i, j)
        self.cells[i][j] = Cell(position, None)
    
    self.doInitialPositioning()
    
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
            
          elif(col == 3):
            king = King(position=Position(row, col), isWhite=True)
            self.cells[row][col].setPiece(king)
            
          elif(col == 4):
            queen = Queen(position=Position(row, col), isWhite=True)
            self.cells[row][col].setPiece(queen)
    
  def __str__(self):
    board_str = ""
    for row in range(8):
        row_str = " | ".join(self.cells[row][col].getPiece().getName() if self.cells[row][col].getPiece() else "Empty" for col in range(8))
        board_str += row_str + "\n" + ("-" * 50) + "\n"
    return board_str
