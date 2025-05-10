import sys
import random
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QApplication, QWidget
#
# 設置窗口大小和顏色
WIDTH = 600
HEIGHT = 400
SNAKE_SIZE = 20
SNAKE_SPEED = 100  # 控制蛇的速度（毫秒）

# 顏色設置
WHITE = QColor(255, 255, 255)
GREEN = QColor(0, 255, 0)
RED = QColor(255, 0, 0)
BLACK = QColor(0, 0, 0)

class SnakeGame(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Snake Game")
        self.setGeometry(100, 100, WIDTH, HEIGHT)
        self.setStyleSheet("background-color: black;")

        self.snake = [(100, 100), (80, 100), (60, 100)]  # 蛇的位置（初始3塊）
        self.snake_direction = "Right"
        self.food = None
        self.score = 0
        self.game_over = False

        # 設置計時器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        self.timer.start(SNAKE_SPEED)

        self.spawn_food()

    def keyPressEvent(self, event):
        """控制蛇的方向"""
        if self.game_over:
            return
        
        if event.key() == Qt.Key_Left and self.snake_direction != "Right":
            self.snake_direction = "Left"
        elif event.key() == Qt.Key_Right and self.snake_direction != "Left":
            self.snake_direction = "Right"
        elif event.key() == Qt.Key_Up and self.snake_direction != "Down":
            self.snake_direction = "Up"
        elif event.key() == Qt.Key_Down and self.snake_direction != "Up":
            self.snake_direction = "Down"

    def spawn_food(self):
        """生成隨機食物位置"""
        food_x = random.randint(0, (WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        food_y = random.randint(0, (HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        self.food = (food_x, food_y)

    def update_game(self):
        """遊戲邏輯更新"""
        if self.game_over:
            return

        # 蛇移動
        head_x, head_y = self.snake[0]
        if self.snake_direction == "Left":
            head_x -= SNAKE_SIZE
        elif self.snake_direction == "Right":
            head_x += SNAKE_SIZE
        elif self.snake_direction == "Up":
            head_y -= SNAKE_SIZE
        elif self.snake_direction == "Down":
            head_y += SNAKE_SIZE

        # 檢查是否撞牆或咬到自己
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT or (head_x, head_y) in self.snake:
            self.game_over = True
            self.update()
            return

        # 在蛇頭插入新位置
        self.snake = [(head_x, head_y)] + self.snake[:-1]

        # 檢查是否吃到食物
        if (head_x, head_y) == self.food:
            self.score += 1
            self.snake.append(self.snake[-1])  # 增加蛇身
            self.spawn_food()

        self.update()

    def paintEvent(self, event):
        """繪製畫面"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.draw_snake(painter)
        self.draw_food(painter)
        self.draw_score(painter)

    def draw_snake(self, painter):
        """繪製蛇"""
        painter.setBrush(GREEN)
        for x, y in self.snake:
            painter.drawRect(x, y, SNAKE_SIZE, SNAKE_SIZE)

    def draw_food(self, painter):
        """繪製食物"""
        food_x, food_y = self.food
        painter.setBrush(RED)
        painter.drawRect(food_x, food_y, SNAKE_SIZE, SNAKE_SIZE)

    def draw_score(self, painter):
        """顯示分數"""
        painter.setPen(WHITE)
        painter.drawText(10, 20, f"Score: {self.score}")

def main():
    app = QApplication(sys.argv)
    game = SnakeGame()
    game.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
