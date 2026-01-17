import pygame
import random
import math
from database import GameDB
from models import Player, Item, Enemy, Bullet
from config import *
from menu import Menu
from sprite_loader import init_sprites, AnimatedMageSprite, get_background
from renderer import GameRenderer


class GameApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Top Down Survival Shooter")
        self.clock = pygame.time.Clock()
        
        init_sprites(WIDTH, HEIGHT)
        
        self.renderer = GameRenderer(self.screen)
        self.font = self.renderer.font
        self.title_font = self.renderer.title_font
        
        self.db = GameDB()
        self.state = "MENU"
        
        self.player_name = "lk"
        self.player = None
        
        self.menu = Menu(self)

        self.enemies = []
        self.bullets = []
        self.dropped_items = []
        self.spawn_timer = 0
        
        self.player_sprite = AnimatedMageSprite(scale=4.0)
        self.last_shot = False
        self.player_dx = 0
        self.player_dy = 0
        
        self.countdown_val = 3
        self.last_count_tick = 0

    def save_game_state(self):
        if self.player:
            del self.player.saved_enemies[:]
            del self.player.saved_bullets[:]
            del self.player.saved_items[:]
            
            for e in self.enemies:
                self.player.saved_enemies.append(e)
            for b in self.bullets:
                self.player.saved_bullets.append(b)
            for it in self.dropped_items:
                self.player.saved_items.append(it)
                
            self.db.save()

    def load_player(self, name=None):
        if name:
            self.player_name = name
            
        if self.player_name not in self.db.root['players']:
            self.db.root['players'][self.player_name] = Player(self.player_name)
            self.db.save()
        
        self.player = self.db.root['players'][self.player_name]
        
        self.db.root['world_state']['last_played'] = self.player_name
        self.db.save()
        
        if self.player.status == "Defeated":
            self.player.reset()
            self.enemies, self.bullets, self.dropped_items = [], [], []
        else:
            self.enemies = list(self.player.saved_enemies)
            self.bullets = list(self.player.saved_bullets)
            self.dropped_items = list(self.player.saved_items)

    def start_countdown(self):
        self.state = "COUNTDOWN"
        self.countdown_val = 3
        self.last_count_tick = pygame.time.get_ticks()

    def format_time(self, seconds):
        mins = int(seconds) // 60
        secs = int(seconds) % 60
        return f"{mins:02}:{secs:02}"

    def handle_countdown(self, events):
        self.renderer.draw_background(get_background())
        if not self.player:
            self.state = "MENU"
            return
        time_str = self.format_time(self.player.time_survived)
        self.renderer.draw_game_world(
            self.bullets, self.enemies, self.dropped_items,
            self.player, self.player_sprite, time_str
        )
        
        now = pygame.time.get_ticks()
        if now - self.last_count_tick >= 1000:
            self.countdown_val -= 1
            self.last_count_tick = now
            if self.countdown_val <= 0:
                self.state = "GAME"
                return
        
        self.renderer.draw_countdown_overlay(self.countdown_val)

    def handle_game(self, events):
        if not self.player:
            self.state = "MENU"
            return
        dt = self.clock.get_time() / 1000.0
        self.renderer.draw_background(get_background())
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.save_game_state()
                    self.state = "MENU"
            if event.type == pygame.MOUSEBUTTONDOWN and self.player.status == "Active":
                mx, my = pygame.mouse.get_pos()
                self.bullets.append(Bullet(self.player.x + 20, self.player.y + 20, mx, my))
                self.last_shot = True

        if self.player.status == "Active":
            self.player.update_time(dt)
            difficulty = 1.0 + (self.player.time_survived / 60.0)
            
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[pygame.K_a]: dx = -5
            if keys[pygame.K_d]: dx = 5
            if keys[pygame.K_w]: dy = -5
            if keys[pygame.K_s]: dy = 5
            if dx != 0 or dy != 0: self.player.move(dx, dy)
            
            self.player_dx = dx
            self.player_dy = dy
            
            mx, my = pygame.mouse.get_pos()
            self.player_sprite.update(
                dt, dx, dy,
                is_shooting=self.last_shot,
                mouse_x=mx, mouse_y=my,
                player_x=self.player.x + 20, player_y=self.player.y + 20
            )
            self.last_shot = False

            spawn_rate = max(20, 60 - int(difficulty * 5))
            self.spawn_timer += 1
            if self.spawn_timer > spawn_rate:
                self.enemies.append(Enemy(difficulty))
                self.spawn_timer = 0

            grid_size = 100
            enemy_grid = {}
            for e in self.enemies:
                gx = int(e.x // grid_size)
                gy = int(e.y // grid_size)
                if (gx, gy) not in enemy_grid:
                    enemy_grid[(gx, gy)] = []
                enemy_grid[(gx, gy)].append(e)

            for b in self.bullets[:]:
                b.move()
                if b.x < 0 or b.x > WIDTH or b.y < 0 or b.y > HEIGHT:
                    self.bullets.remove(b)
                    continue
                
                bgx = int(b.x // grid_size)
                bgy = int(b.y // grid_size)
                
                found_hit = False
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if found_hit: break
                        cell_enemies = enemy_grid.get((bgx + dx, bgy + dy), [])
                        for e in cell_enemies:
                            if math.hypot(b.x - e.x, b.y - e.y) < 20:
                                if random.random() < 0.4:
                                    new_item = Item("Drop_score", 'score', 50)
                                    new_item.x, new_item.y = e.x, e.y
                                    self.dropped_items.append(new_item)
                                
                                if e in self.enemies: 
                                    self.enemies.remove(e)
                                    egx, egy = int(e.x // grid_size), int(e.y // grid_size)
                                    if e in enemy_grid.get((egx, egy), []):
                                         enemy_grid[(egx, egy)].remove(e)

                                if b in self.bullets: self.bullets.remove(b)
                                self.player.add_score(10)
                                found_hit = True
                                break

            for e in self.enemies[:]:
                e.move_towards_player(self.player.x + 20, self.player.y + 20)
                e.update(dt)
                if math.hypot(e.x - (self.player.x + 20), e.y - (self.player.y + 20)) < 30:
                    self.player.take_damage(10)
                    if e in self.enemies: self.enemies.remove(e)
                    if self.player.status == "Defeated":
                        self.db.add_high_score(self.player.name, self.player.score, self.player.time_survived)
                        self.state = "GAMEOVER"

            for it in self.dropped_items[:]:
                if math.hypot(it.x - (self.player.x + 20), it.y - (self.player.y + 20)) < 30:
                    self.player.inventory.append(it)
                    self.player.use_item(it)
                    self.dropped_items.remove(it)

        time_str = self.format_time(self.player.time_survived)
        self.renderer.draw_game_world(
            self.bullets, self.enemies, self.dropped_items,
            self.player, self.player_sprite, time_str
        )

    def handle_gameover(self, events):
        time_str = self.format_time(self.player.time_survived)
        self.renderer.draw_gameover(self.player, time_str)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.player.reset()
                    self.enemies, self.bullets, self.dropped_items = [], [], []
                    self.start_countdown()
                elif event.key == pygame.K_ESCAPE:
                    self.state = "MENU"

    def run(self):
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
            
            if self.state == "MENU":
                self.menu.handle_main(events)
            elif self.state == "GAME":
                self.handle_game(events)
            elif self.state == "LEADERBOARD":
                self.menu.handle_leaderboard(events)
            elif self.state == "GAMEOVER":
                self.handle_gameover(events)
            elif self.state == "LOAD_GAME":
                self.menu.handle_load_game(events)
            elif self.state == "COUNTDOWN":
                self.handle_countdown(events)
            elif self.state == "EXIT":
                running = False
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        print("Packing database...")
        self.db.pack()
        self.db.close()
        pygame.quit()


if __name__ == "__main__":
    app = GameApp()
    app.run()