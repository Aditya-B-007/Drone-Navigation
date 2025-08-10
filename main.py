import pygame
import random
from pathfinding_logic import Searcher
from drone import Drone
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
TILE_SIZE = 16
GRID_WIDTH = SCREEN_WIDTH // TILE_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // TILE_SIZE
kappu=(0,0,0)
bili=(255,255,255)
gray=(40,40,40)
red=(255,0,0)
PATH_COLOR = (173, 216, 230)
OPEN_SET_COLOR = (144, 238, 144)
CLOSED_SET_COLOR = (255, 160, 122)
OBSTACLE_DENSITY = 0.09
Start_pos = (2, 2)
End_pos = (GRID_HEIGHT - 3, GRID_WIDTH - 3)
def generate_obstacles(grid, density):
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if random.random() < density:
                grid[row][col] = 1
            else:
                grid[row][col] = 0
true_grid=[[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
generate_obstacles(true_grid,OBSTACLE_DENSITY)
known_grid=[[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
for row in range(GRID_HEIGHT):
    for col in range(GRID_WIDTH):
        if (row, col) == Start_pos or (row, col) == End_pos:
            continue
        if random.random() < OBSTACLE_DENSITY:
            true_grid[row][col] = 1 
def draw_grid(surface, drone, known_grid):
    """Draws the world from the drone's perspective."""
    fog_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    fog_surface.fill((0,0,0,255)) 
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(surface, bili, rect, 1)
            if known_grid[row][col] != -1:
                pygame.draw.rect(fog_surface, (0,0,0,0), rect)
                if known_grid[row][col] == 1:
                    pygame.draw.rect(surface, red, rect)
    if drone.path:
        for pos in drone.path:
            rect = pygame.Rect(pos[1] * TILE_SIZE, pos[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(surface, OPEN_SET_COLOR, rect, 2)
    surface.blit(fog_surface, (0,0))
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    running=True
    clock=pygame.time.Clock()
    CHANGE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(CHANGE_EVENT, 10000)
    all_sprites = pygame.sprite.Group()
    drone = Drone(Start_pos, TILE_SIZE, GRID_WIDTH, GRID_HEIGHT)
    all_sprites.add(drone)
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type == CHANGE_EVENT:
                print("--- World state is changing! ---")
                generate_obstacles(true_grid, 0.2)
                true_grid[Start_pos[0]][Start_pos[1]] = 0
                true_grid[End_pos[0]][End_pos[1]] = 0
        drone.update(true_grid, known_grid, End_pos)
        all_sprites.update(true_grid, known_grid, End_pos)
        screen.fill(gray)
        draw_grid(screen, drone, known_grid)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
if __name__=="__main__":
    main()