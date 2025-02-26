import pygame
import random
import os

# 初始化Pygame
pygame.init()

# 颜色定义（皮卡丘主题色）
COLORS = [
    (255, 203, 5),    # 皮卡丘黄
    (235, 84, 30),    # 皮卡丘红腮
    (248, 160, 0),    # 橙色
    (255, 235, 59),   # 浅黄
    (244, 187, 68),   # 金黄
    (229, 164, 19),   # 深黄
    (255, 218, 68)    # 明黄
]

# 方块形状（皮卡丘元素）
SHAPES = [
    [[1, 1],      # 耳朵形状
     [1, 1]],     
    
    [[0, 1, 0],   # 尾巴形状
     [1, 1, 1]],  
    
    [[1, 1, 1],   # 脸形状
     [0, 1, 0]],  
    
    [[1, 0, 0],   # 闪电形状1
     [1, 1, 1]], 
    
    [[0, 0, 1],   # 闪电形状2
     [1, 1, 1]],
    
    [[1, 1, 0],   # 球形状1
     [0, 1, 1]],
    
    [[0, 1, 1],   # 球形状2
     [1, 1, 0]]
]

# 游戏设置
CELL_SIZE = 35  # 增大方块尺寸
COLS = 10
ROWS = 18  # 减少行数，使游戏区域更合适
SCREEN_WIDTH = COLS * CELL_SIZE + 250  # 增加右侧空间
SCREEN_HEIGHT = ROWS * CELL_SIZE + 40  # 增加一些底部空间

# 创建游戏窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('皮卡丘俄罗斯方块')

