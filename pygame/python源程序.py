import pygame as pg
import numpy as np
import random
import copy
import sys
from pathlib import Path

# ====================== 全局常量 ======================
INSTR_WIDTH, INSTR_HEIGHT = 440, 600
GAME_WIDTH, GAME_HEIGHT = 1440, 800

# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# 游戏地图相关常量
obstacle_length = 25
x_begin = 63
y_begin = 65
block_step = obstacle_length + 2
map_rows = 25
map_cols = 49

# 操作说明文本
instructions = [
    "【移动操作】",
    "← 左方向键：企鹅向左移动",
    "→ 右方向键：企鹅向右移动",
    "↑ 上方向键：企鹅向上移动",
    "↓ 下方向键：企鹅向下移动",
    "",
    "【游戏目标】",
    "控制企鹅收集金币",
    "避开障碍物",
    "请收集尽可能多的金币",
    "",
    "【重置游戏】",
    "R键:重置游戏地图与位置",
    "【控制音乐】",
    "M键:控制音乐播放"
]

# 按钮区域（说明页）
back_btn_rect = pg.Rect(150, 520, 140, 40)

# 全局变量（在 init_resources 中初始化）
font_title = None
font_content = None
font_btn = None
score_font = None

background_music = None
win_music = None

obstacle = None
penguin = None
rose520 = None
coin_images = []
big_penguin_front = None
big_penguin_back = None

original_treasure_map = None

# ====================== 辅助函数与类定义 ======================

def load_image(path, size=None):
    try:
        current_dir = Path(__file__).parent
        img_path = current_dir / path
        img = pg.image.load(str(img_path)).convert_alpha()
        if size:
            img = pg.transform.scale(img, size)
        return img
    except (FileNotFoundError, pg.error):
        print(f"警告：图片 {path} 缺失，将使用占位")
        surf = pg.Surface(size or (obstacle_length, obstacle_length))
        surf.fill(RED)
        return surf

def generate_map():
    """生成迷宫地图并返回"""
    map_of_treasure = np.ones((map_rows, map_cols), int)
    recorder = np.zeros((int((map_rows - 1) / 2), int((map_cols - 1) / 2)), int)
    random_move = [[1, 0], [0, 1], [0, -1], [-1, 0]]
    
    for i in range(int((map_rows - 1) / 2)):
        for j in range(int((map_cols - 1) / 2)):
            map_of_treasure[2 * i + 1][2 * j + 1] = 0
    recorder[0][0] = 1

    # 使用显式栈代替递归，防止递归过深爆栈
    stack = [(0, 0)]
    while stack:
        x, y = stack[-1]
        flag = 0
        r = random.randint(1, 4)
        for i in range(4):
            xx = x + random_move[(r + i) % 4][0]
            yy = y + random_move[(r + i) % 4][1]
            if 0 <= xx < (map_rows - 1) / 2 and 0 <= yy < (map_cols - 1) / 2:
                if recorder[xx][yy] == 0:
                    flag = 1
                    recorder[xx][yy] = 1
                    map_of_treasure[x * 2 + 1 + xx][y * 2 + 1 + yy] = 0
                    stack.append((xx, yy))
                    break
        if flag == 0:
            map_of_treasure[2 * x + 1][2 * y + 1] = 2  # 金币
            stack.pop()

    map_of_treasure[map_rows - 2][map_cols - 2] = 3  # 终点玫瑰
    return map_of_treasure

def init_resources():
    """初始化 pygame 和各项资源"""
    global font_title, font_content, font_btn, score_font
    global background_music, win_music
    global obstacle, penguin, rose520, coin_images, big_penguin_front, big_penguin_back
    global original_treasure_map

    pg.init()
    pg.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

    font_title = pg.font.SysFont("SimHei", 30, bold=True)
    font_content = pg.font.SysFont("SimHei", 20)
    font_btn = pg.font.SysFont("SimHei", 24)
    score_font = pg.font.SysFont("Arial", 20, bold=True)

    current_dir = Path(__file__).parent
    try:
        background_music = pg.mixer.Sound(str(current_dir / "Funky Town.mp3"))
        win_music = pg.mixer.Sound(str(current_dir / "Wang Fei.mp3"))
        background_music.set_volume(0.3)
        win_music.set_volume(0.5)
    except (FileNotFoundError, pg.error):
        print("警告：音乐文件缺失，游戏将继续运行（无背景音乐）")
        background_music = None
        win_music = None

    obstacle = load_image("obstacle.jpg", (obstacle_length, obstacle_length))
    penguin = load_image("penguin_0.png", (obstacle_length, obstacle_length))
    rose520 = load_image("rose520.png", (obstacle_length - 4, obstacle_length - 4))

    coin_images = [
        load_image("coin_front.png", (obstacle_length - 6, obstacle_length - 6)),
        load_image("coin_right_skew.png", (obstacle_length - 6, obstacle_length - 6)),
        load_image("coin_right_side.png", (obstacle_length - 6, obstacle_length - 6)),
        load_image("coin_back.png", (obstacle_length - 6, obstacle_length - 6)),
        load_image("coin_left_side.png", (obstacle_length - 6, obstacle_length - 6)),
        load_image("coin_left_skew.png", (obstacle_length - 6, obstacle_length - 6)),
    ]

    big_penguin_front = load_image("penguin_2_front.png")
    big_penguin_back = load_image("penguin_2_back.png")

    original_treasure_map = generate_map()

