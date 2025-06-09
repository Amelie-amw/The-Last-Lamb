# Programmer(s): Amelie, Annika
# Date: May 30, 2025
# Description: pygame design

import sys
import pygame
from pygame.locals import *
from pygame.sprite import *
import time
import random


pygame.init()


FPS = 60
WIDTH = 640
HEIGHT = 480
TILE_SIZE = 32


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze RPG Game")
clock = pygame.time.Clock()
main_font = pygame.font.SysFont("fipps", 30)
big_font = pygame.font.SysFont("fipps", 100)

def load_scaled(path, size):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, size)

# Load Assets
start = load_scaled("startingPage.png", (WIDTH, HEIGHT))
bg = load_scaled("menuBackground.png", (WIDTH, HEIGHT))  
logo = load_scaled("logo.png", (300, 300))
dialogue_box = load_scaled("dialogue_box.png", (WIDTH, 130))  
black_bg = pygame.Surface((WIDTH, HEIGHT))
black_bg.fill(BLACK)



######################################################
'''CLASS'''
######################################################

# ----- MAZE (Easy Mode) -----
'''food class'''
class Food(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))

'''player class'''
class ImageSprite(Sprite):
    def __init__(self, x, y, filename):
        super().__init__()
        original_image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(original_image, (28, 28))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, new_x, new_y):
        self.rect.center = (new_x, new_y)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, visible=True):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        if visible:
            self.image.fill((0, 180, 0))
        else:
            self.image.set_alpha(0)  # Invisible
        self.rect = self.image.get_rect(topleft=(x, y))

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((255, 80, 200))
        pygame.draw.circle(self.image, (255, 255, 0), (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//3)
        self.rect = self.image.get_rect(topleft=(x, y))

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((255, 223, 0))
        pygame.draw.rect(self.image, (200, 0, 0), (4, 4, TILE_SIZE-8, TILE_SIZE-8), 3)
        self.rect = self.image(x, y, "lam.png")


# ----- GENERAL -----
'''button class'''
class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos, self.y_pos = pos
        self.rect = self.image.get_rect(center=pos)
        self.text_input = text_input
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color        
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def update(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        return self.rect.collidepoint(position)

    def changeColor(self, position):
        color = self.hovering_color if self.checkForInput(position) else self.base_color
        self.text = self.font.render(self.text_input, True, color)



######################################################
'''STORYLINE'''
######################################################

cg_texts = [
    "Lizard 1: The mutant king shot THE orb?!",
    "Lizard 2: WHAT!? OUR KING IS BARELY HOLDIN’ UP!",
    "*BANG*",
]

def dialogue(text, x, y):
    text_surface = main_font.render(text, True, WHITE)
    screen.blit(text_surface, (x, y))

def storyLine():
    dialogue_index = 0
    running = True
    while running and dialogue_index < len(cg_texts):
        screen.blit(black_bg, (0, 0))
        screen.blit(dialogue_box, (0, HEIGHT - 150))
        dialogue(cg_texts[dialogue_index], 50, HEIGHT - 110)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                dialogue_index += 2




######################################################
'''EASY MODE'''
######################################################
unlocked_nightmare = False

def mazeGame():
    global unlocked_nightmare

    maze = [
    "####################",
    "#......#..........E#",
    "#.#.##.#.##.#.######",
    "#.#.#.....#.#......#",
    "#...#.###.#.#####.##",
    "###.#...#....F#....#",
    "#...###.#####.#.####",
    "#.###...#.....#....#",
    "#.#F#.###.###.####.#",
    "#.#...#...#...#.#..#",
    "#.#######.###.#.#.##",
    "#.......#.#...#F#..#",
    "###.#####.#.#.#.##.#",
    "#.........#.#......#",
    "####################"
    ]

    ROWS = len(maze)
    COLS = len(maze[0])

    # Maze Setup
    def draw_maze(surface, maze, tile_size):
        for row_idx, row in enumerate(maze):
            for col_idx, char in enumerate(row):
                x = col_idx * tile_size
                y = row_idx * tile_size
                if char == "#":
                    pygame.draw.rect(surface, BLUE, (x, y, tile_size, tile_size))
                else:
                    pygame.draw.rect(surface, WHITE, (x, y, tile_size, tile_size))

    def get_tile_coords(char):
        coords = []
        for row_idx, row in enumerate(maze):
            for col_idx, c in enumerate(row):
                if c == char:
                    x = col_idx * TILE_SIZE + TILE_SIZE // 2
                    y = row_idx * TILE_SIZE + TILE_SIZE // 2
                    coords.append((x, y))
        return coords

    # Best Jump Scare
    def show_jumpscare():
        scare_img = pygame.image.load("1.png").convert()
        scare_img = pygame.transform.scale(scare_img, (WIDTH, HEIGHT))
        screen.blit(scare_img, (0, 0))
        pygame.display.flip()
        time.sleep(1)

    # Game Setup
    x, y = get_tile_coords("E")[0]
    sprite = ImageSprite(x, y, "lam.png")
    player_group = pygame.sprite.Group(sprite)

    food_group = pygame.sprite.Group()
    for pos in get_tile_coords("F"):
        food = Food(*pos)
        food_group.add(food)

    food_collected = 0
    game_over = False
    win = False

    # ----- Game Loop -----
    running = True
    while running:
        clock.tick(FPS)

        if game_over:
            show_jumpscare()   
            # Call the restart/quit menu after the scare
            game_over_screen()  

        if win:
            unlocked_nightmare = True
            main_menu()
            

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[K_LEFT]: dx = -2
        if keys[K_RIGHT]: dx = 2
        if keys[K_UP]: dy = -2
        if keys[K_DOWN]: dy = 2

        def is_touching_wall(x, y):
            # Check 4 nearby points around the sprite to make wall detection more sensitive
            offsets = [(-10, 0), (10, 0), (0, -10), (0, 8)]
            for dx, dy in offsets:
                check_x = x + dx
                check_y = y + dy
                col = check_x // TILE_SIZE
                row = check_y // TILE_SIZE
                if 0 <= row < ROWS and 0 <= col < COLS:
                    if maze[row][col] == "#":
                        return True
            return False

        # Predict new position
        new_x = x + dx
        new_y = y + dy

        if not is_touching_wall(new_x, new_y):
            x, y = new_x, new_y
        else:
            game_over = True

        # Check food collection
        sprite.update(x, y)
        hit_list = pygame.sprite.spritecollide(sprite, food_group, dokill=True)
        food_collected += len(hit_list)
        if food_collected >= 3:
            win = True

        # ----- Drawing -----
        screen.fill(BLACK)
        draw_maze(screen, maze, TILE_SIZE)
        food_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()

    pygame.quit()


######################################################
'''NIGHTMARE MODE'''
######################################################

def timeGame():  

    TILE_SIZE = 28
    MAZE_WIDTH = 24
    MAZE_HEIGHT = 15
    SCREEN_WIDTH = MAZE_WIDTH * TILE_SIZE
    SCREEN_HEIGHT = MAZE_HEIGHT * TILE_SIZE
    FPS = 60
    GRAVITY = 0.7
    PLAYER_SPEED = 3
    JUMP_STRENGTH = 12
    MAX_LIVES = 3

    maze = [
        ".WWWWWWW...............W",
        ".W.W...W.WWW.........W.W",
        ".W...W.....WWW.....WWW.W",
        ".W.WWWWW...........W...W",
        ".W.....W........W..W.WWW",
        ".WWWWW.W...W.......W.W..",
        "...C...W...........W....",
        "..WWWWWW.....W......W.W.",
        "..W..........WWW..W.W.W.",
        "..W...............W.W.WC",
        "..W.....WWWW....W.WWW.W.",
        ".WW...WWW.......W.....W.",
        "..W........W.......WWWW.",
        "W.WWW......WWWW......W..",
        "W..................W....",
    ]

    # ----- Class -----
    '''i cant place them to the top with other class
        so here it is... '''
    class Platform(pygame.sprite.Sprite):
        def __init__(self, x, y, visible=True):
            super().__init__()
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            if visible:
                self.image.fill((0, 180, 0))
            else:
                self.image.set_alpha(0)
            self.rect = self.image.get_rect(topleft=(x, y))

    class Collectible(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.image.fill((255, 80, 200))
            pygame.draw.circle(self.image, (255, 255, 0), (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//3)
            self.rect = self.image.get_rect(topleft=(x, y))

    class Goal(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.image.fill((255, 223, 0))
            pygame.draw.rect(self.image, (200, 0, 0), (4, 4, TILE_SIZE-8, TILE_SIZE-8), 3)
            self.rect = self.image.get_rect(topleft=(x, y))

    class Player(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.image.load("lam.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (TILE_SIZE - 3, TILE_SIZE - 3))
            self.rect = self.image.get_rect(topleft=(x, y))
            self.vel_y = 0
            self.on_ground = False
            self.use_up_key = False

        def update(self):
            keys = pygame.key.get_pressed()
            dx = 0
            if keys[pygame.K_LEFT]:
                dx = -PLAYER_SPEED
            if keys[pygame.K_RIGHT]:
                dx = PLAYER_SPEED
            self.rect.x += dx

            for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    if dx > 0:
                        self.rect.right = platform.rect.left
                    elif dx < 0:
                        self.rect.left = platform.rect.right

            self.vel_y += GRAVITY
            self.rect.y += self.vel_y
            self.on_ground = False

            for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        self.vel_y = 0
                        self.on_ground = True
                    elif self.vel_y < 0:
                        self.rect.top = platform.rect.bottom
                        self.vel_y = 0

            jump_key = pygame.K_UP if self.use_up_key else pygame.K_SPACE
            if keys[jump_key] and self.on_ground:
                self.vel_y = -JUMP_STRENGTH

    class Enemy(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.Surface((TILE_SIZE - 6, TILE_SIZE - 6))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(center=(x, y))
            self.vx = random.choice([-2, 2])
            self.vy = random.choice([-2, 2])

        def update(self):
            new_rect = self.rect.move(self.vx, self.vy)
            if is_wall(new_rect.centerx, self.rect.centery):
                self.vx *= -1
            else:
                self.rect.x += self.vx
            if is_wall(self.rect.centerx, new_rect.centery):
                self.vy *= -1
            else:
                self.rect.y += self.vy

    #maze layout built
    def is_wall(x, y):
        col = x // TILE_SIZE
        row = y // TILE_SIZE
        if 0 <= col < MAZE_WIDTH and 0 <= row < MAZE_HEIGHT:
            return maze[row][col] == 'W'
        return True

    def draw_maze():
        for row_idx, row in enumerate(maze):
            for col_idx, tile in enumerate(row):
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE
                if tile == 'W':
                    pygame.draw.rect(screen, (0, 180, 0), (x, y, TILE_SIZE, TILE_SIZE))

    def get_valid_positions():
        positions = []
        for row in range(MAZE_HEIGHT):
            for col in range(MAZE_WIDTH):
                if maze[row][col] != "W":
                    x = col * TILE_SIZE + TILE_SIZE // 2
                    y = row * TILE_SIZE + TILE_SIZE // 2
                    positions.append((x, y))
        return positions

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Nightmare Mode")
    clock = pygame.time.Clock()

    # Sprite Groups
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()
    goal_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

    # Build Level
    player_start = (0, 0)
    for row_idx, row in enumerate(maze):
        for col_idx, tile in enumerate(row):
            x = col_idx * TILE_SIZE
            y = row_idx * TILE_SIZE
            if tile == 'W':
                plat = Platform(x, y)
                platforms.add(plat)
                all_sprites.add(plat)
            elif tile == 'C':
                c = Collectible(x, y)
                collectibles.add(c)
                all_sprites.add(c)
            elif tile == 'E':
                goal = Goal(x, y)
                goal_group.add(goal)
                all_sprites.add(goal)
            elif tile == '.' and player_start == (0, 0) and row_idx == 0 and col_idx == 0:
                player_start = (x, y)

    # Invisible Borders
    for x in range(-TILE_SIZE, SCREEN_WIDTH + TILE_SIZE, TILE_SIZE):
        platforms.add(Platform(x, -TILE_SIZE, visible=False))
        platforms.add(Platform(x, SCREEN_HEIGHT, visible=False))
    for y in range(-TILE_SIZE, SCREEN_HEIGHT + TILE_SIZE, TILE_SIZE):
        platforms.add(Platform(-TILE_SIZE, y, visible=False))
        platforms.add(Platform(SCREEN_WIDTH, y, visible=False))

    player = Player(*player_start)
    all_sprites.add(player)

    # Enemies
    for _ in range(3):
        x, y = random.choice(get_valid_positions())
        enemy = Enemy(x, y)
        enemy_group.add(enemy)

    # Game State
    collected = 0
    required_collect = len(collectibles)
    won = False
    start_ticks = pygame.time.get_ticks()
    timer_duration = 50  #in seconds
    lives = MAX_LIVES
    show_jump_instruction = True


    # ----- Game Loop -----
    running = True
    while running:
        clock.tick(FPS)
        # remaining TIME
        seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
        time_left = max(0, timer_duration - int(seconds_passed))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                player.use_up_key = not player.use_up_key
                show_jump_instruction = False

        if lives > 0 and not won:
            player.update()
            enemy_group.update()

            # Collectibles
            hits = pygame.sprite.spritecollide(player, collectibles, True)
            if hits:
                collected += len(hits)

            # Win
            if collected >= required_collect and pygame.sprite.spritecollide(player, goal_group, False):
                won = True

            # Enemy Hit
            if pygame.sprite.spritecollide(player, enemy_group, False):
                lives -= 1
                player.rect.topleft = player_start

        # Draw
        screen.fill((220, 220, 220))
        draw_maze()
        all_sprites.draw(screen)
        enemy_group.draw(screen)

        font = pygame.font.SysFont(None, 28)
        
        # life remaining
        life_text = font.render(f"Lives: {lives}", True, (0, 0, 0))
        screen.blit(life_text, (10, 5))
        
        # 50 s timer
        timer_text = font.render(f"Time: {time_left}s", True, (0, 0, 0))
        screen.blit(timer_text, (SCREEN_WIDTH - 120, 5))

        if won:
            font2 = pygame.font.SysFont(None, 64)
            text2 = font2.render("YOU WIN!", True, (0, 180, 0))
            screen.blit(text2, (SCREEN_WIDTH//2-120, SCREEN_HEIGHT//2-32))
        
        # Timer runs out = Game over
        if time_left <= 0 and not won:
            lives = 0  # !! game over
            
        if lives <= 0:
            game_over_screen()

        if show_jump_instruction:
            jump_text = font.render("Press ENTER to toggle jump key (SPACE/UP)", True, (0, 0, 0))
            screen.blit(jump_text, (SCREEN_WIDTH//2 - 180, SCREEN_HEIGHT - 30))
            
        pygame.display.flip()

    pygame.quit()


######################################################
'''GENERAL'''
######################################################

# Main Menu
button1 = load_scaled("button.jpg", (180, 60))
button2 = load_scaled("unlock.png", (300, 100))
button3 = load_scaled("button.png", (200, 60))

def main_menu():
    global unlocked_nightmare #if ture then ture lol
    nightmare_button = None  # Prevent reference error

    while True:
        screen.blit(bg, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        
        # Always-visible buttons
        story_button = Button(button1, (WIDTH//2 + 150, 360), "Story", main_font, WHITE, GREEN)
        maze_button = Button(button1, (WIDTH//2 + 150, 430), "Easy Mode", main_font, WHITE, GREEN)

        for button in [story_button, maze_button]:
            button.changeColor(mouse_pos)
            button.update(screen)

        # Conditionally create and show Nightmare button
        if unlocked_nightmare:
            nightmare_button = Button(button2, (WIDTH//2 - 160, 60), "Nightmare Mode", main_font, WHITE, GREEN)
            nightmare_button.changeColor(mouse_pos)
            nightmare_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if maze_button.checkForInput(mouse_pos):
                    mazeGame()
                if story_button.checkForInput(mouse_pos):
                    storyLine()
                if unlocked_nightmare and nightmare_button and nightmare_button.checkForInput(mouse_pos):
                    timeGame()  

        pygame.display.update()
        clock.tick(FPS)

# Game Over Page ;)
def game_over_screen():
    while True:
        screen.fill((0, 0, 0))  # Black background

        # Shown text
        game_over_text = big_font.render("Game Over", True, RED)
        restart_button = Button(button3, (WIDTH//2, 300), "Restart", main_font, WHITE, GREEN)
        quit_button = Button(button3, (WIDTH//2, 380), "Main Menu", main_font, WHITE, GREEN)

        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, 150))

        mouse_pos = pygame.mouse.get_pos()
        for button in [restart_button, quit_button]:
            button.changeColor(mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.checkForInput(mouse_pos):
                    mazeGame()  # Restart the game (or call main_menu() if you want to go back)
                    return
                if quit_button.checkForInput(mouse_pos):
                    main_menu()

        pygame.display.update()
        clock.tick(FPS)


def startGame():
    clock = pygame.time.Clock()
    while True:
        screen.blit(start, (0, 0))
        screen.blit(logo, (WIDTH - logo.get_width() - 5, 200))
        text = "< Press any button to start >"
        text_surface = main_font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2 - 180))
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                main_menu()

        pygame.display.flip()
        clock.tick(FPS)

startGame()

