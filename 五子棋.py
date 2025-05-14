
import tkinter as tk
from tkinter import messagebox

BOARD_SIZE = 15
CELL_SIZE = 40
STONE_RADIUS = 16

HUMAN = 1
AI = 2

SCORES = {5: 100000, 4: 10000, 3: 1000, 2: 100, 1: 10}

class GomokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("五子棋 AI（攻防平衡版）")
        self.canvas = tk.Canvas(root, width=BOARD_SIZE * CELL_SIZE, height=BOARD_SIZE * CELL_SIZE, bg="burlywood")
        self.canvas.pack()
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.current_player = HUMAN
        self.ai_enabled = tk.BooleanVar(value=True)

        ctrl_frame = tk.Frame(root)
        ctrl_frame.pack()
        tk.Button(ctrl_frame, text="重新開始", command=self.restart_game).pack(side=tk.LEFT, padx=5)
        tk.Checkbutton(ctrl_frame, text="AI 模式", variable=self.ai_enabled).pack(side=tk.LEFT)

        self.canvas.bind("<Button-1>", self.handle_click)
        self.draw_board()

    def draw_board(self):
        for i in range(BOARD_SIZE):
            self.canvas.create_line(CELL_SIZE//2, CELL_SIZE//2 + i*CELL_SIZE,
                                    CELL_SIZE//2 + (BOARD_SIZE-1)*CELL_SIZE, CELL_SIZE//2 + i*CELL_SIZE)
            self.canvas.create_line(CELL_SIZE//2 + i*CELL_SIZE, CELL_SIZE//2,
                                    CELL_SIZE//2 + i*CELL_SIZE, CELL_SIZE//2 + (BOARD_SIZE-1)*CELL_SIZE)

    def handle_click(self, event):
        col = round((event.x - CELL_SIZE//2) / CELL_SIZE)
        row = round((event.y - CELL_SIZE//2) / CELL_SIZE)
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.board[row][col] == 0:
            self.make_move(row, col, self.current_player)
            if self.check_win(row, col):
                winner = "玩家（黑棋）" if self.current_player == HUMAN else "玩家（白棋）"
                self.end_game(f"{winner} 勝利！")
                return
            if self.ai_enabled.get():
                if self.current_player == HUMAN:
                    self.current_player = AI
                    self.root.after(300, self.ai_move)
            else:
                self.current_player = HUMAN if self.current_player == AI else AI

    def make_move(self, row, col, player):
        self.board[row][col] = player
        self.draw_stone(row, col, player)

    def ai_move(self):
        row, col = self.find_best_move()
        self.make_move(row, col, AI)
        if self.check_win(row, col):
            self.end_game("AI（白棋）勝利！")
            return
        self.current_player = HUMAN

    def draw_stone(self, row, col, player):
        x = CELL_SIZE // 2 + col * CELL_SIZE
        y = CELL_SIZE // 2 + row * CELL_SIZE
        color = "black" if player == HUMAN else "white"
        self.canvas.create_oval(x - STONE_RADIUS, y - STONE_RADIUS,
                                x + STONE_RADIUS, y + STONE_RADIUS,
                                fill=color)

    def find_best_move(self):
        best_score = -1
        best_move = (BOARD_SIZE // 2, BOARD_SIZE // 2)
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] == 0:
                    offense_score = self.evaluate(r, c, AI)
                    defense_score = self.evaluate(r, c, HUMAN) * 1.1
                    total_score = offense_score + defense_score
                    if total_score > best_score:
                        best_score = total_score
                        best_move = (r, c)
        return best_move

    def evaluate(self, row, col, player):
        total = 0
        directions = [(1,0), (0,1), (1,1), (1,-1)]
        for dr, dc in directions:
            count = 1
            for d in [1, -1]:
                for i in range(1, 5):
                    r, c = row + dr*i*d, col + dc*i*d
                    if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                        if self.board[r][c] == player:
                            count += 1
                        elif self.board[r][c] != 0:
                            break
                    else:
                        break
            total += SCORES.get(count, 0)
        return total

    def check_win(self, row, col):
        def count(dx, dy):
            cnt = 1
            for d in [1, -1]:
                r, c = row + dy*d, col + dx*d
                while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == self.board[row][col]:
                    cnt += 1
                    r += dy*d
                    c += dx*d
            return cnt
        for dx, dy in [(1,0), (0,1), (1,1), (1,-1)]:
            if count(dx, dy) >= 5:
                return True
        return False

    def end_game(self, message):
        messagebox.showinfo("遊戲結束", message)
        self.canvas.unbind("<Button-1>")

    def restart_game(self):
        self.canvas.delete("all")
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.current_player = HUMAN
        self.draw_board()
        self.canvas.bind("<Button-1>", self.handle_click)

if __name__ == "__main__":
    root = tk.Tk()
    game = GomokuGame(root)
    root.mainloop()
