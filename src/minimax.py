from Pawn import Pawn
import time

class MiniMax:
  def __init__(self, board, depth, color):
    self.depth = depth
    self.color = color
    self.board = board.copy()
    
  @profile
  def minimax(self, depth, isMaximizingPLayer, alpha, beta):
    if depth == 0:
      return self.board.evaluationFunction()
    
    if isMaximizingPLayer: # If true, means white and so it is the maximizer
      maxEvaluation = float('-inf')
      for piece in self.board.getPiecesByColor(True): #White pieces want positive evaluation
        for move in piece.getPossibleMoves(self.board):
          storedState = self.board.storeStateBeforeMove(piece, move)
          
          promotion_row = 0 if piece.color == self.board.PlayerColor else 7
          self.board.movePiece(piece, move)
          if isinstance(piece, Pawn) and move[0]==promotion_row:
            self.board.promote(piece, "Queen")
          self.board.increment_turn()

          eval = self.minimax(depth - 1, False, alpha, beta)
          self.board.unmakeMove(piece, move, storedState)
          maxEvaluation = max(maxEvaluation, eval)
          alpha = max(alpha, eval)
          
          if beta <= alpha:
            break
      return maxEvaluation
    else:
      minEvaluation = float('inf')
      for piece in self.board.getPiecesByColor(False): #Black pieces want negative evaluation
        for move in piece.getPossibleMoves(self.board):
          storedState = self.board.storeStateBeforeMove(piece, move)
          
          promotion_row = 0 if piece.color == self.board.PlayerColor else 7
          self.board.movePiece(piece, move)
          if isinstance(piece, Pawn) and move[0]==promotion_row:
            self.board.promote(piece, "Queen")
          self.board.increment_turn()
               
          eval = self.minimax(depth - 1, True, alpha, beta)
          
          self.board.unmakeMove(piece, move, storedState)
          minEvaluation = min(minEvaluation, eval)
          beta = min(beta, eval)
          if alpha >= beta:
            break
      return minEvaluation
      
  @profile
  def getBestMove(self):
    bestMove = None
    bestMoveStartingPosition = None
    bestValue = float('-inf') if self.color else float('inf')
    alpha = float('-inf')
    beta = float('inf')

    for piece in self.board.getPiecesByColor(self.color):
      for move in piece.getPossibleMoves(self.board):
        storedState = self.board.storeStateBeforeMove(piece, move)
        self.board.movePiece(piece, move)
        if isinstance(piece, Pawn) and move[0] == (0 if piece.color == self.board.PlayerColor else 7):
          self.board.promote(piece, "Queen")
        self.board.increment_turn()

        value = self.minimax(self.depth - 1, self.color, alpha, beta)

        self.board.unmakeMove(piece, move, storedState)
        if (self.color and value > bestValue) or (not self.color and value < bestValue):
          bestValue = value
          bestMove = move
          bestMoveStartingPosition = piece.position
          if self.color:
            alpha = max(alpha, bestValue)
          else:
            beta = min(beta, bestValue)

    return bestMoveStartingPosition, bestMove