# main.py
import pygame
import sys
from ui.screens.start_screen import StartScreen
from ui.screens.game_screen import GameScreen
from levels.level_manager import LevelManager

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Proyecto Final: Escape del Laberinto - IA")
    clock = pygame.time.Clock()

    # Inicializar gestores y pantallas
    level_manager = LevelManager()
    states = {
        "START_SCREEN": StartScreen(screen),
        "GAME_SCREEN": GameScreen(screen, level_manager)
    }
    
    current_state_name = "START_SCREEN"
    current_state = states[current_state_name]

    running = True
    while running:
        events = pygame.event.get()
        
        # Procesar eventos según el estado actual
        next_state_name = current_state.handle_events(events)
        
        if next_state_name == "QUIT":
            running = False
        elif next_state_name != current_state_name:
            # Transición de estado (si el jugador presiona JUGAR o ESC)
            if next_state_name in states:
                # Reiniciar el nivel si venimos de la pantalla de inicio
                if next_state_name == "GAME_SCREEN":
                    level_manager = LevelManager()
                    states["GAME_SCREEN"] = GameScreen(screen, level_manager)
                    
                current_state_name = next_state_name
                current_state = states[current_state_name]

        # Actualizar y renderizar el estado actual
        current_state.update()
        current_state.draw()
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()