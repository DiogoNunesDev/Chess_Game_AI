import os
import chess.pgn
from stockfish import Stockfish
from multiprocessing import Pool
import csv

def init_stockfish():
  global stockfish
  stockfish = Stockfish('executables/stockfish-windows-x86-64-avx2.exe')

def evaluate_board(fen):
  stockfish.set_fen_position(fen)
  evaluation = stockfish.get_evaluation()['value']
  return fen, evaluation

def process_game(file_path):
  with open(file_path) as pgn:
    print(f"Processing {file_path}")
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

def write_evaluations_to_file(evaluations, file_name):
  with open(file_name, 'a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for fen, evaluation in evaluations:
      writer.writerow([fen, str(evaluation)])

def main():
  file_paths = [os.path.join('data', file) for file in os.listdir('data')]
  csv_file = 'chess_evaluations.csv'
  # Clear or create the CSV file and write headers
  with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['FEN', 'Evaluation'])

  for file_path in file_paths:
    print(file_path)
    fens = process_game(file_path)
    with Pool(initializer=init_stockfish) as pool:
      evaluations = pool.map(evaluate_board, fens)
      write_evaluations_to_file(evaluations, csv_file)

if __name__ == "__main__":
    main()
