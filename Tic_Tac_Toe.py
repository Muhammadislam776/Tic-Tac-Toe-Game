import tkinter as tk
from PIL import Image, ImageTk
import os
import random

ASSETS = "assets/"  # Folder with images

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("540x872")
        self.root.resizable(False, False)
        self.menu_screen()

    def menu_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.canvas = tk.Canvas(self.root, width=540, height=872, bg="#4E2508", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        banner_img_path = os.path.join(ASSETS, "main_menu.png")
        banner_img = Image.open(banner_img_path).resize((350, 350))
        self.banner_img = ImageTk.PhotoImage(banner_img)
        self.canvas.create_image(270, 230, image=self.banner_img)

        self.btn_1p_img = ImageTk.PhotoImage(Image.open(os.path.join(ASSETS, "1player.png")).resize((250, 45)))
        self.btn_2p_img = ImageTk.PhotoImage(Image.open(os.path.join(ASSETS, "2player.png")).resize((250, 45)))

        btn_1p = tk.Button(self.root, image=self.btn_1p_img, bd=0, highlightthickness=0,
                           command=lambda: self.start_game(vs_computer=True), cursor="hand2",
                           bg="#4E2508", activebackground="#4E2508")
        btn_2p = tk.Button(self.root, image=self.btn_2p_img, bd=0, highlightthickness=0,
                           command=lambda: self.start_game(vs_computer=False), cursor="hand2",
                           bg="#4E2508", activebackground="#4E2508")

        # Updated button placement: shifted up and closer
        self.canvas.create_window(270, 500, window=btn_1p, width=300, height=56)
        self.canvas.create_window(270, 565, window=btn_2p, width=300, height=56)


    def start_game(self, vs_computer=False):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.vs_computer = vs_computer
        self.game_over = False
        self.current_player = "X"
        self.board = [[None]*3 for _ in range(3)]
        self.cells = [[None]*3 for _ in range(3)]

        self.canvas = tk.Canvas(self.root, width=540, height=872, bg="#8B5E3C", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        padding_top = 150
        padding_left = 120
        cell_size = 100

        for i in range(4):
            x = padding_left + i * cell_size
            self.canvas.create_line(x, padding_top, x, padding_top + 3 * cell_size, width=4, fill="#523A1F")
            y = padding_top + i * cell_size
            self.canvas.create_line(padding_left, y, padding_left + 3 * cell_size, y, width=4, fill="#523A1F")

        self.status_text = self.canvas.create_text(270, 100, text="Player X's turn", fill="white",
                                                   font=("Arial Black", 24))

        self.x_img = ImageTk.PhotoImage(Image.open(os.path.join(ASSETS, "x.png")).resize((92, 92)))
        self.o_img = ImageTk.PhotoImage(Image.open(os.path.join(ASSETS, "o.png")).resize((92, 92)))

        self.canvas.bind("<Button-1>", self.handle_click)

        # Restart button
        restart_btn = tk.Button(self.root, text="Restart", font=("Arial", 16, "bold"),
                                command=lambda: self.start_game(vs_computer=self.vs_computer),
                                bg="#F4E2D8", fg="#4B2E1A", cursor="hand2")
        self.canvas.create_window(270, 800, window=restart_btn, width=120, height=40)

        # Play Again button image preload
        self.play_again_img = ImageTk.PhotoImage(
            Image.open(os.path.join(ASSETS, "playagain.png")).resize((200, 50))
        )
        self.play_again_button = None  # placeholder

    def handle_click(self, event):
        if self.game_over:
            return

        padding_top = 150
        padding_left = 120
        cell_size = 100

        x_click = event.x
        y_click = event.y

        col = (x_click - padding_left) // cell_size
        row = (y_click - padding_top) // cell_size

        if 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] is None:
            self.make_move(row, col, self.current_player)

            if self.check_winner(self.current_player):
                self.canvas.itemconfig(self.status_text, text=f"Player {self.current_player} wins!")
                self.game_over = True
                self.show_play_again()
                return
            elif self.check_draw():
                self.canvas.itemconfig(self.status_text, text="It's a Draw!")
                self.game_over = True
                self.show_play_again()
                return

            if self.vs_computer:
                self.current_player = "O"
                self.canvas.itemconfig(self.status_text, text="Computer's turn...")
                self.root.after(500, self.computer_move)
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.canvas.itemconfig(self.status_text, text=f"Player {self.current_player}'s turn")

    def make_move(self, row, col, player):
        self.board[row][col] = player
        x = 120 + col * 100 + 50
        y = 150 + row * 100 + 50
        img = self.x_img if player == "X" else self.o_img
        self.cells[row][col] = self.canvas.create_image(x, y, image=img)

    def computer_move(self):
        if self.game_over:
            return

        empty = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] is None]
        if not empty:
            return

        row, col = random.choice(empty)
        self.make_move(row, col, "O")

        if self.check_winner("O"):
            self.canvas.itemconfig(self.status_text, text="Computer wins!")
            self.game_over = True
            self.show_play_again()
        elif self.check_draw():
            self.canvas.itemconfig(self.status_text, text="It's a Draw!")
            self.game_over = True
            self.show_play_again()
        else:
            self.current_player = "X"
            self.canvas.itemconfig(self.status_text, text="Player X's turn")
    def show_play_again(self):
        # Defensive check: ensure image is loaded
        if not hasattr(self, 'play_again_img'):
            self.play_again_img = ImageTk.PhotoImage(
                Image.open(os.path.join(ASSETS, "playagain.png")).resize((200, 50))
            )

        # Remove old button if it exists
        if hasattr(self, 'play_again_button') and self.play_again_button:
            self.play_again_button.destroy()

        # Create and place new button (on top of canvas)
        self.play_again_button = tk.Button(self.root, image=self.play_again_img, bd=0, highlightthickness=0,
                                           command=lambda: self.start_game(vs_computer=self.vs_computer),
                                           bg="#8B5E3C", activebackground="#A46D2C", cursor="hand2")
        self.play_again_button.place(x=170, y=820)  # More reliable than create_window


    def check_winner(self, player):
        b = self.board
        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] == player or b[0][i] == b[1][i] == b[2][i] == player:
                return True
        if b[0][0] == b[1][1] == b[2][2] == player or b[0][2] == b[1][1] == b[2][0] == player:
            return True
        return False

    def check_draw(self):
        return all(cell is not None for row in self.board for cell in row)


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()
