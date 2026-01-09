import pygame
import math
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPRITESHEET_DIR = os.path.join(BASE_DIR, 'spritesheet')


class SpriteSheet:
    _cache = {}
    
    def __init__(self, filename, columns, rows):
        self.filename = filename
        self.columns = columns
        self.rows = rows
        self.sheet = None
        self.cell_width = 0
        self.cell_height = 0
    
    def load(self):
        if self.sheet is not None:
            return
        path = os.path.join(SPRITESHEET_DIR, self.filename)
        self.sheet = pygame.image.load(path).convert_alpha()
        self.cell_width = self.sheet.get_width() // self.columns
        self.cell_height = self.sheet.get_height() // self.rows
        print(f"[Sprite] {self.filename}: {self.cell_width}x{self.cell_height} ćelija")
    
    def get_sprite(self, col, row, scale=1.0):
        cache_key = (self.filename, col, row, scale)
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        image = pygame.Surface((self.cell_width, self.cell_height), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), 
                   (col * self.cell_width, row * self.cell_height,
                    self.cell_width, self.cell_height))
        
        if scale != 1.0:
            new_size = (int(self.cell_width * scale), int(self.cell_height * scale))
            image = pygame.transform.scale(image, new_size)
        
        self._cache[cache_key] = image
        return image
    
    def get_frames(self, start_col, row, count, scale=1.0):
        return [self.get_sprite(start_col + i, row, scale) for i in range(count)]


ant_sheet = SpriteSheet('Ants.png', 12, 8)
mage_sheet = SpriteSheet('Mage-Cyan.png', 24, 8)
background_image = None


def init_sprites(screen_width=1024, screen_height=768):
    global background_image
    ant_sheet.load()
    mage_sheet.load()
    
    bg_path = os.path.join(SPRITESHEET_DIR, 'bg.jpg')
    if os.path.exists(bg_path):
        background_image = pygame.image.load(bg_path).convert()
        background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
        print(f"[Sprite] Učitan background: {screen_width}x{screen_height}")


def get_background():
    return background_image


ANT_COLORS = {'brown': 0, 'red': 3, 'green': 6, 'black': 9}


class AnimatedAntSprite:
    def __init__(self, color='red', scale=1.0):
        self.color = color
        self.scale = scale
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.15
        self.rotation_angle = 0
        self.is_dead = False
        
        start_col = ANT_COLORS.get(color, 0)
        self._frames = ant_sheet.get_frames(start_col, 0, 3, scale)
        self._rotated_cache = {}
    
    def _get_rotated(self, frame_idx, angle):
        angle = round(angle / 15) * 15 % 360
        key = (frame_idx, angle)
        if key not in self._rotated_cache:
            if angle == 0:
                self._rotated_cache[key] = self._frames[frame_idx]
            else:
                self._rotated_cache[key] = pygame.transform.rotate(self._frames[frame_idx], angle)
        return self._rotated_cache[key]
    
    def update(self, dt, dx=0, dy=0):
        if self.is_dead:
            return
        if dx != 0 or dy != 0:
            angle = math.degrees(math.atan2(dy, dx))
            self.rotation_angle = -angle - 90 + 180
        
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % 3
    
    def get_current_frame(self):
        if self.is_dead:
            return self._get_rotated(0, 90)
        return self._get_rotated(self.current_frame, self.rotation_angle)


MAGE_DIRECTIONS = {'down': 0, 'right': 2, 'up': 4, 'left': 6}
MAGE_ACTIONS = {'walk': (0, 4), 'magic': (12, 4)}


class AnimatedMageSprite:
    def __init__(self, scale=3.0):
        self.scale = scale
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.12
        self.current_direction = 'down'
        self.current_action = 'walk'
        self.is_attacking = False
        self.attack_timer = 0
        
        self._animations = {}
        for action, (start_col, count) in MAGE_ACTIONS.items():
            self._animations[action] = {}
            for direction, row in MAGE_DIRECTIONS.items():
                self._animations[action][direction] = mage_sheet.get_frames(start_col, row, count, scale)
    
    def _angle_to_direction(self, angle):
        angle = angle % 360
        if 315 <= angle or angle < 45:
            return 'right'
        elif 45 <= angle < 135:
            return 'down'
        elif 135 <= angle < 225:
            return 'left'
        return 'up'
    
    def update(self, dt, dx=0, dy=0, is_shooting=False, mouse_x=0, mouse_y=0, player_x=0, player_y=0):
        if is_shooting:
            angle = math.degrees(math.atan2(mouse_y - player_y, mouse_x - player_x))
            self.current_direction = self._angle_to_direction(angle)
            self.current_action = 'magic'
            self.is_attacking = True
            self.attack_timer = 0.4
        elif dx != 0 or dy != 0:
            angle = math.degrees(math.atan2(dy, dx))
            self.current_direction = self._angle_to_direction(angle)
            if not self.is_attacking:
                self.current_action = 'walk'
        
        if self.is_attacking:
            self.attack_timer -= dt
            if self.attack_timer <= 0:
                self.is_attacking = False
                self.current_action = 'walk'
        
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            frames = self._animations[self.current_action][self.current_direction]
            self.current_frame = (self.current_frame + 1) % len(frames)
    
    def get_current_frame(self):
        frames = self._animations[self.current_action][self.current_direction]
        return frames[self.current_frame % len(frames)]
