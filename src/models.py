import pygame
import random
import math
from persistent import Persistent
from persistent.list import PersistentList
from config import WIDTH, HEIGHT
from sprite_loader import AnimatedAntSprite

class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.x, self.y = x, y
        self.speed = 10
        angle = math.atan2(target_y - y, target_x - x)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), 5)


class Enemy:
    COLORS = ['brown', 'red', 'green', 'black']
    
    def __init__(self, difficulty_multiplier=1.0, color=None):
        side = random.randint(0, 3)
        positions = [
            (random.randint(0, WIDTH), -50),
            (random.randint(0, WIDTH), HEIGHT + 50),
            (-50, random.randint(0, HEIGHT)),
            (WIDTH + 50, random.randint(0, HEIGHT))
        ]
        self.x, self.y = positions[side]
        self.speed = random.uniform(1, 2.5) * difficulty_multiplier
        self.color = color or random.choice(self.COLORS)
        self.last_dx, self.last_dy = 0, 0
        self.hp = 1
        self._init_sprite()
    
    def _init_sprite(self):
        self.sprite = AnimatedAntSprite(color=self.color, scale=1)
    
    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop('sprite', None)
        return state
    
    def __setstate__(self, state):
        self.__dict__.update(state)
        self._init_sprite()

    def move_towards_player(self, player_x, player_y):
        angle = math.atan2(player_y - self.y, player_x - self.x)
        self.last_dx = math.cos(angle) * self.speed
        self.last_dy = math.sin(angle) * self.speed
        self.x += self.last_dx
        self.y += self.last_dy

    def update(self, dt):
        if not hasattr(self, 'sprite'):
            self._init_sprite()
        self.sprite.update(dt, self.last_dx, self.last_dy)

    def draw(self, screen):
        if not hasattr(self, 'sprite'):
            self._init_sprite()
        frame = self.sprite.get_current_frame()
        rect = frame.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(frame, rect)


class Item:
    def __init__(self, name, item_type, value):
        self.name = name
        self.item_type = item_type
        self.value = value
        self.x, self.y = 0, 0


class Player(Persistent):
    def __init__(self, name):
        self.name = name
        self._hp = 100
        self.x, self.y = 400, 300
        self.score = 0
        self.multiplier = 1.0
        self.time_survived = 0.0
        self.inventory = PersistentList()
        self.saved_enemies = PersistentList()
        self.saved_bullets = PersistentList()
        self.saved_items = PersistentList()
        self.status = "Active"

    def update_time(self, dt):
        self.time_survived += dt
        self._p_changed = True

    def move(self, dx, dy):
        self.x = max(0, min(self.x + dx, WIDTH - 40))
        self.y = max(0, min(self.y + dy, HEIGHT - 40))
        self._p_changed = True

    def reset(self):
        self._hp = 100
        self.x, self.y = 400, 300
        self.score = 0
        self.multiplier = 1.0
        self.time_survived = 0.0
        self.inventory = PersistentList()
        self.saved_enemies = PersistentList()
        self.saved_bullets = PersistentList()
        self.saved_items = PersistentList()
        self.status = "Active"
        self._p_changed = True

    def use_item(self, item):
        if item.item_type == 'heal':
            self.hp += item.value
        elif item.item_type == 'score':
            self.add_score(item.value)
            self.multiplier += 0.1
        self._p_changed = True

    def take_damage(self, amount):
        self.hp -= amount

    def add_score(self, points):
        self.score += int(points * self.multiplier)
        self._p_changed = True

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = min(100, max(0, value))
        if self._hp == 0:
            self.status = "Defeated"
        self._p_changed = True