import pygame as pg
import numpy as np
import random
import copy
import sys
# 初始化pg
pg.init()
#初始化音频混音器
pg.mixer.init(frequency=44100,size=-16,channels=2,buffer=512)
# 窗口设置
WIDTH, HEIGHT = 440, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("游戏操作说明")
# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
#音频加载与设置
background_music = pg.mixer.Sound("Funky Town.mp3")
win_music = pg.mixer.Sound("Wang Fei.mp3")
#设置音量
background_music.set_volume(0.3)
win_music.set_volume(0.5)
background_playing = False
win_music_playing = False
# 字体设置
font_title = pg.font.SysFont("SimHei", 30, bold=True)
font_content = pg.font.SysFont("SimHei", 20)
font_btn = pg.font.SysFont("SimHei", 24)
# 按钮矩形区域
back_btn_rect = pg.Rect(150, 520, 140, 40)
# 操作说明文本内容
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
    "R键:重置游戏地图与位置"
    "【控制音乐】"
    "M键:控制音乐播放"
]
def draw_instructions():
    """绘制操作说明界面"""
    screen.fill(WHITE)
    
    # 绘制标题
    title_text = font_title.render("寻宝游戏操作说明", True, BLUE)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 30))
    
    # 绘制分割线
    pg.draw.line(screen, GRAY, (50, 80), (390, 80), 2)
    
    # 绘制说明文本
    y_offset = 100
    for line in instructions:
        text = font_content.render(line, True, BLACK)
        screen.blit(text, (60, y_offset))
        y_offset += 30
    
    # 绘制返回按钮
    pg.draw.rect(screen, GRAY, back_btn_rect, border_radius=5)
    pg.draw.rect(screen, BLACK, back_btn_rect, 2, border_radius=5)
    btn_text = font_btn.render("返回游戏", True, RED)
    screen.blit(btn_text, (back_btn_rect.x + 20, back_btn_rect.y + 5))
    
    pg.display.update()
def main():
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                # 点击返回按钮
                if back_btn_rect.collidepoint(event.pos):
                    #开始播放背景音乐
                    global background_playing
                    background_music.play(-1)
                    background_playing = True
                    running = False  # 关闭说明界面，返回游戏
        
        draw_instructions()
if __name__ == "__main__":
    main()
pg.init()
screen_background = pg.display.set_mode((1440, 800))
pg.display.set_caption("迷宫寻宝")
running = True
clock = pg.time.Clock()  #时钟，控制动画帧率
obstacle_length = 25  # 墙体边长
x_begin = 63
y_begin = 65
block_step = obstacle_length + 2  # 墙体间隔
map_rows = 25  # 墙体行数 (必须是奇数)
map_cols = 49  # 墙体列数
# 生成地图
map_of_treasure = np.ones((map_rows, map_cols), int)
recorder = np.zeros((int((map_rows - 1) / 2), int((map_cols - 1) / 2)), int)
for i in range(int((map_rows - 1) / 2)):
    for j in range(int((map_cols - 1) / 2)):
        map_of_treasure[2 * i + 1][2 * j + 1] = 0
random_move = [[1, 0], [0, 1], [0, -1], [-1, 0]]
recorder[0][0] = 1
# 生成地图
def map_generation(x: int, y: int):
    flag = 0
    r = random.randint(1, 4)  # 随机移动
    for i in range(4):
        xx = x + random_move[(r + i) % 4][0]
        yy = y + random_move[(r + i) % 4][1]
        if xx >= 0 and yy >= 0 and xx < (map_rows - 1) / 2 and yy < (map_cols - 1) / 2:
            if recorder[xx][yy] == 0:
                flag = 1
                recorder[xx][yy] = 1
                map_of_treasure[x + xx + 1][y + yy + 1] = 0  # 可以走的地方设置为0
                map_generation(xx, yy)
    if flag == 0:
        map_of_treasure[2 * x + 1][2 * y + 1] = 2  # 金币处设置为2
    return
map_generation(0, 0)
# 备份初始地图（含金币），用于重置时恢复
original_treasure_map = copy.deepcopy(map_of_treasure)
# 颜色设置
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

#素材加载
obstacle = pg.image.load("obstacle.jpg").convert_alpha()  # 加convert_alpha()适配透明
obstacle = pg.transform.scale(obstacle, (obstacle_length, obstacle_length))
score_font = pg.font.SysFont("Arial", 20, bold=True)  # 分数字体
score = 0  # 分数
score_text = score_font.render(f"score  {score}", True, WHITE)
penguin = pg.image.load("penguin_0.png").convert_alpha() 
penguin = pg.transform.scale(penguin, (obstacle_length, obstacle_length))

