import tkinter as tk
import random
from time import time

def generate_sudoku():
    sudoku = [[0] * 9 for _ in range(9)]
    for _ in range(random.randint(12, 24)):
        row, col, num = random.randint(0, 8), random.randint(0, 8), random.randint(1, 9)
        while not is_valid_move(sudoku, row, col, num):
            row, col, num = random.randint(0, 8), random.randint(0, 8), random.randint(1, 9)
        sudoku[row][col] = num
    return sudoku

def is_valid_move(board, row, col, num):
    if num in board[row]:
        return False
    if num in [board[i][col] for i in range(9)]:
        return False
    box_row, box_col = row // 3 * 3, col // 3 * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False
    return True

def draw_sudoku(board):
    for row in range(9):
        for col in range(9):
            value = board[row][col]
            cell = tk.Entry(root, width=3, font=("Helvetica", 16), justify="center")
            cell.grid(row=row, column=col)
            if value != 0:
                cell.insert(0, str(value))

def check_solution(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return False
            if not is_valid_move(board, row, col, board[row][col]):
                return False
    return True

def is_board_full(board):
    for row in board:
        if 0 in row:
            return False
    return True

def on_cell_click(row, col):
    current_row = current_board[row]
    current_cell = current_row[col]

    def submit_answer():
        value = int(current_cell.get())
        if is_valid_move(current_board, row, col, value):
            current_board[row][col] = value
            if is_board_full(current_board):
                if check_solution(current_board):
                    result.config(text="ถูกต้อง")
                else:
                    result.config(text="ไม่ถูกต้อง")

    current_cell.submit_button.config(command=submit_answer)
    current_cell.submit_button.grid(row=row, column=col)

def start_new_game():
    global current_board, start_time, end_time
    current_board = generate_sudoku()
    draw_sudoku(current_board)
    result.config(text="")
    start_time = time()
    end_time = start_time + countdown_time
    reset_timer()

def reset_timer():
    current_time = time()
    remaining_time = max(0, end_time - current_time)
    minutes, seconds = divmod(int(remaining_time), 60)
    time_label.config(text=f"เวลา: {minutes:02d}:{seconds:02d}")
    if remaining_time > 0:
        time_label.after(1000, reset_timer)
    else:
        result.config(text="หมดเวลา")

def check_board():
    if check_solution(current_board):
        result.config(text="ถูกต้อง")
    else:
        result.config(text="ไม่ถูกต้อง")

root = tk.Tk()
root.title("Sudoku")

current_board = generate_sudoku()
draw_sudoku(current_board)

new_game_button = tk.Button(root, text="เริ่มใหม่", command=start_new_game)
new_game_button.grid(row=10, column=0, columnspan=9, pady=(5, 10))

result = tk.Label(root, text="", font=("Helvetica", 16))
result.grid(row=11, columnspan=9)

start_time = time()
countdown_time = 600
end_time = start_time + countdown_time

time_label = tk.Label(root, text="", font=("Helvetica", 16))
time_label.grid(row=12, columnspan=9)

check_button = tk.Button(root, text="ตรวจสอบ", command=check_board)
check_button.grid(row=13, column=0, columnspan=9, pady=(10, 5))

root.mainloop()
