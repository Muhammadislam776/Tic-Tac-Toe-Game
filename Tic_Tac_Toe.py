import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk

ASSETS = "assets/"

class TicTacToeApp:
    def __init__(self, root):  # <-- FIXED
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("540x800")
        self.root.resizable(False, False)
        self.load_assets()
        self.show_main_menu()

    def load_assets(self):
        # Load background
        self.bg_img = Image.open(ASSETS + "background.jpg").resize((540, 800))
        self.bg_tk = ImageTk.PhotoImage(self.bg_img)
        # Load X, O, button
        self.x_img = ImageTk.PhotoImage(Image.open(ASSETS + "x.png").resize((100, 100)))
        self.o_img = ImageTk.PhotoImage(Image.open(ASSETS + "o.png").resize((100, 100)))
        self.button_img = ImageTk.PhotoImage(Image.open(ASSETS + "button.png").resize((300, 60)))
        # Try to load custom font, fallback to Arial
        try:
            self.custom_font = font.Font(family="Luckiest Guy", size=28)
        except:
            self.custom_font = font.Font(family="Arial", size=28, weight="bold")

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear()
        canvas = tk.Canvas(self.root, width=540, height=800, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, anchor="nw", image=self.bg_tk)
        # Title
        canvas.create_text(270, 120, text="TIC TAC TOE", font=(self.custom_font, 50), fill="#E5B97A")
        # 1 Player Button
        btn1 = tk.Button(self.root, image=self.button_img, text="1 Player", compound="center",
                         font=(self.custom_font, 22), fg="white", bg="#8B5C2B", bd=0,
                         command=lambda: self.show_grid_menu(1))
        btn1_window = canvas.create_window(270, 350, window=btn1)
        # 2 Players Button
        btn2 = tk.Button(self.root, image=self.button_img, text="2 Players", compound="center",
                         font=(self.custom_font, 22), fg="white", bg="#8B5C2B", bd=0,
                         command=lambda: self.show_grid_menu(2))
        btn2_window = canvas.create_window(270, 430, window=btn2)

    def show_grid_menu(self, num_players):
        self.num_players = num_players
        self.clear()
        canvas = tk.Canvas(self.root, width=540, height=800, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, anchor="nw", image=self.bg_tk)
        canvas.create_text(270, 120, text="CHOOSE A GRID", font=(self.custom_font, 38), fill="#E5B97A")
        # Grid buttons
        btn3 = tk.Button(self.root, image=self.button_img, text="3 X 3", compound="center",
                         font=(self.custom_font, 22), fg="white", bg="#8B5C2B", bd=0,
                         command=lambda: self.start_game(3))
        btn5 = tk.Button(self.root, image=self.button_img, text="5 X 5", compound="center",
                         font=(self.custom_font, 22), fg="white", bg="#8B5C2B", bd=0,
                         command=lambda: self.start_game(5))
        btn7 = tk.Button(self.root, image=self.button_img, text="7 X 7", compound="center",
                         font=(self.custom_font, 22), fg="white", bg="#8B5C2B", bd=0,
                         command=lambda: self.start_game(7))
        canvas.create_window(140, 300, window=btn3)
        canvas.create_window(270, 400, window=btn5)
        canvas.create_window(400, 500, window=btn7)

    def start_game(self, grid_size):
        self.grid_size = grid_size
        self.clear()
        self.board = [[None for _ in range(grid_size)] for _ in range(grid_size)]
        self.turn = "X"
        self.moves = 0
        self.cells = [[None for _ in range(grid_size)] for _ in range(grid_size)]
        self.game_canvas = tk.Canvas(self.root, width=540, height=800, highlightthickness=0)
        self.game_canvas.pack(fill="both", expand=True)
        self.game_canvas.create_image(0, 0, anchor="nw", image=self.bg_tk)
        # Title
        self.turn_text = self.game_canvas.create_text(270, 60, text="Player 1 to move",
                                                     font=(self.custom_font, 28), fill="white")
        # Draw grid
        self.draw_grid()
        # Bind click
        self.game_canvas.bind("<Button-1>", self.on_click)
        # Message
        self.msg_text = self.game_canvas.create_text(270, 720, text=f"PLACE {3 if grid_size==3 else 4} IN A ROW!",
                                                     font=(self.custom_font, 22), fill="white")

    def draw_grid(self):
        size = self.grid_size
        cell = 480 // size
        offset_x = (540 - 480) // 2
        offset_y = 120
        for i in range(size + 1):
            x = offset_x + i * cell
            self.game_canvas.create_line(x, offset_y, x, offset_y + cell * size, width=6, fill="#7b4a14")
            y = offset_y + i * cell
            self.game_canvas.create_line(offset_x, y, offset_x + cell * size, y, width=6, fill="#7b4a14")
        self.cell_size = cell
        self.offset_x = offset_x
        self.offset_y = offset_y

    def on_click(self, event):
        x, y = event.x, event.y
        row = (y - self.offset_y) // self.cell_size
        col = (x - self.offset_x) // self.cell_size
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            if self.board[row][col] is None:
                self.place_piece(row, col)

    def place_piece(self, row, col):
        x = self.offset_x + col * self.cell_size + self.cell_size // 2
        y = self.offset_y + row * self.cell_size + self.cell_size // 2
        img = self.x_img if self.turn == "X" else self.o_img
        self.cells[row][col] = self.game_canvas.create_image(x, y, image=img)
        self.board[row][col] = self.turn
        self.moves += 1
        if self.check_winner(row, col):
            self.show_winner()
        elif self.moves == self.grid_size ** 2:
            self.show_draw()
        else:
            self.turn = "O" if self.turn == "X" else "X"
            player_num = 1 if self.turn == "X" else 2
            self.game_canvas.itemconfig(self.turn_text, text=f"Player {player_num} to move")

    def check_winner(self, row, col):
        n = self.grid_size
        win_len = 3 if n == 3 else 4
        directions = [(1,0), (0,1), (1,1), (1,-1)]
        for dx, dy in directions:
            count = 1
            for dir in [1, -1]:
                for i in range(1, win_len):
                    r = row + dx * i * dir
                    c = col + dy * i * dir
                    if 0 <= r < n and 0 <= c < n and self.board[r][c] == self.turn:
                        count += 1
                    else:
                        break
            if count >= win_len:
                return True
        return False

    def show_winner(self):
        self.game_canvas.unbind("<Button-1>")
        self.popup("PLAYER 1 WINS!!!" if self.turn == "X" else "PLAYER 2 WINS!!!")

    def show_draw(self):
        self.game_canvas.unbind("<Button-1>")
        self.popup("DRAW!!!")

    def popup(self, message):
        # Popup background
        popup = tk.Toplevel(self.root)
        popup.geometry("400x250+600+300")
        popup.overrideredirect(True)
        popup.attributes("-topmost", True)
        canvas = tk.Canvas(popup, width=400, height=250, highlightthickness=0)
        canvas.pack()
        # Wood background
        bg = Image.open(ASSETS + "button.png").resize((400, 250))
        bg_tk = ImageTk.PhotoImage(bg)
        canvas.create_image(0, 0, anchor="nw", image=bg_tk)
        # Message
        canvas.create_text(200, 60, text=message, font=(self.custom_font, 28), fill="white")
        # Play Again button
        btn = tk.Button(popup, image=self.button_img, text="PLAY AGAIN", compound="center",
                        font=(self.custom_font, 22), fg="white", bg="#8B5C2B", bd=0,
                        command=lambda: [popup.destroy(), self.show_main_menu()])
        canvas.create_window(200, 180, window=btn)
        # Keep a reference to avoid garbage collection
        popup.bg_tk = bg_tk

if __name__ == "__main__":  # <-- FIXED
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()