import pygame
import random
import math
from database import GameDB
from models import Player, Item

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
        side = random.randint(0, 3)
        if side == 0: self.x, self.y = random.randint(0, 800), -50
        elif side == 1: self.x, self.y = random.randint(0, 800), 650
        elif side == 2: self.x, self.y = -50, random.randint(0, 600)
        else: self.x, self.y = 850, random.randint(0, 600)
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
    pygame.display.set_caption("ZODB RPG Projekt - Advanced Persistence")
    
    db = GameDB()
    player_name = "Igrac1"
    if player_name not in db.root['players']:
        db.root['players'][player_name] = Player(player_name)
        db.save()
    
    player = db.root['players'][player_name]
    clock = pygame.time.Clock()

    # ZODB Query: Top Scores
    top_scores = db.get_top_scores()
    print(f"Top rezultati iz baze: {top_scores}")

    enemies = []
    bullets = []
    dropped_items = [] # Lista Item objekata (Persistent)
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
                    enemies, bullets, dropped_items = [], [], []
            
            if event.type == pygame.MOUSEBUTTONDOWN and player.status == "Aktivan":
                mx, my = pygame.mouse.get_pos()
                bullets.append(Bullet(player.x + 20, player.y + 20, mx, my))

        if player.status == "Aktivan":
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[pygame.K_a]: dx = -5
            if keys[pygame.K_d]: dx = 5
            if keys[pygame.K_w]: dy = -5
            if keys[pygame.K_s]: dy = 5
            if dx != 0 or dy != 0: player.move(dx, dy)

            spawn_timer += 1
            if spawn_timer > 60:
                enemies.append(Enemy())
                spawn_timer = 0

            # Update metaka i sudari
            for b in bullets[:]:
                b.move()
                if b.x < 0 or b.x > 800 or b.y < 0 or b.y > 600:
                    bullets.remove(b)
                    continue
                
                for e in enemies[:]:
                    if math.hypot(b.x - e.x, b.y - e.y) < 20:
                        # Nasumični drop predmeta (ZODB Reference)
                        if random.random() < 0.3:
                            item_type = random.choice(['heal', 'score'])
                            val = 20 if item_type == 'heal' else 50
                            new_item = Item(f"Drop_{item_type}", item_type, val)
                            new_item.x, new_item.y = e.x, e.y
                            dropped_items.append(new_item)
                        
                        if e in enemies: enemies.remove(e)
                        if b in bullets: bullets.remove(b)
                        player.add_score(10)
                        break

            # Update neprijatelja
            for e in enemies[:]:
                e.move_towards_player(player.x + 20, player.y + 20)
                if math.hypot(e.x - (player.x + 20), e.y - (player.y + 20)) < 30:
                    player.take_damage(10)
                    enemies.remove(e)
                    if player.status == "Poražen":
                        db.add_high_score(player.name, player.score)

            # Skupljanje predmeta (ZODB Object Graph)
            for it in dropped_items[:]:
                if math.hypot(it.x - (player.x + 20), it.y - (player.y + 20)) < 30:
                    player.inventory.append(it) # Dodajemo Persistent objekt u PersistentList
                    player.use_item(it) # Odmah iskoristi (Stored Procedure)
                    dropped_items.remove(it)

        # Crtanje
        for b in bullets: b.draw(screen)
        for e in enemies: e.draw(screen)
        for it in dropped_items:
            color = (0, 255, 255) if it.item_type == 'heal' else (255, 255, 0)
            pygame.draw.rect(screen, color, (it.x, it.y, 15, 15))

        color = (0, 255, 0) if player.status == "Aktivan" else (100, 100, 100)
        pygame.draw.rect(screen, color, (player.x, player.y, 40, 40))
        
        # UI
        font = pygame.font.SysFont(None, 32)
        ui_text = f"HP: {player.hp} | Score: {player.score} | Inv: {len(player.inventory)}"
        screen.blit(font.render(ui_text, True, (255, 255, 255)), (20, 20))

        if player.status == "Poražen":
            screen.blit(pygame.font.SysFont(None, 72).render("GAME OVER", True, (255, 0, 0)), (250, 200))
            # Prikaz top score-a iz baze
            y_off = 280
            screen.blit(font.render("Top Scores (iz ZODB BTree):", True, (255, 255, 255)), (280, y_off))
            for name, score in db.get_top_scores(3):
                y_off += 30
                screen.blit(font.render(f"{name}: {score}", True, (200, 200, 200)), (300, y_off))
            screen.blit(font.render("Pritisni R za Restart", True, (200, 200, 200)), (280, y_off + 50))

        pygame.display.flip()
        clock.tick(60)

    db.close()
    pygame.quit()

if __name__ == "__main__":
    run_game()
