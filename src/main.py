import pygame
from database import GameDB
from models import Player

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("ZODB RPG Projekt")
    
    db = GameDB()
    # Dohvati ili kreiraj igrača
    player_name = "Igrac1"
    if player_name not in db.root['players']:
        db.root['players'][player_name] = Player(player_name)
        db.save()
    
    player = db.root['players'][player_name]
    clock = pygame.time.Clock()

    # Primjer upita: ispiši sve aktivne igrače na početku
    aktivni = db.get_all_active_players()
    print(f"Aktivni igrači u bazi: {[p.name for p in aktivni]}")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                db.save() # Spremi napredak prije izlaza
                running = False
            
            # Simulacija damage-a za trigger (tipka SPACE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.take_damage(20)
                    print(f"Igrač {player.name} primio damage. HP: {player.hp}")
                
                # Izlaz na tipku X
                if event.key == pygame.K_x:
                    db.save()
                    running = False

        # Kretanje (A i D)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: player.move(-5, 0)
        if keys[pygame.K_d]: player.move(5, 0)

        # Crtanje
        screen.fill((50, 50, 50))
        
        # Nacrtaj igrača
        color = (0, 255, 0) if player.status == "Aktivan" else (255, 0, 0)
        pygame.draw.rect(screen, color, (player.x, player.y, 40, 40))
        
        # Ispis HP-a na ekranu
        font = pygame.font.SysFont(None, 36)
        img = font.render(f"Ime: {player.name} | HP: {player.hp} | Status: {player.status}", True, (255, 255, 255))
        screen.blit(img, (20, 20))

        # Upute na ekranu
        small_font = pygame.font.SysFont(None, 24)
        instr = small_font.render("Kontrole: A/D = Kretanje | SPACE = Damage | X = Spremi i izađi", True, (200, 200, 200))
        screen.blit(instr, (20, 560))

        pygame.display.flip()
        clock.tick(60)

    db.close()
    pygame.quit()

if __name__ == "__main__":
    run_game()