coin_front = pg.image.load("coin_front.png").convert_alpha()    # 正视图
coin_right_skew = pg.image.load("coin_right_skew.png").convert_alpha() # 斜右侧
coin_right_side = pg.image.load("coin_right_side.png").convert_alpha()  # 正右侧
coin_back = pg.image.load("coin_back.png").convert_alpha()      # 反视图
coin_left_side = pg.image.load("coin_left_side.png").convert_alpha()   # 正左侧
coin_left_skew = pg.image.load("coin_left_skew.png").convert_alpha()   # 斜左侧
coin = [coin_front, coin_right_skew, coin_right_side, coin_back, coin_left_side, coin_left_skew]
   
for i in range(len(coin)):
    coin[i] = pg.transform.scale(coin[i], (obstacle_length - 6, obstacle_length - 6))
# 金币旋转角度管理
coin_rotate_angles = {}
for i in range(map_rows):
    for j in range(map_cols):
        if map_of_treasure[i][j] == 2:
            coin_rotate_angles[(i, j)] = random.randint(0, 359)
# 企鹅初始位置
init_penguin_x = 1
init_penguin_y = 1
penguin_x = init_penguin_x
penguin_y = init_penguin_y
penguin_move_x = 0
penguin_move_y = 0

#素材加载
rose520 = pg.image.load("rose520.png").convert_alpha()
rose520 = pg.transform.scale(rose520, (obstacle_length - 4, obstacle_length - 4))  # 适配格子

big_penguin_front = pg.image.load("penguin_2_front.png").convert_alpha()
big_penguin_back = pg.image.load("penguin_2_back.png").convert_alpha()
base_height = 400
penguin_state = "front"
switch_timer = 0
switch_interval = 1000
current_width = 400
is_switching = False
target_width = 400
big_penguin_x = 1440//2 - current_width//2
big_penguin_y = 800//2 - base_height//2
big_penguin_pos =(big_penguin_x,big_penguin_y)


map_of_treasure[map_rows - 2][map_cols - 2] = 3  

original_treasure_map = copy.deepcopy(map_of_treasure)

game_over = False


# 金币旋转绘制函数
def draw_rotating_coin(screen, map_i, map_j):
    screen_x = x_begin + map_j * block_step + 3
    screen_y = y_begin + map_i * block_step + 3
    current_angle = coin_rotate_angles[(map_i, map_j)]
    coin_rotate_angles[(map_i, map_j)] = (current_angle + 2) % 360  # 角度更新
    # 角度区间匹配六视图
    angle = current_angle % 360
    if (angle >= 315 or angle < 45):
        img = coin[0]  # 正视图
    elif angle >= 45 and angle < 90:
        img = coin[1]  # 斜右侧
    elif angle >= 90 and angle < 135:
        img = coin[2]  # 正右侧
    elif angle >= 135 and angle < 225:
        img = coin[3]  # 反视图
    elif angle >= 225 and angle < 270:
        img = coin[4]  # 正左侧
    elif angle >= 270 and angle < 315:
        img = coin[5]  # 斜左侧
    screen.blit(img, (screen_x, screen_y))  
