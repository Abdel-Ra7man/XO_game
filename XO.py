import tkinter as tk
from tkinter import messagebox
import math

# Initialize the window
root = tk.Tk()
root.title("Tic-Tac-Toe")

# Global variables
current_player = "X"  # Player always starts first
game_mode = None  # Will be set to "1v1" or "1vCPU"
buttons = []
board = [[" " for _ in range(3)] for _ in range(3)]

# Function to check for a winner
def check_winner(player):
    for row in board:
        if row.count(player) == 3:
            return True
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True
    if board[0][0] == board[1][1] == board[2][2] == player or board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

# Function to check for a tie
def is_full():
    return all(cell != " " for row in board for cell in row)

# Minimax algorithm for AI
def minimax(board, depth, is_maximizing):
    if check_winner("O"):
        return 1  # Computer wins
    if check_winner("X"):
        return -1  # Player wins
    if is_full():
        return 0  # Tie

    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    score = minimax(board, depth + 1, False)
                    board[i][j] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    score = minimax(board, depth + 1, True)
                    board[i][j] = " "
                    best_score = min(score, best_score)
        return best_score

# AI move using Minimax
def computer_move():
    best_score = -math.inf
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                score = minimax(board, 0, False)
                board[i][j] = " "
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    
    if best_move:
        board[best_move[0]][best_move[1]] = "O"
        buttons[best_move[0]][best_move[1]].config(text="O", state=tk.DISABLED)

        if check_winner("O"):
            messagebox.showinfo("Tic-Tac-Toe", "Computer wins!")
            root.quit()
        elif is_full():
            messagebox.showinfo("Tic-Tac-Toe", "It's a tie!")
            root.quit()

# Handle player move
def player_move(row, col):
    global current_player
    if board[row][col] == " ":
        board[row][col] = current_player
        buttons[row][col].config(text=current_player, state=tk.DISABLED)

        # Check for win or tie
        if check_winner(current_player):
            messagebox.showinfo("Tic-Tac-Toe", f"Player {current_player} wins!")
            root.quit()
        elif is_full():
            messagebox.showinfo("Tic-Tac-Toe", "It's a tie!")
            root.quit()
        else:
            # Switch turns
            if game_mode == "1v1":
                current_player = "O" if current_player == "X" else "X"
            elif game_mode == "1vCPU":
                current_player = "O"
                computer_move()
                current_player = "X"

# Function to set game mode
def set_game_mode(mode):
    global game_mode
    game_mode = mode
    mode_selection.destroy()  # Close the mode selection window

# Create a pop-up window to choose game mode
mode_selection = tk.Toplevel(root)
mode_selection.title("Choose Game Mode")
tk.Label(mode_selection, text="Select Game Mode:", font=("Arial", 14)).pack(pady=10)
tk.Button(mode_selection, text="1v1 (Two Players)", font=("Arial", 12), command=lambda: set_game_mode("1v1")).pack(pady=5)
tk.Button(mode_selection, text="1vCPU (Play vs AI)", font=("Arial", 12), command=lambda: set_game_mode("1vCPU")).pack(pady=5)
mode_selection.grab_set()  # Make this window modal (blocks interaction with main window)

# Create the GUI grid of buttons
for i in range(3):
    row = []
    for j in range(3):
        button = tk.Button(root, text="", font=('normal', 40), width=5, height=2,
                           command=lambda i=i, j=j: player_move(i, j))
        button.grid(row=i, column=j)
        row.append(button)
    buttons.append(row)

# Start the Tkinter loop
root.mainloop()
