import pygame
import random
import math
from database import GameDB
from models import Player

class Bullet:
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

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), 5)

class Enemy:
    def __init__(self):
        # Spawn izvan ekrana
        side = random.randint(0, 3)
        if side == 0: # Top
            self.x = random.randint(0, 800)
            self.y = -50
        elif side == 1: # Bottom
            self.x = random.randint(0, 800)
            self.y = 650
        elif side == 2: # Left
            self.x = -50
            self.y = random.randint(0, 600)
        else: # Right
            self.x = 850
            self.y = random.randint(0, 600)
        
        self.speed = random.uniform(1, 2.5)

    def move_towards_player(self, player_x, player_y):
        angle = math.atan2(player_y - self.y, player_x - self.x)
        self.x += math.cos(angle) * self.speed
        self.y += math.sin(angle) * self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), 15)

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("ZODB RPG Projekt - Survival")
    
    db = GameDB()
    # Dohvati ili kreiraj igrača
    player_name = "Igrac1"
    if player_name not in db.root['players']:
        db.root['players'][player_name] = Player(player_name)
        db.save()
    
    player = db.root['players'][player_name]
    clock = pygame.time.Clock()

    enemies = []
    bullets = []
    spawn_timer = 0

    running = True
    while running:
        screen.fill((50, 50, 50))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                db.save()
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    db.save()
                    running = False
                if event.key == pygame.K_r and player.status == "Poražen":
                    player.reset()
                    enemies = []
                    bullets = []
            
            if event.type == pygame.MOUSEBUTTONDOWN and player.status == "Aktivan":
                mx, my = pygame.mouse.get_pos()
                bullets.append(Bullet(player.x + 20, player.y + 20, mx, my))

        if player.status == "Aktivan":
            # Kretanje (WASD)
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[pygame.K_a]: dx = -5
            if keys[pygame.K_d]: dx = 5
            if keys[pygame.K_w]: dy = -5
            if keys[pygame.K_s]: dy = 5
            if dx != 0 or dy != 0:
                player.move(dx, dy)

            # Spawning neprijatelja
            spawn_timer += 1
            if spawn_timer > 60: # Svake sekunde
                enemies.append(Enemy())
                spawn_timer = 0

            # Update metaka
            for b in bullets[:]:
                b.move()
                if b.x < 0 or b.x > 800 or b.y < 0 or b.y > 600:
                    bullets.remove(b)
                    continue
                
                # Collision s neprijateljima
                for e in enemies[:]:
                    dist = math.hypot(b.x - e.x, b.y - e.y)
                    if dist < 20:
                        if e in enemies: enemies.remove(e)
                        if b in bullets: bullets.remove(b)
                        player.add_score(10)
                        break

            # Update neprijatelja
            for e in enemies[:]:
                e.move_towards_player(player.x + 20, player.y + 20)
                
                # Collision s igračem
                dist = math.hypot(e.x - (player.x + 20), e.y - (player.y + 20))
                if dist < 30:
                    player.take_damage(10)
                    enemies.remove(e)

        # Crtanje metaka
        for b in bullets:
            b.draw(screen)

        # Crtanje neprijatelja
        for e in enemies:
            e.draw(screen)

        # Nacrtaj igrača
        color = (0, 255, 0) if player.status == "Aktivan" else (100, 100, 100)
        pygame.draw.rect(screen, color, (player.x, player.y, 40, 40))
        
        # UI
        font = pygame.font.SysFont(None, 36)
        ui_text = f"HP: {player.hp} | Score: {player.score} | Status: {player.status}"
        img = font.render(ui_text, True, (255, 255, 255))
        screen.blit(img, (20, 20))

        if player.status == "Poražen":
            over_font = pygame.font.SysFont(None, 72)
            over_img = over_font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(over_img, (250, 250))
            retry_img = font.render("Pritisni R za Restart", True, (200, 200, 200))
            screen.blit(retry_img, (280, 320))

        # Upute
        small_font = pygame.font.SysFont(None, 24)
        instr = small_font.render("WASD = Kretanje | MOUSE = Pucanje | X = Spremi i izađi", True, (200, 200, 200))
        screen.blit(instr, (20, 560))

        pygame.display.flip()
        clock.tick(60)

    db.close()
    pygame.quit()

if __name__ == "__main__":
    run_game()