def draw_instructions(screen):
    """绘制说明界面"""
    screen.fill(WHITE)
    title_text = font_title.render("寻宝游戏操作说明", True, BLUE)
    screen.blit(title_text, (INSTR_WIDTH // 2 - title_text.get_width() // 2, 30))
    pg.draw.line(screen, GRAY, (50, 80), (390, 80), 2)

    y_offset = 100
    for line in instructions:
        text = font_content.render(line, True, BLACK)
        screen.blit(text, (60, y_offset))
        y_offset += 30

    pg.draw.rect(screen, GRAY, back_btn_rect, border_radius=5)
    pg.draw.rect(screen, BLACK, back_btn_rect, 2, border_radius=5)
    btn_text = font_btn.render("返回游戏", True, RED)
    screen.blit(btn_text, (back_btn_rect.x + 20, back_btn_rect.y + 5))

def draw_rotating_coin(screen, map_i, map_j, coin_rotate_angles):
    """单独绘制金币动效"""
    screen_x = x_begin + map_j * block_step + 3
    screen_y = y_begin + map_i * block_step + 3
    current_angle = coin_rotate_angles.get((map_i, map_j), 0)
    coin_rotate_angles[(map_i, map_j)] = (current_angle + 2) % 360

    angle = current_angle % 360
    if angle >= 315 or angle < 45:
        img = coin_images[0]
    elif angle < 90:
        img = coin_images[1]
    elif angle < 135:
        img = coin_images[2]
    elif angle < 225:
        img = coin_images[3]
    elif angle < 270:
        img = coin_images[4]
    else:
        img = coin_images[5]
    screen.blit(img, (screen_x, screen_y))

# ====================== 主程序入口 ======================
def main():
    # 1. 结构整理：在主入口前才进行一次初始化
    init_resources()
    
    screen = pg.display.set_mode((INSTR_WIDTH, INSTR_HEIGHT))
    pg.display.set_caption("游戏操作说明")
    state = "INSTRUCTIONS"

    # 游戏状态变量
    penguin_row = 1
    penguin_col = 1
    score = 0
    map_of_treasure = copy.deepcopy(original_treasure_map)
    game_over = False
    background_playing = False
    win_music_playing = False
    
    coin_rotate_angles = {}
    for i in range(map_rows):
        for j in range(map_cols):
            if map_of_treasure[i][j] == 2:
                coin_rotate_angles[(i, j)] = random.randint(0, 359)

    def reset_game():
        nonlocal penguin_row, penguin_col, score, map_of_treasure, game_over, win_music_playing, coin_rotate_angles
        penguin_row = 1
        penguin_col = 1
        score = 0
        map_of_treasure = copy.deepcopy(original_treasure_map)
        game_over = False
        win_music_playing = False
        coin_rotate_angles.clear()
        for i in range(map_rows):
            for j in range(map_cols):
                if map_of_treasure[i][j] == 2:
                    coin_rotate_angles[(i, j)] = random.randint(0, 359)

    score_text = score_font.render(f"score  {score}", True, WHITE)
    penguin_move_x = penguin_move_y = 0
    move_speed = 6

    # 游戏结束动画状态
    base_height = 400
    current_width = 400
    is_switching = False
    switch_timer = 0
    switch_interval = 1000
    penguin_state = "front"
    big_penguin_x = GAME_WIDTH // 2 - current_width // 2
    big_penguin_y = GAME_HEIGHT // 2 - base_height // 2
    big_penguin_pos = (big_penguin_x, big_penguin_y)

    clock = pg.time.Clock()
    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            # 分发不同状态下的事件
            if state == "INSTRUCTIONS":
                if event.type == pg.MOUSEBUTTONDOWN:
                    if back_btn_rect.collidepoint(event.pos):
                        # 状态机转场：避免多次 pg.init 
                        screen = pg.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
                        pg.display.set_caption("迷宫寻宝")
                        if background_music:
                            background_music.play(-1)
                            background_playing = True
                        state = "PLAYING"

            elif state in ("PLAYING", "GAME_OVER") and penguin_move_x == 0 and penguin_move_y == 0:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT and map_of_treasure[penguin_row][penguin_col - 1] != 1:
                        penguin_move_y = -block_step
                        penguin_col -= 1
                    elif event.key == pg.K_RIGHT and map_of_treasure[penguin_row][penguin_col + 1] != 1:
                        penguin_move_y = block_step
                        penguin_col += 1
                    elif event.key == pg.K_UP and map_of_treasure[penguin_row - 1][penguin_col] != 1:
                        penguin_move_x = -block_step
                        penguin_row -= 1
                    elif event.key == pg.K_DOWN and map_of_treasure[penguin_row + 1][penguin_col] != 1:
                        penguin_move_x = block_step
                        penguin_row += 1
                    elif event.key == pg.K_r:
                        reset_game()
                        score_text = score_font.render(f"score  {score}", True, WHITE)
                    elif event.key == pg.K_m and background_music:
                        if background_playing:
                            background_music.stop()
                        else:
                            background_music.play(-1)
                        background_playing = not background_playing

        if state == "PLAYING":
            if penguin_move_x < 0: penguin_move_x = min(0, penguin_move_x + move_speed)
            if penguin_move_x > 0: penguin_move_x = max(0, penguin_move_x - move_speed)
            if penguin_move_y < 0: penguin_move_y = min(0, penguin_move_y + move_speed)
            if penguin_move_y > 0: penguin_move_y = max(0, penguin_move_y - move_speed)

            # 到达终点
            if map_of_treasure[penguin_row][penguin_col] == 3:
                state = "GAME_OVER"
                game_over = True
                if background_music:
                    background_music.stop()
                    background_playing = False
                if win_music and not win_music_playing:
                    win_music.play()
                    win_music_playing = True

            # 吃到金币
            if map_of_treasure[penguin_row][penguin_col] == 2:
                score += 1
                map_of_treasure[penguin_row][penguin_col] = 0
                score_text = score_font.render(f"score  {score}", True, WHITE)
                if (penguin_row, penguin_col) in coin_rotate_angles:
                    del coin_rotate_angles[(penguin_row, penguin_col)]

        if state == "INSTRUCTIONS":
            draw_instructions(screen)
        else:
            screen.fill(YELLOW)
            pg.draw.rect(screen, BLACK, (50, 0, GAME_WIDTH, 25))
            screen.blit(score_text, (70, 0))

            for i in range(map_rows):
                for j in range(map_cols):
                    if map_of_treasure[i][j] == 0:
                        continue
                    if map_of_treasure[i][j] == 2:
                        draw_rotating_coin(screen, i, j, coin_rotate_angles)
                        continue
                    if map_of_treasure[i][j] == 3:
                        sx = x_begin + j * block_step + 2
                        sy = y_begin + i * block_step + 2
                        screen.blit(rose520, (sx, sy))
                        continue
                    screen.blit(obstacle, (x_begin + j * block_step, y_begin + i * block_step))

            screen.blit(penguin, (x_begin + penguin_col * block_step - penguin_move_y,
                                  y_begin + penguin_row * block_step - penguin_move_x))

            if state == "GAME_OVER":
                switch_timer += clock.get_time()
                if switch_timer >= switch_interval and not is_switching:
                    is_switching = True
                    switch_timer = 0
                    current_width = 80

                if is_switching:
                    if current_width > 80:
                        current_width -= 2
                    else:
                        penguin_state = "back" if penguin_state == "front" else "front"
                        current_width = 400
                        is_switching = False

                big_penguin_x = GAME_WIDTH // 2 - current_width // 2
                big_penguin_pos = (big_penguin_x, big_penguin_y)
                current_penguin = big_penguin_front if penguin_state == "front" else big_penguin_back
                scaled = pg.transform.smoothscale(current_penguin, (current_width, base_height))
                screen.blit(scaled, big_penguin_pos)

                end_font = pg.font.SysFont("SimHei", 40, bold=True)
                txt1 = end_font.render("明月几时有，把酒问青天", True, RED)
                txt2 = end_font.render(f"最终得分：{score} | 按 R 键重置", True, BLUE)
                screen.blit(txt1, (GAME_WIDTH // 2 - txt1.get_width() // 2, GAME_HEIGHT // 2 - 250))
                screen.blit(txt2, (GAME_WIDTH // 2 - txt2.get_width() // 2, GAME_HEIGHT // 2 + 220))

        pg.display.flip()
        clock.tick(60)

    pg.mixer.stop()
    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()