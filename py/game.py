import pygame
import random
import sys
import os

pygame.init()
pygame.mixer.init()

# 判断是否为打包环境
if getattr(sys, 'frozen', False):
    asset_path = sys._MEIPASS
else:
    asset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

menu_music = os.path.join(asset_path, "mp3", "Toby Fox - Dogsong.mp3")
hit_sound = pygame.mixer.Sound(os.path.join(asset_path, "mp3", "collide.mp3"))
game_music = os.path.join(asset_path, "mp3", "Toby Fox - Song That Might Play When You Fight Sans.mp3")
end_music = os.path.join(asset_path, "mp3", "Toby Fox - sans_cbr.mp3")
buff_sound = pygame.mixer.Sound(os.path.join(asset_path, "mp3", "du.mp3"))

# 常量
CELL_SIZE = 70
MAP_WIDTH = 20
MAP_HEIGHT = 12
WINDOW_WIDTH = CELL_SIZE * MAP_WIDTH
WINDOW_HEIGHT = CELL_SIZE * MAP_HEIGHT
FPS = 60

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Car Game")
clock = pygame.time.Clock()

# 图片预处理优化
car_img = pygame.image.load(os.path.join(asset_path, "png", "car.png")).convert_alpha()
obstacle_img = pygame.image.load(os.path.join(asset_path, "png", "obstacle.png")).convert_alpha()
fail_img = pygame.image.load(os.path.join(asset_path, "png", "fail.png")).convert_alpha()
car_img = pygame.transform.scale(car_img, (int(1.7 * CELL_SIZE), int(1.1 * CELL_SIZE)))
obstacle_img = pygame.transform.scale(obstacle_img, (int(1.25 * CELL_SIZE), int(1.25 * CELL_SIZE)))
fail_img = pygame.transform.scale(fail_img, (int(8 * CELL_SIZE), int(8 * CELL_SIZE)))

swerve_img = pygame.image.load(os.path.join(asset_path, "png", "swerve.png")).convert_alpha()
swerve_img = pygame.transform.scale(swerve_img, (int(1.25 * CELL_SIZE), int(1.25 * CELL_SIZE)))

kraken_img = pygame.image.load(os.path.join(asset_path, "png", "kraken.png")).convert_alpha()
kraken_img = pygame.transform.scale(kraken_img, (int(1.25 * CELL_SIZE), int(1.25 * CELL_SIZE)))

xiaomai_img = pygame.image.load(os.path.join(asset_path, "png", "xiaomai.png")).convert_alpha()
xiaomai_img = pygame.transform.scale(xiaomai_img, (int(1.25 * CELL_SIZE), int(1.25 * CELL_SIZE)))

car_def_img = pygame.image.load(os.path.join(asset_path, "png", "car_def.png")).convert_alpha()
car_def_img = pygame.transform.scale(car_def_img, (int(1.7 * CELL_SIZE), int(1.8 * CELL_SIZE)))

double_img = pygame.image.load(os.path.join(asset_path, "png", "double.png")).convert_alpha()
double_img = pygame.transform.scale(double_img, (int(1.25 * CELL_SIZE), int(1.25 * CELL_SIZE)))

blind_img = pygame.image.load(os.path.join(asset_path, "png", "blind.png")).convert_alpha()
blind_img = pygame.transform.scale(blind_img, (int(1.25 * CELL_SIZE), int(1.25 * CELL_SIZE)))

font = pygame.font.SysFont("Arial", 36)
button_font = pygame.font.SysFont("Arial", 40)

button_rect = pygame.Rect(500, 300, 180, 60)
single_button_rect = pygame.Rect(500, 600, 180, 60)
restart_button_rect = pygame.Rect(500, 400, 180, 60)

single_play_mode = False
show_menu = True
game_over = False
loser = None
end_music_played = False

car_x, car_y = 5, 2
car2_x, car2_y = 5, 7
obstacles2 = []
score2 = 0
game_over2 = False
obstacles = []
single_obstacles = []
score = 0
obstacle_speed = 0.3

