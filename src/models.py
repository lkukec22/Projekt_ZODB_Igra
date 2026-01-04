import pygame
import random
import math
from persistent import Persistent
from persistent.list import PersistentList
from config import WIDTH, HEIGHT

class Bullet(Persistent):
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.speed = 10
        angle = math.atan2(target_y - y, target_x - x)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self._p_changed = True

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), 5)

class Enemy(Persistent):
    def __init__(self, difficulty_multiplier=1.0):
        side = random.randint(0, 3)
        if side == 0: self.x, self.y = random.randint(0, WIDTH), -50
        elif side == 1: self.x, self.y = random.randint(0, WIDTH), HEIGHT + 50
        elif side == 2: self.x, self.y = -50, random.randint(0, HEIGHT)
        else: self.x, self.y = WIDTH + 50, random.randint(0, HEIGHT)
        
        base_speed = random.uniform(1, 2.5)
        self.speed = base_speed * difficulty_multiplier

    def move_towards_player(self, player_x, player_y):
        angle = math.atan2(player_y - self.y, player_x - self.x)
        self.x += math.cos(angle) * self.speed
        self.y += math.sin(angle) * self.speed
        self._p_changed = True

    def draw(self, screen):
        pygame.draw.circle(screen, (200, 50, 50), (int(self.x), int(self.y)), 15)

class Item(Persistent):
    def __init__(self, name, item_type, value):
        self.name = name
        self.item_type = item_type # 'heal' or 'score'
        self.value = value
        self.x = 0
        self.y = 0

class Player(Persistent):
    def __init__(self, name):
        self.name = name
        self._hp = 100
        self.x = 400
        self.y = 300
        self.score = 0
        self.multiplier = 1.0
        self.time_survived = 0.0
        self.inventory = PersistentList()
        self.saved_enemies = PersistentList()
        self.saved_bullets = PersistentList()
        self.saved_items = PersistentList()
        self.status = "Active"

    def update_time(self, dt):
        """Updates survival time (in seconds)"""
        self.time_survived += dt
        self._p_changed = True

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.x = max(0, min(self.x, WIDTH - 40)) 
        self.y = max(0, min(self.y, HEIGHT - 40)) 
        self._p_changed = True

    def reset(self):
        self._hp = 100
        self.x = 400
        self.y = 300
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