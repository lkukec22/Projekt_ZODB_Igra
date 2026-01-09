import pygame
import math
from config import WIDTH, HEIGHT, WHITE, RED, CYAN, GRAY


class GameRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 74)
        self.countdown_font = pygame.font.Font(None, 300)
        self.controls_font = pygame.font.Font(None, 24)
    
    def draw_background(self, background_image):
        if background_image:
            self.screen.blit(background_image, (0, 0))
        else:
            self.screen.fill(GRAY)
    
    def draw_bullets(self, bullets):
        for b in bullets:
            b.draw(self.screen)
    
    def draw_enemies(self, enemies):
        for e in enemies:
            e.draw(self.screen)
    
    def draw_item(self, item):
        time_ms = pygame.time.get_ticks()
        pulse = math.sin(time_ms / 200) * 2
        size = int(12 + pulse)
        
        cx, cy = int(item.x) + 8, int(item.y) + 8
        gem_points = [
            (cx, cy - size),
            (cx + size, cy),
            (cx, cy + size),
            (cx - size, cy)
        ]
        pygame.draw.polygon(self.screen, (0, 100, 200), gem_points)
        
        inner_size = size - 3
        inner_points = [
            (cx, cy - inner_size),
            (cx + inner_size, cy),
            (cx, cy + inner_size),
            (cx - inner_size, cy)
        ]
        pygame.draw.polygon(self.screen, (80, 180, 255), inner_points)
        pygame.draw.line(self.screen, (255, 255, 255), (cx - 3, cy - 4), (cx, cy - size + 3), 2)
    
    def draw_dropped_items(self, dropped_items):
        for item in dropped_items:
            self.draw_item(item)
    
    def draw_player(self, player, player_sprite):
        if player.status == "Active":
            player_frame = player_sprite.get_current_frame()
            frame_rect = player_frame.get_rect(center=(player.x + 20, player.y + 20))
            self.screen.blit(player_frame, frame_rect)
        else:
            pygame.draw.rect(self.screen, GRAY, (player.x, player.y, 40, 40))
    
    def draw_hud(self, player, time_str):
        name_surf = self.font.render(f"Player: {player.name}", True, CYAN)
        self.screen.blit(name_surf, (20, 20))
        
        ui_text = f"HP: {player.hp} | Score: {player.score} | Time: {time_str} | Multi: x{player.multiplier:.1f}"
        self.screen.blit(self.font.render(ui_text, True, WHITE), (20, 50))
        
        difficulty = 1.0 + (player.time_survived / 60.0)
        diff_text = f"Difficulty: {difficulty:.1f}x"
        self.screen.blit(self.font.render(diff_text, True, RED), (WIDTH - 220, 20))
        
        controls_text = "WASD: Move | MOUSE: Shoot | ESC: Menu"
        controls_surf = self.controls_font.render(controls_text, True, (200, 200, 200))
        self.screen.blit(controls_surf, (WIDTH - controls_surf.get_width() - 20, HEIGHT - 30))
    
    def draw_game_world(self, bullets, enemies, dropped_items, player, player_sprite, time_str):
        self.draw_bullets(bullets)
        self.draw_enemies(enemies)
        self.draw_dropped_items(dropped_items)
        self.draw_player(player, player_sprite)
        self.draw_hud(player, time_str)
    
    def draw_countdown_overlay(self, countdown_val):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        count_surf = self.countdown_font.render(str(countdown_val), True, (255, 255, 0))
        rect = count_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(count_surf, rect)
    
    def draw_gameover(self, player, time_str):
        self.screen.fill((50, 0, 0))
        
        msg = self.title_font.render("GAME OVER", True, RED)
        self.screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 120))
        
        stats = f"Score: {player.score} | Time: {time_str}"
        score_msg = self.font.render(stats, True, WHITE)
        self.screen.blit(score_msg, (WIDTH // 2 - score_msg.get_width() // 2, HEIGHT // 2 - 40))
        
        restart_msg = self.font.render("Press R to Restart or ESC for Menu", True, (200, 200, 200))
        self.screen.blit(restart_msg, (WIDTH // 2 - restart_msg.get_width() // 2, HEIGHT // 2 + 40))