# ====== Powerups & Invincible Variables ======
powerups = []
invincible1 = False
invincible2 = False
invincible_end_time1 = 0
invincible_end_time2 = 0
reversed_controls1 = False
reversed_controls2 = False
reverse_end_time1 = 0
reverse_end_time2 = 0
double_score1 = False
double_score2 = False
double_score_end_time1 = 0
double_score_end_time2 = 0
xiaomai1 = False
xiaomai2 = False
xiaomai_end_time1 = 0
xiaomai_end_time2 = 0
blind1 = False
blind2 = False
blind_end_time1 = 0
blind_end_time2 = 0
# ============================================

start_time = pygame.time.get_ticks()
game_time_limit = 60000  # 1分钟 = 60000毫秒

last_move_time1 = 0
last_move_time2 = 0
MOVE_COOLDOWN = 100  # 毫秒

def draw_text_with_outline(text, font, color, outline_color, x, y):
    outline_range = 1
    for dx in range(-outline_range, outline_range + 1):
        for dy in range(-outline_range, outline_range + 1):
            if dx != 0 or dy != 0:
                outline_surface = font.render(text, True, outline_color)
                outline_rect = outline_surface.get_rect(center=(x + dx, y + dy))
                screen.blit(outline_surface, outline_rect)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

running = True
while running:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False

    if show_menu:
        # 绘制上半区深蓝，下半区深红
        screen.fill((30, 30, 60), rect=pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT // 2))
        screen.fill((60, 30, 30), rect=pygame.Rect(0, WINDOW_HEIGHT // 2, WINDOW_WIDTH, WINDOW_HEIGHT // 2))

        if not pygame.mixer.music.get_busy() or pygame.mixer.music.get_pos() < 0:
            pygame.mixer.music.load(menu_music)
            pygame.mixer.music.play(-1)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        # --- 渲染 single play 按钮 ---
        single_rect = single_button_rect.copy()
        single_color = (0, 120, 215)
        if single_rect.collidepoint(mouse_x, mouse_y):
            if mouse_pressed:
                single_color = (255, 0, 0)
                single_rect = single_rect.inflate(-10, -10)
            else:
                single_color = (0, 150, 255)
        pygame.draw.rect(screen, single_color, single_rect, border_radius=8)
        single_text = button_font.render("Single Play", True, (255, 255, 255))
        single_shadow = button_font.render("Single Play", True, (50, 50, 50))
        tx = single_rect.x + (single_rect.width - single_text.get_width()) // 2
        ty = single_rect.y + (single_rect.height - single_text.get_height()) // 2
        screen.blit(single_shadow, (tx + 2, ty + 2))
        screen.blit(single_text, (tx, ty))

        # --- 渲染 double play 按钮 ---
        multi_rect = button_rect.copy()
        multi_color = (0, 120, 215)
        if multi_rect.collidepoint(mouse_x, mouse_y):
            if mouse_pressed:
                multi_color = (255, 0, 0)
                multi_rect = multi_rect.inflate(-10, -10)
            else:
                multi_color = (0, 150, 255)
        pygame.draw.rect(screen, multi_color, multi_rect, border_radius=8)
        multi_text = button_font.render("Double Play", True, (255, 255, 255))
        multi_shadow = button_font.render("Double Play", True, (50, 50, 50))
        mtx = multi_rect.x + (multi_rect.width - multi_text.get_width()) // 2
        mty = multi_rect.y + (multi_rect.height - multi_text.get_height()) // 2
        screen.blit(multi_shadow, (mtx + 2, mty + 2))
        screen.blit(multi_text, (mtx, mty))

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if single_button_rect.collidepoint(event.pos):
                    # ===== 单人模式初始化逻辑 =====
                    show_menu = False
                    single_play_mode = True
                    car_x, car_y = 5, 2
                    obstacles.clear()
                    single_obstacles.clear()
                    powerups.clear()
                    score = 0
                    game_over = False
                    end_music_played = False
                    start_time = pygame.time.get_ticks()
                    invincible1 = False
                    invincible_end_time1 = 0
                    reversed_controls1 = False
                    reverse_end_time1 = 0
                    double_score1 = False
                    double_score_end_time1 = 0
                    xiaomai1 = False
                    xiaomai_end_time1 = 0
                    blind1 = False
                    blind_end_time1 = 0
                    pygame.mixer.music.load(game_music)
                    pygame.mixer.music.play(-1)
                elif button_rect.collidepoint(event.pos):
                    # ===== 双人模式初始化逻辑 =====
                    show_menu = False
                    single_play_mode = False
                    car_x, car_y = 5, 2
                    car2_x, car2_y = 5, 7
                    obstacles.clear()
                    obstacles2.clear()
                    single_obstacles.clear()
                    powerups.clear()
                    score = 0
                    score2 = 0
                    game_over = False
                    game_over2 = False
                    end_music_played = False
                    start_time = pygame.time.get_ticks()
                    invincible1 = invincible2 = False
                    invincible_end_time1 = invincible_end_time2 = 0
                    reversed_controls1 = reversed_controls2 = False
                    reverse_end_time1 = reverse_end_time2 = 0
                    double_score1 = double_score2 = False
                    double_score_end_time1 = double_score_end_time2 = 0
                    xiaomai1 = xiaomai2 = False
                    xiaomai_end_time1 = xiaomai_end_time2 = 0
                    blind1 = blind2 = False
                    blind_end_time1 = blind_end_time2 = 0
                    pygame.mixer.music.load(game_music)
                    pygame.mixer.music.play(-1)

        pygame.display.flip()
        clock.tick(FPS)
        continue

    if blind1 == False:
        screen.fill((30, 30, 60), rect=pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT // 2))
    if blind2 == False:
        screen.fill((60, 30, 30), rect=pygame.Rect(0, WINDOW_HEIGHT // 2, WINDOW_WIDTH, WINDOW_HEIGHT // 2))

    keys = pygame.key.get_pressed()
    if not show_menu and (not game_over or not game_over2):
        current_time = pygame.time.get_ticks()
        if current_time - last_move_time1 >= MOVE_COOLDOWN:
            if xiaomai1:
                move_direction = random.choice(['up', 'down', 'left', 'right'])
                if move_direction == 'up' and car_y > 0:
                    car_y -= 1
                elif move_direction == 'down' and car_y < (MAP_HEIGHT - 1 if single_play_mode else MAP_HEIGHT // 2 - 1):
                    car_y += 1
                elif move_direction == 'left' and car_x > 0:
                    car_x -= 1
                elif move_direction == 'right' and car_x < MAP_WIDTH - 1:
                    car_x += 1
                last_move_time1 = current_time
            else:
                if not reversed_controls1 and not single_play_mode:
                    if keys[pygame.K_w] and car_y > 0:
                        car_y -= 1
                    elif keys[pygame.K_s] and car_y < MAP_HEIGHT // 2 - 1:
                        car_y += 1
                    elif keys[pygame.K_a] and car_x > 0:
                        car_x -= 1
                    elif keys[pygame.K_d] and car_x < MAP_WIDTH - 1:
                        car_x += 1
                elif single_play_mode:
                    if keys[pygame.K_w] and car_y > 0:
                        car_y -= 1
                    elif keys[pygame.K_s] and car_y < MAP_HEIGHT - 1:
                        car_y += 1
                    elif keys[pygame.K_a] and car_x > 0:
                        car_x -= 1
                    elif keys[pygame.K_d] and car_x < MAP_WIDTH - 1:
                        car_x += 1
                else:
                    if keys[pygame.K_s] and car_y > 0:
                        car_y -= 1
                    elif keys[pygame.K_w] and car_y < MAP_HEIGHT // 2 - 1:
                        car_y += 1
                    elif keys[pygame.K_d] and car_x > 0:
                        car_x -= 1
                    elif keys[pygame.K_a] and car_x < MAP_WIDTH - 1:
                        car_x += 1
                last_move_time1 = current_time
        if not single_play_mode and current_time - last_move_time2 >= MOVE_COOLDOWN:
            if xiaomai2:
                move_direction = random.choice(['up', 'down', 'left', 'right'])
                if move_direction == 'up' and car2_y > 5:
                    car2_y -= 1
                elif move_direction == 'down' and car2_y < MAP_HEIGHT - 1:
                    car2_y += 1
                elif move_direction == 'left' and car2_x > 0:
                    car2_x -= 1
                elif move_direction == 'right' and car2_x < MAP_WIDTH - 1:
                    car2_x += 1
                last_move_time2 = current_time
            else:
                if not reversed_controls2:
                    if keys[pygame.K_UP] and car2_y > MAP_HEIGHT // 2 :
                        car2_y -= 1
                    elif keys[pygame.K_DOWN] and car2_y < MAP_HEIGHT - 1:
                        car2_y += 1
                    elif keys[pygame.K_LEFT] and car2_x > 0:
                        car2_x -= 1
                    elif keys[pygame.K_RIGHT] and car2_x < MAP_WIDTH - 1:
                        car2_x += 1
                else:
                    if keys[pygame.K_DOWN] and car2_y > 5:
                        car2_y -= 1
                    elif keys[pygame.K_UP] and car2_y < MAP_HEIGHT - 1:
                        car2_y += 1
                    elif keys[pygame.K_RIGHT] and car2_x > 0:
                        car2_x -= 1
                    elif keys[pygame.K_LEFT] and car2_x < MAP_WIDTH - 1:
                        car2_x += 1
                last_move_time2 = current_time

    if not (game_over and game_over2):
        if not single_play_mode:
            if random.randint(0, 12) == 0:
                obstacles.append([MAP_WIDTH - 1, random.randint(0, 5), False])
            if random.randint(0, 12) == 0:
                obstacles2.append([MAP_WIDTH - 1, random.randint(6, MAP_HEIGHT - 1), False])
        else:
            if random.randint(0, 8) == 0:
                single_obstacles.append([MAP_WIDTH - 1, random.randint(0, MAP_HEIGHT - 1), False])

        if not single_play_mode:
            if random.randint(0, 350) == 0:
                powerups.append([MAP_WIDTH - 1, random.randint(0, MAP_HEIGHT - 1), "invincible"])
            if random.randint(0, 350) == 0:
                powerups.append([MAP_WIDTH - 1, random.randint(0, MAP_HEIGHT - 1), "reverse"])
            if random.randint(0, 350) == 0:
                powerups.append([MAP_WIDTH - 1, random.randint(0, MAP_HEIGHT - 1), "double"])
            if random.randint(0, 650) == 0:
                powerups.append([MAP_WIDTH - 1, random.randint(0, MAP_HEIGHT - 1), "xiaomai"])
            if random.randint(0, 350) == 0:
                powerups.append([MAP_WIDTH - 1, random.randint(0, MAP_HEIGHT - 1), "blind"])
        else:
            if random.randint(0, 200) == 0:
                powerups.append([MAP_WIDTH - 1, random.randint(0, MAP_HEIGHT - 1), "invincible"])
            if random.randint(0, 200) == 0:
                powerups.append([MAP_WIDTH - 1, random.randint(0, MAP_HEIGHT - 1), "double"])

        if not single_play_mode:
            new_obstacles = []
            for ob in obstacles:
                ob[0] -= obstacle_speed
                if ob[0] > 0:
                    new_obstacles.append(ob)
                else:
                    if not game_over:
                        score += 2 if double_score1 else 1
            obstacles = new_obstacles
            if blind1:
                pygame.draw.rect(screen, (0, 0, 0), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT // 2))
            else:
                screen.fill((30, 30, 60), rect=pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT // 2))
                for ob in obstacles:
                    screen.blit(obstacle_img, (int(ob[0]) * CELL_SIZE, int(ob[1]) * CELL_SIZE))
            if invincible1:
                screen.blit(car_def_img, (car_x * CELL_SIZE, car_y * CELL_SIZE))
            else:
                screen.blit(car_img, (car_x * CELL_SIZE, car_y * CELL_SIZE))
            new_obstacles2 = []
            for ob in obstacles2:
                ob[0] -= obstacle_speed
                if ob[0] > 0:
                    new_obstacles2.append(ob)
                else:
                    if not game_over:
                        score2 += 2 if double_score2 else 1
            obstacles2 = new_obstacles2
            if blind2:
                pygame.draw.rect(screen, (0, 0, 0), (0, WINDOW_HEIGHT // 2, WINDOW_WIDTH, WINDOW_HEIGHT // 2))
            else:
                screen.fill((60, 30, 30), rect=pygame.Rect(0, WINDOW_HEIGHT // 2, WINDOW_WIDTH, WINDOW_HEIGHT // 2))
                for ob in obstacles2:
                    screen.blit(obstacle_img, (int(ob[0]) * CELL_SIZE, int(ob[1]) * CELL_SIZE))
            if invincible2:
                screen.blit(car_def_img, (car2_x * CELL_SIZE, car2_y * CELL_SIZE))
            else:
                screen.blit(car_img, (car2_x * CELL_SIZE, car2_y * CELL_SIZE))
        else:
            single_new_obstacles = []
            screen.fill((30, 30, 60), rect=pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
            for ob in single_obstacles:
                screen.blit(obstacle_img, (int(ob[0]) * CELL_SIZE, int(ob[1]) * CELL_SIZE))
                ob[0] -= obstacle_speed
                if ob[0] > 0:
                    single_new_obstacles.append(ob)
                else:
                    if not game_over:
                        score += 2 if double_score1 else 1
            single_obstacles = single_new_obstacles

        new_powerups = []
        for item in powerups:
            item[0] -= obstacle_speed
            if item[0] > 0:
                new_powerups.append(item)
        powerups = new_powerups

    for item in powerups[:]:
        if not single_play_mode:
            if int(item[0]) == car_x and int(item[1]) == car_y:
                if item[2] == "invincible":
                    invincible1 = True
                    invincible_end_time1 = pygame.time.get_ticks() + 3000
                elif item[2] == "reverse":
                    reversed_controls2 = True
                    reverse_end_time2 = pygame.time.get_ticks() + 3000
                elif item[2] == "double":
                    double_score1 = True
                    double_score_end_time1 = pygame.time.get_ticks() + 3000
                elif item[2] == "blind":
                    blind2 = True
                    blind_end_time2 = pygame.time.get_ticks() + 3000
                elif item[2] == "xiaomai":
                    xiaomai2 = True
                    xiaomai_end_time2 = pygame.time.get_ticks() + 3000
                buff_sound.play()
                powerups.remove(item)
            elif int(item[0]) == car2_x and int(item[1]) == car2_y:
                if item[2] == "invincible":
                    invincible2 = True
                    invincible_end_time2 = pygame.time.get_ticks() + 3000
                elif item[2] == "reverse":
                    reversed_controls1 = True
                    reverse_end_time1 = pygame.time.get_ticks() + 3000
                elif item[2] == "double":
                    double_score2 = True
                    double_score_end_time2 = pygame.time.get_ticks() + 3000
                elif item[2] == "blind":
                    blind1 = True
                    blind_end_time1 = pygame.time.get_ticks() + 3000
                elif item[2] == "xiaomai":
                    xiaomai1 = True
                    xiaomai_end_time1 = pygame.time.get_ticks() + 3000
                buff_sound.play()
                powerups.remove(item)
        else:
            if int(item[0]) == car_x and int(item[1]) == car_y:
                if item[2] == "invincible":
                    invincible1 = True
                    invincible_end_time1 = pygame.time.get_ticks() + 3000
                elif item[2] == "double":
                    double_score1 = True
                    double_score_end_time1 = pygame.time.get_ticks() + 3000
                buff_sound.play()
                powerups.remove(item)

    for ob in obstacles:
        if not ob[2] and int(ob[0] + 0.5) == car_x and int(ob[1] + 0.5) == car_y:
            if not invincible1:
                score = max(0, score - 10)
                hit_sound.play()
            ob[2] = True

    for ob in obstacles2:
        if not ob[2] and int(ob[0] + 0.5) == car2_x and int(ob[1] + 0.5) == car2_y:
            if not invincible2:
                score2 = max(0, score2 - 10)
                hit_sound.play()
            ob[2] = True

    if single_play_mode:
        for ob in single_obstacles:
            if not ob[2] and int(ob[0] + 0.5) == car_x and int(ob[1] + 0.5) == car_y:
                if not invincible1:
                    score = max(0, score - 10)
                    hit_sound.play()
                ob[2] = True

    elapsed_time = pygame.time.get_ticks() - start_time

    if elapsed_time >= game_time_limit and not (game_over and game_over2):
        game_over = True
        game_over2 = True
        if score > score2:
            loser = "p2"
        elif score < score2:
            loser = "p1"
        else:
            loser = None

    if invincible1:
        car_render_img1 = car_def_img
    else:
        car_render_img1 = car_img
    screen.blit(car_render_img1, (car_x * CELL_SIZE, car_y * CELL_SIZE))

    if not single_play_mode:
        if invincible2:
            car_render_img2 = car_def_img
        else:
            car_render_img2 = car_img
        screen.blit(car_render_img2, (car2_x * CELL_SIZE, car2_y * CELL_SIZE))

    for ob in obstacles:
        if not blind1:
            screen.blit(obstacle_img, (int(ob[0]) * CELL_SIZE, int(ob[1]) * CELL_SIZE))

    for ob in obstacles2:
        if not blind2:
            screen.blit(obstacle_img, (int(ob[0]) * CELL_SIZE, int(ob[1]) * CELL_SIZE))

    for item in powerups:
        if item[2] == "invincible":
            if (item[1] < MAP_HEIGHT // 2 and not blind1) or (item[1] >= MAP_HEIGHT // 2 and not blind2):
                screen.blit(swerve_img, (int(item[0]) * CELL_SIZE, int(item[1]) * CELL_SIZE))
        elif item[2] == "reverse":
            if (item[1] < MAP_HEIGHT // 2 and not blind1) or (item[1] >= MAP_HEIGHT // 2 and not blind2):
                screen.blit(kraken_img, (int(item[0]) * CELL_SIZE, int(item[1]) * CELL_SIZE))
        elif item[2] == "double":
            if (item[1] < MAP_HEIGHT // 2 and not blind1) or (item[1] >= MAP_HEIGHT // 2 and not blind2):
                screen.blit(double_img, (int(item[0]) * CELL_SIZE, int(item[1]) * CELL_SIZE))
        elif item[2] == "xiaomai":
            if (item[1] < MAP_HEIGHT // 2 and not blind1) or (item[1] >= MAP_HEIGHT // 2 and not blind2):
                screen.blit(xiaomai_img, (int(item[0]) * CELL_SIZE, int(item[1]) * CELL_SIZE))
        elif item[2] == "blind":
            screen.blit(blind_img, (int(item[0]) * CELL_SIZE, int(item[1]) * CELL_SIZE))

    if not single_play_mode:
        pygame.draw.line(screen, (255, 255, 255), (0, WINDOW_HEIGHT // 2), (WINDOW_WIDTH, WINDOW_HEIGHT // 2), 2)

    score_text = font.render(f"P1 Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (WINDOW_WIDTH // 4 - score_text.get_width() // 2, 10))
    if double_score1:
        bonus_text = font.render("x2!", True, (255, 215, 0))
        screen.blit(bonus_text, (WINDOW_WIDTH // 4 + score_text.get_width() // 2 + 10, 10))
    if reversed_controls1:
        reversed_text1 = font.render("REVERSED", True, (255, 100, 100))
        screen.blit(reversed_text1, (WINDOW_WIDTH // 4 - reversed_text1.get_width() // 2, 50))

    if not single_play_mode:
        score_text2 = font.render(f"P2 Score: {score2}", True, (255, 255, 255))
        screen.blit(score_text2, (3 * WINDOW_WIDTH // 4 - score_text2.get_width() // 2, WINDOW_HEIGHT // 2 + 10))
        if double_score2:
            bonus_text2 = font.render("x2!", True, (255, 215, 0))
            screen.blit(bonus_text2, (3 * WINDOW_WIDTH // 4 + score_text2.get_width() // 2 + 10, WINDOW_HEIGHT // 2 + 10))
        if reversed_controls2:
            reversed_text2 = font.render("REVERSED", True, (255, 100, 100))
            screen.blit(reversed_text2, (3 * WINDOW_WIDTH // 4 - reversed_text2.get_width() // 2, WINDOW_HEIGHT // 2 + 50))

    progress_width = int((1 - elapsed_time / game_time_limit) * WINDOW_WIDTH)
    progress_height = 10
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, WINDOW_WIDTH, progress_height))
    pygame.draw.rect(screen, (0, 200, 0), (0, 0, progress_width, progress_height))

    if game_over and (single_play_mode or game_over2):
        obstacles.clear()
        obstacles2.clear()
        if not end_music_played:
            pygame.mixer.music.pause()
            pygame.mixer.music.load(end_music)
            pygame.mixer.music.play(-1)
            end_music_played = True
        if single_play_mode:
            end_text = font.render(f"game ended, your score: {score}", True, (255, 255, 255))
            screen.blit(end_text, (WINDOW_WIDTH // 2 - end_text.get_width() // 2, 50))
        else:
            if loser == "p1":
                win_text = font.render("Player 2 Wins!", True, (255, 255, 255))
            elif loser == "p2":
                win_text = font.render("Player 1 Wins!", True, (255, 255, 255))
            else:
                win_text = font.render("Draw!", True, (255, 255, 255))
            screen.blit(win_text, (WINDOW_WIDTH // 2 - win_text.get_width() // 2, 50))

        screen.blit(fail_img, (WINDOW_WIDTH // 2 - fail_img.get_width() // 2, WINDOW_HEIGHT // 2 - 300))
        restart_button_rect.y = WINDOW_HEIGHT // 2 + 200
        restart_button_rect.x = WINDOW_WIDTH // 2 - restart_button_rect.width // 2
        mouse_x, mouse_y = pygame.mouse.get_pos()
        original_restart_rect = restart_button_rect.copy()
        if restart_button_rect.collidepoint(mouse_x, mouse_y):
            if pygame.mouse.get_pressed()[0]:
                restart_button_color = (255, 0, 0)
                restart_button_rect = restart_button_rect.inflate(-10, -10)
            else:
                restart_button_color = (0, 150, 255)
        else:
            restart_button_color = (0, 120, 215)
        pygame.draw.rect(screen, restart_button_color, restart_button_rect, border_radius=8)
        shadow_text = button_font.render("Restart", True, (50, 50, 50))
        screen.blit(shadow_text, (restart_button_rect.x + 17, restart_button_rect.y + 17))
        draw_text_with_outline("Restart", button_font, (255, 255, 255), (0, 0, 0), restart_button_rect.centerx, restart_button_rect.centery)
        restart_button_rect = original_restart_rect
        pygame.display.flip()
        for event in event_list:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and restart_button_rect.collidepoint(event.pos):
                car_x, car_y = 10, 2
                car2_x, car2_y = 10, 7
                obstacles.clear()
                obstacles2.clear()
                single_obstacles.clear()
                powerups.clear()
                score = 0
                score2 = 0
                obstacle_speed = 0.2
                end_music_played = False
                show_menu = True
                game_over = False
                game_over2 = False
                loser = None
                single_play_mode = False
                start_time = pygame.time.get_ticks()
                invincible1 = invincible2 = False
                invincible_end_time1 = invincible_end_time2 = 0
                reversed_controls1 = reversed_controls2 = False
                reverse_end_time1 = reverse_end_time2 = 0
                double_score1 = double_score2 = False
                double_score_end_time1 = double_score_end_time2 = 0
                xiaomai1 = xiaomai2 = False
                xiaomai_end_time1 = xiaomai_end_time2 = 0
                blind1 = blind2 = False
                blind_end_time1 = blind_end_time2 = 0
                pygame.mixer.music.stop()
                pygame.mixer.music.load(menu_music)
                pygame.mixer.music.play(-1)
        clock.tick(FPS)
        continue


    current_time = pygame.time.get_ticks()
    if invincible1 and current_time > invincible_end_time1:
        invincible1 = False
    if invincible2 and current_time > invincible_end_time2:
        invincible2 = False
    if reversed_controls1 and current_time > reverse_end_time1:
        reversed_controls1 = False
    if reversed_controls2 and current_time > reverse_end_time2:
        reversed_controls2 = False
    if double_score1 and current_time > double_score_end_time1:
        double_score1 = False
    if double_score2 and current_time > double_score_end_time2:
        double_score2 = False
    if xiaomai1 and current_time > xiaomai_end_time1:
        xiaomai1 = False
    if xiaomai2 and current_time > xiaomai_end_time2:
        xiaomai2 = False
    if blind1 and current_time > blind_end_time1:
        blind1 = False
    if blind2 and current_time > blind_end_time2:
        blind2 = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()