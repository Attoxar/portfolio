import pygame
import random
# import sys
# from PIL import Image
from moviepy.editor import *

# Initialize Pygame
pygame.init()

# Set screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders 2K")

menu_background_img = pygame.image.load('menu_background.jpg').convert()
game_background_img = pygame.image.load('game_background.jpg').convert()

menu_music = pygame.mixer.Sound("menu_music.mp3")
game_music = pygame.mixer.Sound("game_music.mp3")

laser_sound = pygame.mixer.Sound('laser.wav')
enemy_hit_sound = pygame.mixer.Sound('enemy_hit.wav')
collision_sound = pygame.mixer.Sound('collision.wav')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Fonts
FONT = pygame.font.Font(None, 36)


# Main menu loop
def main_menu():
    menu_music.play(loops=-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu_music.stop()
                    return "start"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        SCREEN.blit(menu_background_img, (0, 0))
        draw_text("Press ENTER to Start", FONT, WHITE, SCREEN, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        draw_text("Press ESC to Quit", FONT, WHITE, SCREEN, SCREEN_WIDTH/2, SCREEN_HEIGHT * 3/4)
        pygame.display.flip()


# Draw text helper function
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)


# Player
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
player_img = pygame.image.load('player.png')
player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
player_rect = player_img.get_rect()
player_rect.centerx = SCREEN_WIDTH // 2
player_rect.bottom = SCREEN_HEIGHT - 10
PLAYER_SPEED = 5

# Enemies
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 40
enemy_img = pygame.image.load('enemy.png')
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))
enemy_list = []
ENEMY_SPEED = 2

# Bullets
BULLET_WIDTH = 5
BULLET_HEIGHT = 10
bullet_img = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))
bullet_img.fill(RED)
bullet_list = []
BULLET_SPEED = 5

# Game variables
score = 0
game_over = False
level = 1


def create_enemies():
    num_enemies = int(5 * 1.5 ** (level - 1))  # Increase number of enemies by 50% for each level
    for i in range(num_enemies):
        enemy = enemy_img.get_rect()
        enemy.x = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
        enemy.y = random.randint(-500, -ENEMY_HEIGHT)
        enemy_list.append(enemy)


def move_enemies():
    global level
    for enemy in enemy_list:
        enemy.y += ENEMY_SPEED + (level - 1) * 1  # Increase enemy speed by 2 for each level
        if enemy.y > SCREEN_HEIGHT:
            enemy.y = random.randint(-500, -ENEMY_HEIGHT)
            enemy.x = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)


def move_bullets():
    for bullet in bullet_list:
        bullet.y -= BULLET_SPEED


def draw_objects():
    SCREEN.blit(player_img, player_rect)
    for enemy in enemy_list:
        SCREEN.blit(enemy_img, enemy)
    for bullet in bullet_list:
        pygame.draw.rect(SCREEN, RED, bullet)

    score_text = FONT.render("Score: " + str(score), True, WHITE)
    SCREEN.blit(score_text, (10, 10))

    if game_over:
        game_over_text = FONT.render("You're DEAD! Press R to Retry or ESC to Quit", True, WHITE)
        SCREEN.blit(game_over_text, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2))
    else:
        level_text = FONT.render("Level: " + str(level), True, WHITE)
        SCREEN.blit(level_text, (SCREEN_WIDTH - 120, 10))


# Main game loop
menu_result = main_menu()
while menu_result == "start":
    game_music.play(loops=-1)
    create_enemies()
    clock = pygame.time.Clock()
    running = True
    while running:
        SCREEN.blit(game_background_img, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game_over:
                laser_sound.play()
                bullet = bullet_img.get_rect()
                bullet.centerx = player_rect.centerx
                bullet.bottom = player_rect.top
                bullet_list.append(bullet)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
                game_over = False
                score = 0
                level = 1
                enemy_list.clear()
                bullet_list.clear()
                create_enemies()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and game_over:
                game_over = False
                game_music.stop()
                menu_result = main_menu()
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.x > 0:
            player_rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and player_rect.x < SCREEN_WIDTH - PLAYER_WIDTH:
            player_rect.x += PLAYER_SPEED

        if not game_over:
            move_enemies()
            move_bullets()

            # Check for collisions
            for enemy in enemy_list:
                if player_rect.colliderect(enemy):
                    collision_sound.play()
                    game_over = True
                for bullet in bullet_list:
                    if bullet.colliderect(enemy):
                        enemy_hit_sound.play()
                        enemy_list.remove(enemy)
                        bullet_list.remove(bullet)
                        score += 1

            if len(enemy_list) == 0:
                if level < 10:  # Increase level until level 10
                    level += 1
                create_enemies()

        draw_objects()

        pygame.display.flip()
        clock.tick(60)

pygame.quit()
sys.exit()
