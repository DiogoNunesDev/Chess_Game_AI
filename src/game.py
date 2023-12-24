from Board import Board
import tkinter as tk
from PIL import Image, ImageTk

from Position import Position

def create_chessboard(root, board):
  colors = ["green", "beige"]
  image_size = 80  
  square_size = 90  
  offset = (square_size - image_size) // 2
  for row in range(8):
    for col in range(8):
      color = colors[(row + col) % 2]
      frame = tk.Frame(root, width=90, height=90, bg=color)
      frame.grid(row=row, column=col)
      frame.grid_propagate(False)
      frame.columnconfigure(0, weight=1)
      frame.rowconfigure(0, weight=1)

      cell = board.getCell(Position(row, col))
      piece = cell.getPiece()
      if piece is not None:
        image_path = piece.getName()  # Path to the image
        with Image.open(image_path) as img:
          img = img.convert("RGBA")
          img = img.resize((80, 80), Image.LANCZOS)
          tk_image = ImageTk.PhotoImage(img)
        
          label = tk.Label(root, image=tk_image)  # Placed directly on root
          label.image = tk_image  # Keep a reference
          label.place(x=col * square_size + offset, y=row * square_size + offset)  # Place on the root window
                    
          label.bind("<Button-1>", lambda event: start_drag(event))
          label.bind("<B1-Motion>", lambda event: do_drag(event))
          label.bind("<ButtonRelease-1>", lambda event, board=board, piece=piece: drop(event, board, piece))
          
          


        
def square_clicked(event, row, col):
  print(f"Square clicked at Row: {row}, Col: {col}")
  
def start_drag(event):
    # Remember the initial position of the piece
    widget = event.widget
    widget.lift()
    widget._drag_start_x = event.x_root
    widget._drag_start_y = event.y_root
    widget._start_x = widget.winfo_x()
    widget._start_y = widget.winfo_y()
    print(f'Start X: {widget._drag_start_x}, Start Y: {widget._drag_start_y}')



def do_drag(event):
    # Calculate the distance moved and move the piece
    widget = event.widget
    dx = event.x_root - widget._drag_start_x
    dy = event.y_root - widget._drag_start_y
    
    #Checking if the piece does not go outofbounds
    new_x = max(0, min(widget._start_x + dx, 90 * 7))
    new_y = max(0, min(widget._start_y + dy, 90 * 7))
    
    widget.place_configure(x=new_x, y=new_y)


def drop(event, board, piece):
    widget = event.widget
    # Calculate the center of the piece
    piece_center_x = widget.winfo_x() + widget.winfo_width() // 2
    piece_center_y = widget.winfo_y() + widget.winfo_height() // 2
    # Determine which square the center of the piece is over
    col = piece_center_x // 90
    row = piece_center_y // 90
    # Offset to center the piece in the square
    offset = (90 - widget.winfo_width()) // 2
    # Snap the piece to the center of the identified square
    next_position = Position(row, col)
    if(piece.checkMove(board, next_position)):
      #widget.place(x=col * 90 + offset, y=row * 90 + offset)
      piece.move(board, next_position)
      redraw_board(event.widget.master, board)
      print(board)
    else:
      col = piece.getPosition().getCol()
      row = piece.getPosition().getRow()
      widget.place(x=col * 90 + offset, y=row * 90 + offset)

def redraw_board(root, board):
    # Clear all existing piece images first
    for label in root.grid_slaves():
      if isinstance(label, tk.Label):
        label.grid_forget()

    # Redraw the board based on the current state of the board object
    create_chessboard(root, board)     

def main():
    board = Board()
    root = tk.Tk()
    root.title("Chess Game")
    create_chessboard(root, board)
    root.mainloop()

if __name__ == "__main__":
    main()