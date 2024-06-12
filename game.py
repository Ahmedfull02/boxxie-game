import pygame
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
TILE_SIZE = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Load images
def load_image(name):
    path = os.path.join('images', name)
    image = pygame.image.load(path)
    return pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))

player_image = load_image('player.png')
box_image = load_image('box.png')
target_image = load_image('target.png')
wall_image = load_image('wall.png')

# Define the level layout
level = [
    "WWWWWWWWWW",
    "W   W    W",
    "W B   T  W",
    "W   W    W",
    "WW WW    W",
    "W        W",
    "W   P    W",
    "W        W",
    "W        W", 
    "WWWWWWWWWW"
]

# Game objects
player_pos = None
boxes = []
targets = []
walls = []

for y, row in enumerate(level):
    for x, char in enumerate(row):
        if char == 'P':
            player_pos = [x, y]
        elif char == 'B':
            boxes.append([x, y])
        elif char == 'T':
            targets.append([x, y])
        elif char == 'W':
            walls.append([x, y])

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sokoban")

# Font
font = pygame.font.SysFont("monospace", 35)

# Draw the game
def draw_game():
    screen.fill(GRAY)
    
    for wall in walls:
        screen.blit(wall_image, (wall[0] * TILE_SIZE, wall[1] * TILE_SIZE))
    for target in targets:
        screen.blit(target_image, (target[0] * TILE_SIZE, target[1] * TILE_SIZE))
    for box in boxes:
        screen.blit(box_image, (box[0] * TILE_SIZE, box[1] * TILE_SIZE))
        
    screen.blit(player_image, (player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE))
    pygame.display.update()

# Check if position is a wall
def is_wall(pos):
    return pos in walls

# Check if position is a box
def is_box(pos):
    return pos in boxes

# Move box
def move_box(pos, direction):
    new_pos = [pos[0] + direction[0], pos[1] + direction[1]]
    if new_pos in walls or new_pos in boxes:
        return False
    boxes.remove(pos)
    boxes.append(new_pos)
    return True

# Check if level is completed
def check_win():
    for box in boxes:
        if box not in targets:
            return False
    return True

# Main game loop
game_running = True
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.KEYDOWN:
            direction = None
            if event.key == pygame.K_LEFT:
                direction = [-1, 0]
            elif event.key == pygame.K_RIGHT:
                direction = [1, 0]
            elif event.key == pygame.K_UP:
                direction = [0, -1]
            elif event.key == pygame.K_DOWN:
                direction = [0, 1]
            
            if direction:
                new_pos = [player_pos[0] + direction[0], player_pos[1] + direction[1]]
                if not is_wall(new_pos):
                    if is_box(new_pos):
                        if move_box(new_pos, direction):
                            player_pos = new_pos
                    else:
                        player_pos = new_pos
            
            if check_win():
                text = font.render("You Win!", True, GREEN)
                pygame.display.update()
                screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
                pygame.time.wait(2000)
                game_running = False

    draw_game()
    pygame.time.Clock().tick(30)

pygame.quit()
