import tkinter as tk
import random

# 畫面大小與設定
WIDTH, HEIGHT = 400, 600
GRAVITY = 2
PLAYER_SPEED = 5
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 10
PLAYER_SIZE = 40
MIN_PLATFORM_GAP = 100

class Game:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='white')
        self.canvas.pack()
        self.root.title("小朋友下樓梯")
        self.keys = set()
        self.root.bind("<KeyPress>", self.key_down)
        self.root.bind("<KeyRelease>", self.key_up)
        self.restart_game()

    def restart_game(self):
        self.canvas.delete("all")
        self.platforms = []
        self.spikes = []
        self.health = 100
        self.score = 0
        self.player_vy = 0
        self.running = True

        # 用矩形作為玩家
        self.player = self.canvas.create_rectangle(WIDTH//2, 200, WIDTH//2 + PLAYER_SIZE, 200 + PLAYER_SIZE, fill="blue")

        for i in range(6):
            self.spawn_platform(random.randint(0, WIDTH - PLATFORM_WIDTH), HEIGHT - i * 120)

        self.update()

    def key_down(self, event):
        self.keys.add(event.keysym.lower())
        if event.keysym.lower() == "r" and not self.running:
            self.restart_game()

    def key_up(self, event):
        self.keys.discard(event.keysym.lower())

    def spawn_platform(self, x, y):
        platform = self.canvas.create_rectangle(x, y, x + PLATFORM_WIDTH, y + PLATFORM_HEIGHT, fill="green")
        self.platforms.append(platform)
        if random.random() < 0.3:
            self.spawn_spike(x + random.randint(0, PLATFORM_WIDTH - 30), y - 10)

    def spawn_spike(self, x, y):
        spike = self.canvas.create_polygon(x, y + 10, x + 15, y, x + 30, y + 10, fill="red")
        self.spikes.append(spike)

    def move_player(self):
        dx = 0
        if "a" in self.keys:
            dx = -PLAYER_SPEED
        if "d" in self.keys:
            dx = PLAYER_SPEED
        self.canvas.move(self.player, dx, 0)
        self.player_vy += GRAVITY
        self.canvas.move(self.player, 0, self.player_vy)

    def check_platform_collision(self):
        px1, py1, px2, py2 = self.canvas.coords(self.player)
        for platform in self.platforms:
            x1, y1, x2, y2 = self.canvas.coords(platform)
            if py2 >= y1 - 5 and py2 <= y1 + 10 and px2 > x1 and px1 < x2 and self.player_vy >= 0:
                self.canvas.coords(self.player, px1, y1 - PLAYER_SIZE, px2, y1)
                self.player_vy = 0
                break

    def check_spike_collision(self):
        px1, py1, px2, py2 = self.canvas.coords(self.player)
        for spike in self.spikes:
            if self.canvas.bbox(spike):
                x1, y1, x2, y2 = self.canvas.bbox(spike)
                if px2 > x1 and px1 < x2 and py2 > y1 and py1 < y2:
                    self.health -= 1
                    break

    def scroll_world(self):
        for item in self.platforms + self.spikes:
            self.canvas.move(item, 0, -2)
        self.platforms = [p for p in self.platforms if self.canvas.coords(p)[1] < HEIGHT + 50]
        self.spikes = [s for s in self.spikes if self.canvas.coords(s)[1] < HEIGHT + 50]

        last_y = max([self.canvas.coords(p)[1] for p in self.platforms]) if self.platforms else HEIGHT
        if HEIGHT - last_y > MIN_PLATFORM_GAP:
            self.spawn_platform(random.randint(0, WIDTH - PLATFORM_WIDTH), HEIGHT)

    def draw_hud(self):
        self.canvas.delete("hud")
        self.canvas.create_text(10, 10, anchor="nw", text=f"Score: {self.score}", tag="hud")
        self.canvas.create_text(10, 30, anchor="nw", text=f"Health: {self.health}", tag="hud")

    def update(self):
        if not self.running:
            return

        self.move_player()
        self.check_platform_collision()
        self.check_spike_collision()
        self.scroll_world()
        self.draw_hud()
        self.score += 1

        _, y1, _, y2 = self.canvas.coords(self.player)

        # 加入上下死亡判定
        if self.health <= 0 or y2 > HEIGHT or y1 < 0:
            self.running = False
            self.canvas.create_text(WIDTH//2, HEIGHT//2, text="Game Over\n按 R 鍵重新開始", font=("Arial", 20), fill="black")
            return

        self.root.after(30, self.update)

# 啟動遊戲
root = tk.Tk()
game = Game(root)
root.mainloop()