class PikachuTetris:
    def __init__(self):
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.score = 0
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.game_over = False
        self.clock = pygame.time.Clock()
        # 使用系统中文字体
        self.font = pygame.font.SysFont('SimHei', 36)  # 使用黑体
        
        # 加载皮卡丘图片
        try:
            self.pikachu_icon = pygame.image.load('pikachu.png')
            self.pikachu_icon = pygame.transform.scale(self.pikachu_icon, (30, 30))
        except:
            # 如果图片加载失败，创建一个黄色方块作为替代
            self.pikachu_icon = pygame.Surface((30, 30))
            self.pikachu_icon.fill(COLORS[0])  # 使用皮卡丘黄色
        self.pikachu_icon.fill(COLORS[0])  # 使用皮卡丘黄色

    def new_piece(self):
        shape_idx = random.randint(0, len(SHAPES) - 1)
        return {
            'shape': SHAPES[shape_idx],
            'color': COLORS[shape_idx],
            'x': COLS // 2 - len(SHAPES[shape_idx][0]) // 2,
            'y': 0
        }

    def draw(self):
        screen.fill((40, 44, 52))  # 深色背景
        
        # 绘制游戏区域背景
        pygame.draw.rect(screen, (30, 33, 39), (0, 0, COLS * CELL_SIZE, ROWS * CELL_SIZE))
        
        # 绘制已落下的方块
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell:
                    self.draw_block(x, y, cell)

        # 绘制当前方块
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    self.draw_block(self.current_piece['x'] + x, 
                                  self.current_piece['y'] + y, 
                                  self.current_piece['color'])

        # 绘制右侧信息区
        self.draw_side_panel()
        
        pygame.display.flip()

    def draw_block(self, x, y, color):
        # 绘制主方块
        pygame.draw.rect(screen, color,
                        (x * CELL_SIZE + 1, y * CELL_SIZE + 1,
                         CELL_SIZE - 2, CELL_SIZE - 2))
        # 只保留一个高光效果，使用纯白色
        pygame.draw.rect(screen, (255, 255, 255),
                        (x * CELL_SIZE + 1, y * CELL_SIZE + 1,
                         CELL_SIZE - 2, 3))
        # 添加高光效果
        pygame.draw.rect(screen, (255, 255, 255, 128),
                        (x * CELL_SIZE + 1, y * CELL_SIZE + 1,
                         CELL_SIZE - 2, 2))

    def draw_side_panel(self):
        # 绘制分数
        score_text = self.font.render('得分: ' + str(self.score), True, (255, 255, 255))
        screen.blit(score_text, (COLS * CELL_SIZE + 20, 20))

        # 绘制下一个方块预览
        preview_text = self.font.render('下一个:', True, (255, 255, 255))
        screen.blit(preview_text, (COLS * CELL_SIZE + 20, 80))
        
        # 绘制下一个方块
        for y, row in enumerate(self.next_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.next_piece['color'],
                                   ((COLS + 3 + x) * CELL_SIZE,
                                    (3 + y) * CELL_SIZE,
                                    CELL_SIZE - 2, CELL_SIZE - 2))

        # 游戏结束显示
        if self.game_over:
            game_over_text = self.font.render('游戏结束!', True, (255, 203, 5))
            restart_text = self.font.render('按 R 键重新开始', True, (255, 203, 5))
            screen.blit(game_over_text, (COLS * CELL_SIZE + 20, SCREEN_HEIGHT // 2))
            screen.blit(restart_text, (COLS * CELL_SIZE + 20, SCREEN_HEIGHT // 2 + 40))

    def collision(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    board_x = self.current_piece['x'] + x
                    board_y = self.current_piece['y'] + y
                    if (board_x < 0 or board_x >= COLS or
                        board_y >= ROWS or
                        (board_y >= 0 and self.board[board_y][board_x])):
                        return True
        return False

    def merge(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    self.board[self.current_piece['y'] + y][self.current_piece['x'] + x] = self.current_piece['color']

    def rotate(self):
        shape = self.current_piece['shape']
        new_shape = [[shape[y][x] for y in range(len(shape)-1, -1, -1)]
                    for x in range(len(shape[0]))]
        old_shape = self.current_piece['shape']
        self.current_piece['shape'] = new_shape
        if self.collision():
            self.current_piece['shape'] = old_shape

    def clear_lines(self):
        lines_cleared = 0
        y = ROWS - 1
        while y >= 0:
            if all(self.board[y]):
                lines_cleared += 1
                del self.board[y]
                self.board.insert(0, [0 for _ in range(COLS)])
            else:
                y -= 1
        self.score += lines_cleared * 100

    def reset_game(self):
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.score = 0
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.game_over = False
    def run(self):
        drop_time = 0
        running = True
        while running:
            self.clock.tick(60)
            drop_time += self.clock.get_rawtime()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.reset_game()
                        drop_time = 0
                        continue
                    if not self.game_over:  # 只在游戏未结束时响应其他按键
                        if event.key == pygame.K_LEFT:
                            self.current_piece['x'] -= 1
                            if self.collision():
                                self.current_piece['x'] += 1
                        elif event.key == pygame.K_RIGHT:  # 修复缩进
                            self.current_piece['x'] += 1
                            if self.collision():
                                self.current_piece['x'] -= 1
                        elif event.key == pygame.K_DOWN:
                            self.current_piece['y'] += 1
                            if self.collision():
                                self.current_piece['y'] -= 1
                                self.merge()
                                self.clear_lines()
                                self.current_piece = self.next_piece
                                self.next_piece = self.new_piece()
                                if self.collision():
                                    self.game_over = True
                        elif event.key == pygame.K_UP:
                            self.rotate()
                        elif event.key == pygame.K_SPACE:  # 快速下落
                            while not self.collision():
                                self.current_piece['y'] += 1
                            self.current_piece['y'] -= 1
                            self.merge()
                            self.clear_lines()
                            self.current_piece = self.next_piece
                            self.next_piece = self.new_piece()
                            if self.collision():
                                self.game_over = True
                    elif event.key == pygame.K_r and self.game_over:  # 添加重新开始功能
                        self.reset_game()
                        drop_time = 0
                        continue

            if drop_time > 600:  # 降低下落速度，从500改为600
                self.current_piece['y'] += 1
                if self.collision():
                    self.current_piece['y'] -= 1
                    self.merge()
                    self.clear_lines()
                    self.current_piece = self.next_piece
                    self.next_piece = self.new_piece()
                    if self.collision():
                        self.game_over = True
                drop_time = 0

            self.draw()  # 无论游戏是否结束都继续绘制
if __name__ == '__main__':
    game = PikachuTetris()
    game.run()
    pygame.quit()