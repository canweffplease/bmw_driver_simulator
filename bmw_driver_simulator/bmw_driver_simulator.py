import pygame
import random
import os
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

sprite_path = "C:\\Users\\Chris\\Documents\\stuff_for_github\\bmw_driver_simulator\\Topdown_vehicle_sprites_pack"

player_sprite = pygame.image.load(os.path.join(sprite_path, 'player.png'))
player_sprite = pygame.transform.scale(player_sprite, (50, 50))

bullet_sprite_width, bullet_sprite_height = 50, 50
bullet_hitbox_width = 30
initial_bullet_speed = 10
bullets = []

bullet_sprites = []
for i in range(1, 9):
    img = pygame.image.load(os.path.join(sprite_path, f'{i}.png'))
    img = pygame.transform.scale(img, (bullet_sprite_width, bullet_sprite_height))
    bullet_sprites.append(img)

WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

num_lanes = 15
lane_width = WIDTH // num_lanes
bullet_centers = [(lane_width * i + lane_width // 2) for i in range(num_lanes)]

road_speed = 10
lane_divider_length = 20
gap = 20
road_y = 0

FPS = 60
clock = pygame.time.Clock()

def draw_road(road_y):
    screen.fill(GRAY)
    for i in range(1, num_lanes):
        pygame.draw.line(screen, WHITE, (lane_width * i, 0), (lane_width * i, HEIGHT), 5)
    y_pos = road_y % (lane_divider_length + gap) - (lane_divider_length + gap)
    while y_pos < HEIGHT:
        for i in range(1, num_lanes):
            pygame.draw.line(screen, YELLOW, (lane_width * i, y_pos), (lane_width * i, y_pos + lane_divider_length), 5)
        y_pos += lane_divider_length + gap

def game_over_screen(survival_time):
    screen.fill(GRAY)
    font = pygame.font.SysFont(None, 48)
    game_over_text = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Survived: {survival_time} seconds", True, WHITE)
    replay_text = font.render("Click to Replay", True, YELLOW)

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(replay_text, (WIDTH // 2 - replay_text.get_width() // 2, HEIGHT // 1.5))

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting_for_input = False

player_sprite_size = 50
player_hitbox_width = 30

def main_game():
    start_time = time.time()
    bullets = []

    running = True
    global road_y
    while running:
        current_time = time.time() - start_time
        bullet_speed = initial_bullet_speed + current_time
        print(bullet_speed)
        road_y += road_speed
        draw_road(road_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        player_x, player_y = pygame.mouse.get_pos()
        player_hitbox_x = player_x - player_hitbox_width // 2
        player_rect = pygame.Rect(player_hitbox_x, HEIGHT - 60, player_hitbox_width, player_sprite_size)
        screen.blit(player_sprite, (player_x - player_sprite_size // 2, HEIGHT - 60))
        pygame.draw.rect(screen, RED, player_rect, 2)

        if random.randint(1, 20) == 1:
            lane = random.choice(bullet_centers)
            bullet_x = lane - bullet_sprite_width // 2
            bullet_sprite = random.choice(bullet_sprites)
            bullets.append([bullet_x, -bullet_sprite_height, bullet_sprite])

        for bullet in bullets[:]:
            bullet[1] += bullet_speed
            screen.blit(bullet[2], (bullet[0], bullet[1]))
            bullet_hitbox_x = bullet[0] + (bullet_sprite_width - bullet_hitbox_width) // 2
            bullet_rect = pygame.Rect(bullet_hitbox_x, bullet[1], bullet_hitbox_width, bullet_sprite_height)
            pygame.draw.rect(screen, RED, bullet_rect, 2)
            if player_rect.colliderect(bullet_rect):
                game_over_screen(round(current_time, 2))
                running = False
                break

        survival_time = round(current_time, 2)
        font = pygame.font.SysFont(None, 36)
        timer_text = font.render(f"Time: {survival_time} s", True, WHITE)
        screen.blit(timer_text, (10, 10))

        bullets = [bullet for bullet in bullets if bullet[1] < HEIGHT]

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    while True:
        main_game()
