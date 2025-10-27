import pygame, random, sys

# Initialize
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
RED = (255, 60, 60)
BLACK = (0, 0, 0)

# Player setup
player = pygame.Rect(50, HEIGHT//2 - 25, 40, 40)
speed = 5

# Obstacle setup
obstacles = []
obstacle_timer = 0
obstacle_interval = 1500  # milliseconds
score = 0
game_over = False

# Main loop
start_time = pygame.time.get_ticks()
while True:
    dt = clock.tick(60)
    screen.fill(BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if not game_over:
        # Move player
        if keys[pygame.K_UP] and player.top > 0:
            player.y -= speed
        if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
            player.y += speed

        # Spawn obstacles
        obstacle_timer += dt
        if obstacle_timer > obstacle_interval:
            obstacle_timer = 0
            y = random.randint(0, HEIGHT - 40)
            obstacles.append(pygame.Rect(WIDTH, y, 40, 40))

        # Move obstacles
        for obs in obstacles:
            obs.x -= 6

        # Remove off-screen obstacles
        obstacles = [obs for obs in obstacles if obs.right > 0]

        # Collision check
        for obs in obstacles:
            if player.colliderect(obs):
                game_over = True
                end_time = pygame.time.get_ticks()

        # Draw
        pygame.draw.rect(screen, RED, player)
        for obs in obstacles:
            pygame.draw.rect(screen, BLACK, obs)

        # Score
        score = (pygame.time.get_ticks() - start_time) // 1000
        text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text, (10, 10))
    else:
        # Game Over screen
        game_over_text = font.render("Game Over!", True, WHITE)
        score_text = font.render(f"Your Score: {score}", True, WHITE)
        screen.blit(game_over_text, (WIDTH//2 - 80, HEIGHT//2 - 40))
        screen.blit(score_text, (WIDTH//2 - 90, HEIGHT//2))
        restart_text = font.render("Press R to Restart", True, WHITE)
        screen.blit(restart_text, (WIDTH//2 - 120, HEIGHT//2 + 40))
        if keys[pygame.K_r]:
            player.y = HEIGHT//2 - 25
            obstacles = []
            start_time = pygame.time.get_ticks()
            game_over = False

    pygame.display.flip()
