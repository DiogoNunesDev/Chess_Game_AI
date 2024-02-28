import os
import chess.pgn
from stockfish import Stockfish
from multiprocessing import Pool
import csv

def evaluate_board(fen):
  stockfish = Stockfish('executables/stockfish-windows-x86-64-avx2.exe')
  stockfish.set_fen_position(fen)
  return fen, stockfish.get_evaluation()['value']

def process_game(file_path):
  with open(file_path) as pgn:
    fens = []
    while True:
      game = chess.pgn.read_game(pgn)
      if game is None:
        break
      board = game.board()
      for move in game.mainline_moves():
        board.push(move)
        fens.append(board.fen())
    return fens

def save_evaluations_to_file(evaluations, file_name='chess_evaluations.csv'):
  with open(file_name, 'a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for fen, evaluation in evaluations:
      writer.writerow([fen, str(evaluation)])

def main():
    
  with open('chess_evaluations.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['FEN', 'Evaluation'])

  file_paths = [os.path.join('data', file) for file in os.listdir('data') if file == 'Carlsen.pgn']

  # Extract FENs from games
  all_fens = []
  for file_path in file_paths:
    all_fens.extend(process_game(file_path))

  # Use of multithreading for board state evaluation using stockfish
  with Pool() as pool:
    evaluations = pool.map(evaluate_board, all_fens)

  save_evaluations_to_file(evaluations)

if __name__ == "__main__":
    main()
