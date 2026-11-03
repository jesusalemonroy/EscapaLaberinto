import pygame
import sys

# --- Constantes simuladas de core/settings.py ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Paleta de colores 
BG_COLOR = (40, 42, 54)       # Fondo oscuro
TITLE_COLOR = (80, 250, 123)  # Verde neón
TEXT_COLOR = (248, 248, 242)  # Blanco suave
HOVER_COLOR = (189, 147, 249) # Morado

class Button:
    """Componente de interfaz gráfica para interactuar en los menús."""
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.is_hovered = False

    def draw(self, surface):
        # Cambia el color si el cursor está encima
        color = HOVER_COLOR if self.is_hovered else TEXT_COLOR
        text_surf = self.font.render(self.text, True, color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        
        # Dibuja el borde y el texto
        pygame.draw.rect(surface, color, self.rect, 2, border_radius=10)
        surface.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos, mouse_pressed):
        return self.is_hovered and mouse_pressed[0]

class StartScreen:
    """
    Pantalla de título para 'Escape del laberinto'.
    Implementa el patrón State para poder ser intercambiada por el Nivel 1.
    """
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont("consolas", 48, bold=True)
        self.font_subtitle = pygame.font.SysFont("consolas", 24)
        self.font_button = pygame.font.SysFont("consolas", 32)
        
        # Textos basados en "Inteligencia_artificial-30.pdf"
        self.title_text = "ESCAPE DEL LABERINTO"
        self.subtitle_text = "Inteligencia Artificial 0406"
        
        # Botones
        center_x = SCREEN_WIDTH // 2
        self.btn_play = Button(center_x - 100, 300, 200, 60, "JUGAR", self.font_button)
        self.btn_quit = Button(center_x - 100, 390, 200, 60, "SALIR", self.font_button)

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        self.btn_play.check_hover(mouse_pos)
        self.btn_quit.check_hover(mouse_pos)

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.btn_play.is_clicked(mouse_pos, mouse_pressed):
                    # Aquí el gestor de estados cambiaría a la pantalla de juego
                    print("Iniciando Nivel 1: Búsqueda A*...")
                    return "GAME_SCREEN"
                if self.btn_quit.is_clicked(mouse_pos, mouse_pressed):
                    pygame.quit()
                    sys.exit()
        return "START_SCREEN"

    def update(self):
        # Lógica de actualización (animaciones, partículas) si las hubiera
        pass

    def draw(self):
        self.screen.fill(BG_COLOR)
        
        # Renderizado de títulos
        title_surf = self.font_title.render(self.title_text, True, TITLE_COLOR)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 150))
        
        subtitle_surf = self.font_subtitle.render(self.subtitle_text, True, TEXT_COLOR)
        subtitle_rect = subtitle_surf.get_rect(center=(SCREEN_WIDTH // 2, 210))

        self.screen.blit(title_surf, title_rect)
        self.screen.blit(subtitle_surf, subtitle_rect)

        # Renderizado de botones
        self.btn_play.draw(self.screen)
        self.btn_quit.draw(self.screen)

# --- Ciclo de prueba (simulación del main.py) ---
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Proyecto Final: IA")
    clock = pygame.time.Clock()
    
    start_screen = StartScreen(screen)
    
    running = True
    while running:
        events = pygame.event.get()
        
        # Manejo de estados (simplificado)
        next_state = start_screen.handle_events(events)
        if next_state == "GAME_SCREEN":
            # Transición hacia el escenario de 10x10
            pass 
            
        start_screen.update()
        start_screen.draw()
        
        pygame.display.flip()
        clock.tick(FPS)