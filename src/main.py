import pygame
import random
import math
import sys
from database import GameDB
from models import Player, Item, Enemy, Bullet

# --- CONFIGURATION ---
WIDTH, HEIGHT = 1024, 768
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
DARK_GRAY = (30, 30, 30)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 50, 200)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

class Button:
    def __init__(self, x, y, w, h, text, action=None, color=BLUE):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action = action
        self.color = color
        self.hover_color = (min(color[0]+50, 255), min(color[1]+50, 255), min(color[2]+50, 255))

    def draw(self, screen, font, small_text=""):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        
        if not small_text:
            text_surf = font.render(self.text, True, WHITE)
            text_rect = text_surf.get_rect(center=self.rect.center)
            screen.blit(text_surf, text_rect)
        else:
            main_surf = font.render(self.text, True, WHITE)
            sub_font = pygame.font.Font(None, 24)
            sub_surf = sub_font.render(small_text, True, (220, 220, 220))
            
            total_h = main_surf.get_height() + sub_surf.get_height() + 5
            screen.blit(main_surf, (self.rect.x + 10, self.rect.centery - total_h//2))
            screen.blit(sub_surf, (self.rect.x + 10, self.rect.centery + total_h//2 - sub_surf.get_height()))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = text
        self.txt_surface = None
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
        return None

    def draw(self, screen, font):
        self.txt_surface = font.render(self.text, True, WHITE)
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

class GameApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("ZODB RPG - Advanced Persistence")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 74)
        self.countdown_font = pygame.font.Font(None, 300)
        
        self.db = GameDB()
        self.state = "MENU" # MENU, GAME, LEADERBOARD, GAMEOVER, LOAD_GAME, COUNTDOWN
        
        self.player_name = "Player1"
        self.player = None
        
        # UI Elements
        self.name_input = InputBox(WIDTH//2 - 100, HEIGHT//2 - 100, 140, 32, self.player_name)
        self.btn_start = Button(WIDTH//2 - 100, HEIGHT//2 - 30, 200, 50, "New Game", color=GREEN)
        self.btn_load_menu = Button(WIDTH//2 - 100, HEIGHT//2 + 40, 200, 50, "Load / Continue", color=BLUE)
        self.btn_leaderboard = Button(WIDTH//2 - 100, HEIGHT//2 + 110, 200, 50, "Leaderboard", color=GRAY)
        self.btn_quit = Button(WIDTH//2 - 100, HEIGHT//2 + 180, 200, 50, "Exit", color=RED)
        self.btn_back = Button(50, HEIGHT - 80, 150, 40, "Back", color=GRAY)

        # Game Objects
        self.enemies = []
        self.bullets = []
        self.dropped_items = []
        self.spawn_timer = 0
        self.load_buttons = []
        
        # Countdown variables
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
        elif self.name_input.text:
            self.player_name = self.name_input.text
            
        if self.player_name not in self.db.root['players']:
            self.db.root['players'][self.player_name] = Player(self.player_name)
            self.db.save()
        
        self.player = self.db.root['players'][self.player_name]
        
        # Save last played player to world state
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

    def handle_menu(self, events):
        self.screen.fill(DARK_GRAY)
        title = self.title_font.render("ZODB RPG", True, WHITE)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        info = self.font.render("Enter name for New Game:", True, WHITE)
        self.screen.blit(info, (WIDTH//2 - info.get_width()//2, HEIGHT//2 - 140))

        for event in events:
            self.name_input.handle_event(event)
            if self.btn_start.is_clicked(event):
                self.load_player()
                self.start_countdown()
            elif self.btn_load_menu.is_clicked(event):
                self.refresh_load_menu()
                self.state = "LOAD_GAME"
            elif self.btn_leaderboard.is_clicked(event):
                self.state = "LEADERBOARD"
            elif self.btn_quit.is_clicked(event):
                self.save_game_state()
                pygame.quit()
                sys.exit()

        self.name_input.draw(self.screen, self.font)
        self.btn_start.draw(self.screen, self.font)
        self.btn_load_menu.draw(self.screen, self.font)
        self.btn_leaderboard.draw(self.screen, self.font)
        self.btn_quit.draw(self.screen, self.font)

    def refresh_load_menu(self):
        active_players = self.db.get_all_active_players()
        last_played = self.db.root['world_state'].get('last_played')
        
        self.load_buttons = []
        start_y = 150
        for i, p in enumerate(active_players):
            display_name = p.name
            if p.name == last_played:
                display_name += " (last played)"
                
            info_str = f"Score: {p.score} | HP: {p.hp} | Time: {self.format_time(p.time_survived)}"
            btn = Button(WIDTH//2 - 250, start_y + i * 70, 500, 60, display_name, color=BLUE)
            self.load_buttons.append((btn, p.name, info_str))

    def handle_load_game(self, events):
        self.screen.fill(BLACK)
        title = self.title_font.render("Continue Adventure", True, CYAN)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))

        if not self.load_buttons:
            empty_msg = self.font.render("No active saved games found.", True, GRAY)
            self.screen.blit(empty_msg, (WIDTH//2 - empty_msg.get_width()//2, HEIGHT//2))

        for event in events:
            if self.btn_back.is_clicked(event):
                self.state = "MENU"
            for btn, name, info in self.load_buttons:
                if btn.is_clicked(event):
                    self.load_player(name)
                    self.start_countdown()

        for btn, name, info in self.load_buttons:
            btn.draw(self.screen, self.font, small_text=info)

        self.btn_back.draw(self.screen, self.font)

    def handle_leaderboard(self, events):
        self.screen.fill(BLACK)
        title = self.title_font.render("Leaderboard (ZODB)", True, YELLOW)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        
        header = self.font.render("Rank   Name         Score    Time", True, (200, 200, 200))
        self.screen.blit(header, (WIDTH//2 - 250, 120))
        pygame.draw.line(self.screen, WHITE, (WIDTH//2 - 260, 150), (WIDTH//2 + 260, 150), 2)

        top_scores = self.db.get_top_scores(10)
        start_y = 170
        for i, (name, score, time_val) in enumerate(top_scores):
            time_str = self.format_time(time_val)
            text_str = f"{i+1:<5}  {name:<12} {score:<8} {time_str}"
            text = self.font.render(text_str, True, WHITE)
            self.screen.blit(text, (WIDTH//2 - 250, start_y + i * 40))

        for event in events:
            if self.btn_back.is_clicked(event):
                self.state = "MENU"

        self.btn_back.draw(self.screen, self.font)

    def draw_game_world(self):
        for b in self.bullets: b.draw(self.screen)
        for e in self.enemies: e.draw(self.screen)
        for it in self.dropped_items:
            pygame.draw.rect(self.screen, YELLOW, (it.x, it.y, 15, 15))

        color = GREEN if self.player.status == "Active" else GRAY
        pygame.draw.rect(self.screen, color, (self.player.x, self.player.y, 40, 40))

        time_str = self.format_time(self.player.time_survived)
        name_surf = self.font.render(f"Player: {self.player.name}", True, CYAN)
        self.screen.blit(name_surf, (20, 20))
        
        ui_text = f"HP: {self.player.hp} | Score: {self.player.score} | Time: {time_str} | Multi: x{self.player.multiplier:.1f}"
        self.screen.blit(self.font.render(ui_text, True, WHITE), (20, 50))
        
        diff_text = f"Difficulty: {1.0 + (self.player.time_survived/60.0):.1f}x"
        self.screen.blit(self.font.render(diff_text, True, RED), (WIDTH - 220, 20))

        controls_text = "WASD: Move | MOUSE: Shoot | ESC: Menu"
        controls_surf = pygame.font.Font(None, 24).render(controls_text, True, (200, 200, 200))
        self.screen.blit(controls_surf, (WIDTH - controls_surf.get_width() - 20, HEIGHT - 30))

    def handle_countdown(self, events):
        self.screen.fill(GRAY)
        self.draw_game_world()
        
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0,0))
        
        now = pygame.time.get_ticks()
        if now - self.last_count_tick >= 1000:
            self.countdown_val -= 1
            self.last_count_tick = now
            if self.countdown_val <= 0:
                self.state = "GAME"
                return

        count_text = str(self.countdown_val)
        count_surf = self.countdown_font.render(count_text, True, YELLOW)
        rect = count_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.screen.blit(count_surf, rect)

    def handle_game(self, events):
        dt = self.clock.get_time() / 1000.0
        self.screen.fill(GRAY)
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.save_game_state()
                    self.state = "MENU"
            if event.type == pygame.MOUSEBUTTONDOWN and self.player.status == "Active":
                mx, my = pygame.mouse.get_pos()
                self.bullets.append(Bullet(self.player.x + 20, self.player.y + 20, mx, my))

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

            spawn_rate = max(20, 60 - int(difficulty * 5))
            self.spawn_timer += 1
            if self.spawn_timer > spawn_rate:
                self.enemies.append(Enemy(difficulty))
                self.spawn_timer = 0

            for b in self.bullets[:]:
                b.move()
                if b.x < 0 or b.x > WIDTH or b.y < 0 or b.y > HEIGHT:
                    self.bullets.remove(b)
                    continue
                for e in self.enemies[:]:
                    if math.hypot(b.x - e.x, b.y - e.y) < 20:
                        if random.random() < 0.4:
                            item_type = 'score'
                            val = 50
                            new_item = Item(f"Drop_{item_type}", item_type, val)
                            new_item.x, new_item.y = e.x, e.y
                            self.dropped_items.append(new_item)
                        if e in self.enemies: self.enemies.remove(e)
                        if b in self.bullets: self.bullets.remove(b)
                        self.player.add_score(10)
                        break

            for e in self.enemies[:]:
                e.move_towards_player(self.player.x + 20, self.player.y + 20)
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

        self.draw_game_world()

    def handle_gameover(self, events):
        self.screen.fill((50, 0, 0))
        msg = self.title_font.render("GAME OVER", True, RED)
        self.screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 120))
        stats = f"Score: {self.player.score} | Time: {self.format_time(self.player.time_survived)}"
        score_msg = self.font.render(stats, True, WHITE)
        self.screen.blit(score_msg, (WIDTH//2 - score_msg.get_width()//2, HEIGHT//2 - 40))
        restart_msg = self.font.render("Press R to Restart or ESC for Menu", True, (200, 200, 200))
        self.screen.blit(restart_msg, (WIDTH//2 - restart_msg.get_width()//2, HEIGHT//2 + 40))

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
                self.handle_menu(events)
            elif self.state == "GAME":
                self.handle_game(events)
            elif self.state == "LEADERBOARD":
                self.handle_leaderboard(events)
            elif self.state == "GAMEOVER":
                self.handle_gameover(events)
            elif self.state == "LOAD_GAME":
                self.handle_load_game(events)
            elif self.state == "COUNTDOWN":
                self.handle_countdown(events)
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        self.db.close()
        pygame.quit()

if __name__ == "__main__":
    app = GameApp()
    app.run()