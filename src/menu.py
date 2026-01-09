import pygame
import sys
from config import *
from ui import Button, InputBox

class Menu:
    def __init__(self, game):
        self.game = game
        self.name_input = InputBox(WIDTH//2 - 100, HEIGHT//2 - 100, 140, 32, self.game.player_name)
        self.btn_start = Button(WIDTH//2 - 100, HEIGHT//2 - 30, 200, 50, "New Game", color=GREEN)
        self.btn_load_menu = Button(WIDTH//2 - 100, HEIGHT//2 + 40, 200, 50, "Load / Continue", color=BLUE)
        self.btn_leaderboard = Button(WIDTH//2 - 100, HEIGHT//2 + 110, 200, 50, "Leaderboard", color=GRAY)
        self.btn_quit = Button(WIDTH//2 - 100, HEIGHT//2 + 180, 200, 50, "Exit", color=RED)
        self.btn_back = Button(50, HEIGHT - 80, 150, 40, "Back", color=GRAY)
        self.load_buttons = []

    def handle_main(self, events):
        self.game.screen.fill(DARK_GRAY)
        title = self.game.title_font.render("ZODB Survival Shooter", True, WHITE)
        self.game.screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        info = self.game.font.render("Enter name for New Game:", True, WHITE)
        self.game.screen.blit(info, (WIDTH//2 - info.get_width()//2, HEIGHT//2 - 140))

        for event in events:
            self.name_input.handle_event(event)
            if self.btn_start.is_clicked(event):
                if self.name_input.text:
                    self.game.player_name = self.name_input.text
                self.game.load_player()
                self.game.start_countdown()
            elif self.btn_load_menu.is_clicked(event):
                self.refresh_load_menu()
                self.game.state = "LOAD_GAME"
            elif self.btn_leaderboard.is_clicked(event):
                self.game.state = "LEADERBOARD"
            elif self.btn_quit.is_clicked(event):
                self.game.save_game_state()
                self.game.state = "EXIT"

        self.name_input.draw(self.game.screen, self.game.font)
        self.btn_start.draw(self.game.screen, self.game.font)
        self.btn_load_menu.draw(self.game.screen, self.game.font)
        self.btn_leaderboard.draw(self.game.screen, self.game.font)
        self.btn_quit.draw(self.game.screen, self.game.font)

    def refresh_load_menu(self):
        active_players = self.game.db.get_all_active_players()
        last_played = self.game.db.root['world_state'].get('last_played')
        
        self.load_buttons = []
        start_y = 150
        for i, p in enumerate(active_players):
            display_name = p.name
            if p.name == last_played:
                display_name += " (last played)"
                
            info_str = f"Score: {p.score} | HP: {p.hp} | Time: {self.game.format_time(p.time_survived)}"
            btn = Button(WIDTH//2 - 250, start_y + i * 70, 500, 60, display_name, color=BLUE)
            self.load_buttons.append((btn, p.name, info_str))

    def handle_load_game(self, events):
        self.game.screen.fill(BLACK)
        title = self.game.title_font.render("Continue Adventure", True, CYAN)
        self.game.screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))

        if not self.load_buttons:
            empty_msg = self.game.font.render("No active saved games found.", True, GRAY)
            self.game.screen.blit(empty_msg, (WIDTH//2 - empty_msg.get_width()//2, HEIGHT//2))

        for event in events:
            if self.btn_back.is_clicked(event):
                self.game.state = "MENU"
            for btn, name, info in self.load_buttons:
                if btn.is_clicked(event):
                    self.game.load_player(name)
                    self.game.start_countdown()

        for btn, name, info in self.load_buttons:
            btn.draw(self.game.screen, self.game.font, small_text=info)

        self.btn_back.draw(self.game.screen, self.game.font)

    def handle_leaderboard(self, events):
        self.game.screen.fill(BLACK)
        title = self.game.title_font.render("Leaderboard (ZODB)", True, YELLOW)
        self.game.screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        
        header = self.game.font.render("Rank   Name         Score    Time", True, (200, 200, 200))
        self.game.screen.blit(header, (WIDTH//2 - 250, 120))
        pygame.draw.line(self.game.screen, WHITE, (WIDTH//2 - 260, 150), (WIDTH//2 + 260, 150), 2)

        top_scores = self.game.db.get_top_scores(10)
        start_y = 170
        for i, (name, score, time_val) in enumerate(top_scores):
            time_str = self.game.format_time(time_val)
            text_str = f"{i+1:<5}  {name:<12} {score:<8} {time_str}"
            text = self.game.font.render(text_str, True, WHITE)
            self.game.screen.blit(text, (WIDTH//2 - 250, start_y + i * 40))

        for event in events:
            if self.btn_back.is_clicked(event):
                self.game.state = "MENU"

        self.btn_back.draw(self.game.screen, self.game.font)
