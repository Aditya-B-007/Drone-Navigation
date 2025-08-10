import pygame
from pathfinding_logic import Searcher as astar_find_path
class Drone(pygame.sprite.Sprite):
    def __init__(self, pos, tile_size, grid_w, grid_h):
        super().__init__()
        self.image = pygame.Surface([tile_size - 4, tile_size - 4])
        self.image.fill(pygame.Color('dodgerblue'))
        self.rect = self.image.get_rect()
        self.tile_size = tile_size
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.path = []
        self.target_index = 0
        self.target_node = None
        start_x = pos[1] * tile_size + tile_size / 2
        start_y = pos[0] * tile_size + tile_size / 2
        self.pos = pygame.math.Vector2(start_x, start_y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.max_speed = 3
        self.max_force = 0.2
        self.sensor_radius = 8
    def set_path(self, path):
        if path:
            self.path = path
            self.target_index = 0
            self._update_target_node()
        else:
            self.path = []
            self.target_node = None
    def _update_target_node(self):
        if self.path and self.target_index < len(self.path):
            grid_pos = self.path[self.target_index]
            target_x = grid_pos[1] * self.tile_size + self.tile_size / 2
            target_y = grid_pos[0] * self.tile_size + self.tile_size / 2
            self.target_node = pygame.math.Vector2(target_x, target_y)
        else:
            self.target_node = None
            self.path = []
    def apply_force(self, force):
        self.acc += force
    def seek(self, target):
        if target:
            desired = target - self.pos
            dist = desired.length()
            if dist < 100:
                speed = (dist / 100) * self.max_speed
            else:
                speed = self.max_speed
            if desired.length() > 0:
                desired.scale_to_length(speed)
            steer = desired - self.vel
            if steer.length() > self.max_force:
                steer.scale_to_length(self.max_force)
            self.apply_force(steer)
    def scan_environment(self, true_grid, known_grid):
        center_r, center_c = int(self.pos.y / self.tile_size), int(self.pos.x / self.tile_size)
        
        for r_offset in range(-self.sensor_radius, self.sensor_radius + 1):
            for c_offset in range(-self.sensor_radius, self.sensor_radius + 1):
                r, c = center_r + r_offset, center_c + c_offset
                
                if 0 <= r < self.grid_h and 0 <= c < self.grid_w:
                    if r_offset**2 + c_offset**2 <= self.sensor_radius**2:
                        known_grid[r][c] = true_grid[r][c]
                        
    def is_path_valid(self, known_grid):
        if not self.path:
            return True
        for pos in self.path:
            if known_grid[pos[0]][pos[1]] == 1:
                return False
        return True

    def update(self, true_grid, known_grid, end_pos):
        self.scan_environment(true_grid, known_grid)

        if not self.is_path_valid(known_grid) or (not self.path and self.vel.length() < 0.1):
            current_grid_pos = (int(self.pos.y / self.tile_size), int(self.pos.x / self.tile_size))
            
            if current_grid_pos != end_pos:
                print("Path invalid or finished. Re-planning...")
                new_path = astar_find_path(known_grid, current_grid_pos, end_pos)
                self.set_path(new_path)

        if self.target_node:
            self.seek(self.target_node)
            if self.pos.distance_to(self.target_node) < self.tile_size / 2:
                self.target_index += 1
                self._update_target_node()
        else:
            self.vel *= 0.95 

        self.vel += self.acc
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)
            
        self.pos += self.vel
        self.acc *= 0

        self.rect.center = self.pos