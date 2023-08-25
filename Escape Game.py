import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maze Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the player
player_size = 30
player = pygame.Rect(width // 2 - player_size // 2, height - player_size * 2, player_size, player_size)
player_speed = 3  # Slower speed

# Set up opponent shapes
opponent_size = 30
opponents = []
num_opponents = 3

# Set up the endpoint
end_block_size = 50
end_block = pygame.Rect(random.randint(0, width - end_block_size), random.randint(0, height - end_block_size), end_block_size, end_block_size)

# Set up walls
wall_width = 20
walls = [
    pygame.Rect(100, 100, wall_width, 200),
    pygame.Rect(width - 120, 100, wall_width, 200),
    pygame.Rect(300, height // 2 - wall_width // 2, 200, wall_width),
    pygame.Rect(width // 2 - wall_width // 2, 300, wall_width, 200)
]

def reset_game():
    global opponents, player, end_block
    player.x = width // 2 - player_size // 2
    player.y = height - player_size * 2
    opponents = []
    for _ in range(num_opponents):
        opponent = pygame.Rect(random.randint(0, width - opponent_size), random.randint(0, height), opponent_size, opponent_size)
        opponents.append(opponent)
    end_block.x = random.randint(0, width - end_block_size)
    end_block.y = random.randint(0, height - end_block_size)

reset_game()

# Main game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed
    if keys[pygame.K_UP]:
        player.y -= player_speed
    if keys[pygame.K_DOWN]:
        player.y += player_speed

    # Limit player movement within the screen
    player.x = max(0, min(player.x, width - player.width))
    player.y = max(0, min(player.y, height - player.height))

    # Prevent player from passing through walls
    for wall in walls:
        if player.colliderect(wall):
            if player.x < wall.x:
                player.x = wall.left - player.width
            if player.x > wall.x:
                player.x = wall.right
            if player.y < wall.y:
                player.y = wall.top - player.height
            if player.y + player.height > wall.y:
                player.y = wall.bottom

    # Move opponent shapes
    for opponent in opponents:
        if player.x < opponent.x:
            opponent.x -= 1
        else:
            opponent.x += 1
        if player.y < opponent.y:
            opponent.y -= 1
        else:
            opponent.y += 1

        # Check for collision with walls
        for wall in walls:
            if opponent.colliderect(wall):
                if opponent.x < wall.x:
                    opponent.x = wall.left - opponent.width
                if opponent.x > wall.x:
                    opponent.x = wall.right
                if opponent.y < wall.y:
                    opponent.y = wall.top - opponent.height
                if opponent.y + opponent.height > wall.y:
                    opponent.y = wall.bottom

        # Check for collision with player
        if player.colliderect(opponent):
            reset_game()

    # Check for reaching the endpoint
    if player.colliderect(end_block):
        reset_game()

    # Draw game elements
    display.fill(BLACK)
    pygame.draw.rect(display, GREEN, player)
    pygame.draw.rect(display, WHITE, end_block)
    for opponent in opponents:
        pygame.draw.rect(display, RED, opponent)
    for wall in walls:
        pygame.draw.rect(display, WHITE, wall)

    pygame.display.flip()
    clock.tick(60)
