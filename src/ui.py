import pygame
from config import WHITE, BLUE

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
