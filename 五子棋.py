import tkinter as tk
from tkinter import messagebox

# 定義棋盤大小
GRID_SIZE = 15
CELL_SIZE = 40
turn = 1  # 1 為黑子，2 為白子

# 初始化棋盤
board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# 判斷是否有玩家獲勝
def check_winner():
    # 檢查橫向、縱向、斜向
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if board[x][y] != 0:
                # 橫向檢查
                if y + 4 < GRID_SIZE and all(board[x][y + i] == board[x][y] for i in range(5)):
                    return board[x][y]
                # 縱向檢查
                if x + 4 < GRID_SIZE and all(board[x + i][y] == board[x][y] for i in range(5)):
                    return board[x][y]
                # 右下斜向檢查
                if x + 4 < GRID_SIZE and y + 4 < GRID_SIZE and all(board[x + i][y + i] == board[x][y] for i in range(5)):
                    return board[x][y]
                # 右上斜向檢查
                if x - 4 >= 0 and y + 4 < GRID_SIZE and all(board[x - i][y + i] == board[x][y] for i in range(5)):
                    return board[x][y]
    return 0  # 沒有獲勝者

# 繪製棋盤和棋子
def draw_board():
    canvas.delete("all")
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            canvas.create_rectangle(y * CELL_SIZE, x * CELL_SIZE,
                                    (y + 1) * CELL_SIZE, (x + 1) * CELL_SIZE,
                                    outline="black", width=1)

            if board[x][y] == 1:
                canvas.create_oval(y * CELL_SIZE + 5, x * CELL_SIZE + 5,
                                   (y + 1) * CELL_SIZE - 5, (x + 1) * CELL_SIZE - 5,
                                   fill="black")
            elif board[x][y] == 2:
                canvas.create_oval(y * CELL_SIZE + 5, x * CELL_SIZE + 5,
                                   (y + 1) * CELL_SIZE - 5, (x + 1) * CELL_SIZE - 5,
                                   fill="white")

# 處理玩家點擊的事件
def on_click(event):
    global turn
    x, y = event.y // CELL_SIZE, event.x // CELL_SIZE

    if board[x][y] == 0:  # 如果該位置空著
        board[x][y] = turn
        turn = 3 - turn  # 換玩家，1 變 2，2 變 1
        draw_board()

        winner = check_winner()
        if winner != 0:
            winner_color = "黑子" if winner == 1 else "白子"
            messagebox.showinfo("遊戲結束", f"{winner_color} 獲勝！")
            reset_game()

# 重設遊戲
def reset_game():
    global board, turn
    board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    turn = 1  # 從黑子開始
    draw_board()

# 設定視窗
root = tk.Tk()
root.title("五子棋")

# 創建畫布
canvas = tk.Canvas(root, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE, bg="#f0e4d7")
canvas.pack()

# 綁定點擊事件
canvas.bind("<Button-1>", on_click)

# 初始化棋盤畫面
draw_board()

# 添加重設遊戲按鈕
reset_button = tk.Button(root, text="重新開始", command=reset_game)
reset_button.pack(pady=10)

# 運行主循環
root.mainloop()