while running:
     # 获取窗口事件
     for event in pg.event.get():
         if event.type == pg.QUIT:
             running = False
         elif penguin_move_x == 0 and penguin_move_y == 0 and event.type == pg.KEYDOWN:
             if event.key == pg.K_LEFT:
                 if map_of_treasure[penguin_x][penguin_y - 1] != 1:
                     penguin_move_y = - block_step
                     penguin_y -= 1
             elif event.key == pg.K_RIGHT:
                 if map_of_treasure[penguin_x][penguin_y + 1] != 1:
                     penguin_move_y = block_step
                     penguin_y += 1
             elif event.key == pg.K_UP:
                 if map_of_treasure[penguin_x - 1][penguin_y] != 1:
                     penguin_move_x = - block_step
                     penguin_x -= 1
             elif event.key == pg.K_DOWN:
                 if map_of_treasure[penguin_x + 1][penguin_y] != 1:
                     penguin_move_x = block_step
                     penguin_x += 1
             elif event.key == pg.K_r:
                 penguin_x = init_penguin_x  
                 penguin_y = init_penguin_y  
                 score = 0  
                 map_of_treasure = copy.deepcopy(original_treasure_map) 
                 score_text = score_font.render(f"score  {score}", True, WHITE)  
                 # 重新初始化金币旋转角度
                 coin_rotate_angles.clear()
                 for i in range(map_rows):
                     for j in range(map_cols):
                         if map_of_treasure[i][j] == 2:
                             coin_rotate_angles[(i, j)] = random.randint(0, 359)
                             current_rotate_angle = 0
                             win_music_playing = False
                 print("游戏已重置！")
             elif event.key == pg.K_m:
                 if background_music:
                     background_music.stop()
                 else: background_music.play(-1)
                 background_playing = not background_playing
                 
                 game_over = False
                 
     if penguin_move_x < 0:
         penguin_move_x += 1
     if penguin_move_x > 0:
         penguin_move_x -= 1
     if penguin_move_y < 0:
         penguin_move_y += 1
     if penguin_move_y > 0:
         penguin_move_y -= 1


     
     if not game_over and map_of_treasure[penguin_x][penguin_y] == 3:
         game_over = True
         background_music.stop()
         if not win_music_playing:
             win_music.play()
             win_music_playing = True
         print(f"成功变身高雅人士！游戏结束，最终得分：{score}")
     

     # 吃金币并加分
     if not game_over and map_of_treasure[penguin_x][penguin_y] == 2:  # 游戏结束后不触发吃金币
         score += 1
         map_of_treasure[penguin_x][penguin_y] = 0
         score_text = score_font.render(f"score  {score}", True, WHITE)
         print("Got coin!")
         if (penguin_x, penguin_y) in coin_rotate_angles:
             del coin_rotate_angles[(penguin_x, penguin_y)]  # 收集后停止旋转
     # 绘制背景和标题栏
     screen_background.fill(YELLOW)  # 填充背景颜色
     pg.draw.rect(screen_background, BLACK, (50, 0, 1440, 25))  # 画标题栏
     screen_background.blit(score_text, (70, 0))  # 画分数
     for i in range(map_rows):
         for j in range(map_cols):
             if map_of_treasure[i][j] == 0:
                 continue
             if map_of_treasure[i][j] == 2:
                 draw_rotating_coin(screen_background, i, j)
                 continue
             
             if map_of_treasure[i][j] == 3:
                 # 玫瑰花绘制位置（与金币同居中）
                 screen_x = x_begin + j * block_step + 2
                 screen_y = y_begin + i * block_step + 2
                 screen_background.blit(rose520, (screen_x, screen_y))
                 continue
             
             screen_background.blit(obstacle, (x_begin + j * block_step, y_begin + i * block_step))  # 绘制墙体
     # 绘制企鹅
     screen_background.blit(penguin, (x_begin + penguin_y * block_step - penguin_move_y, y_begin + penguin_x * block_step - penguin_move_x))

     
     if game_over:
         # 计时器累加（毫秒）
         switch_timer += clock.get_time()
         # 到切换间隔，触发切换准备
         if switch_timer >= switch_interval and not is_switching:
             is_switching = True
             switch_timer = 0  # 重置计时器
             # 设定目标宽度（压缩到80像素，接近一条线时切换图片）
             target_width = 80
         # 切换中：横向压缩宽度
         if is_switching:
             if current_width > target_width:
                 current_width -= 2  # 每次减少2像素，控制平滑度
             else:
                 # 宽度压缩到目标，切换企鹅图片
                 penguin_state = "back" if penguin_state == "front" else "front"
                 # 切换后恢复宽度，准备下一次切换
                 current_width = 400
                 is_switching = False
                 win_music_playing = False
                 
         # 计算当前企鹅位置（始终居中）
         big_penguin_x = 1440 // 2 - current_width // 2
         big_penguin_pos = (big_penguin_x, big_penguin_y)
         # 选择当前显示的企鹅图片并缩放
         current_penguin = big_penguin_front if penguin_state == "front" else big_penguin_back
         current_penguin_scaled = pg.transform.smoothscale(current_penguin, (current_width, base_height))
         if game_over:
            screen_background.blit(current_penguin_scaled,big_penguin_pos)

         end_font = pg.font.SysFont("SimHei", 40, bold=True)
         end_text1 = end_font.render("明月几时有，把酒问青天", True, RED)
         end_text2 = end_font.render(f"最终得分：{score} | 按R键重置", True, BLUE)
         # 文字位置（企鹅上方和下方）
         screen_background.blit(end_text1, (1440//2 - end_text1.get_width()//2, 800//2 - 250))
         screen_background.blit(end_text2, (1440//2 - end_text2.get_width()//2, 800//2 + 220))
     

     pg.display.flip()
     
     if penguin_x == map_rows - 2 and penguin_y == map_cols - 2 and not game_over:
         win_text = score_font.render(f"congradulations!score:{score},press r to reset", True, RED)
         screen_background.blit(win_text, (600, 400))
         pg.display.flip()
         # 等待事件(可退出或按R重置)
         while running:
             for event in pg.event.get():
                 if event.type == pg.QUIT:
                     running = False
                 elif event.type == pg.KEYDOWN and event.key == pg.K_r:
                     penguin_x = init_penguin_x
                     penguin_y = init_penguin_y
                     score = 0
                     map_of_treasure = copy.deepcopy(original_treasure_map)
                     score_text = score_font.render(f"score  {score}", True, WHITE)
                     # 重置金币角度
                     coin_rotate_angles.clear()
                     for i in range(map_rows):
                         for j in range(map_cols):
                             if map_of_treasure[i][j] == 2:
                                 coin_rotate_angles[(i, j)] = random.randint(0, 359)
                     
                     game_over = False
                     
                     break  # 退出通关等待循环，回到主游戏循环
             if not running or (event.type == pg.KEYDOWN and event.key == pg.K_r):
                 break
     clock.tick(60)  # 控制帧率，保证旋转动画流畅
pg.mixer.stop()
pg.quit()