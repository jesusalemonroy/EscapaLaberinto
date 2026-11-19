# ui/screens/game_screen.py
import pygame
from entities.player import Player
from entities.agents.a_star_agent import AStarAgent

GRID_WIDTH = 10
GRID_HEIGHT = 10
CELL_SIZE = 60

BG_COLOR = (15, 17, 26)
WALL_COLOR = (27, 30, 47)
PLAYER_COLOR = (0, 240, 255)
AGENT_COLOR = (125, 91, 166)
EXIT_COLOR = (224, 230, 237)
GRID_LINE_COLOR = (40, 42, 54)
TEXT_COLOR = (248, 248, 242)

class GameScreen:
    def __init__(self, screen, level_manager):
        self.screen = screen
        self.level_manager = level_manager
        self.parser = level_manager.parser
        
        self.offset_x = (screen.get_width() - (GRID_WIDTH * CELL_SIZE)) // 2
        self.offset_y = (screen.get_height() - (GRID_HEIGHT * CELL_SIZE)) // 2
        
        # Inicializar instancias basadas en el parser
        self.player = Player(*self.parser.player_pos)
        self.agent = AStarAgent(*self.parser.agent_pos)
        self.exit_pos = self.parser.exit_pos
        
        self.game_over = False
        self.message = ""
        self.font = pygame.font.SysFont("consolas", 32, bold=True)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return "QUIT"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "START_SCREEN"
                
                # Manejo de turnos si el juego está activo
                if not self.game_over:
                    dx, dy = 0, 0
                    if event.key in [pygame.K_w, pygame.K_UP]: dy = -1
                    elif event.key in [pygame.K_s, pygame.K_DOWN]: dy = 1
                    elif event.key in [pygame.K_a, pygame.K_LEFT]: dx = -1
                    elif event.key in [pygame.K_d, pygame.K_RIGHT]: dx = 1
                    
                    if dx != 0 or dy != 0:
                        # 1. Turno del Jugador
                        movimiento_valido = self.player.move(dx, dy, self.parser)
                        
                        if movimiento_valido:
                            # 2. Turno del Agente (solo se ejecuta si el jugador gastó su turno)
                            self.agent.take_turn((self.player.x, self.player.y), self.parser)
                            # 3. Evaluar estado de victoria/derrota
                            self.check_game_state()
                            
        return "GAME_SCREEN"

    def check_game_state(self):
        # Evaluar victoria (el jugador pisó la salida)
        if (self.player.x, self.player.y) == self.exit_pos:
            self.game_over = True
            self.message = "NIVEL 1 COMPLETADO"
        # Evaluar derrota (el agente interceptó al jugador)
        elif (self.agent.x, self.agent.y) == (self.player.x, self.player.y):
            self.game_over = True
            self.message = "CAPTURADO"

    def update(self):
        pass

    def draw(self):
        self.screen.fill(BG_COLOR)
        grid = self.parser.grid

        # 1. Dibujar escenario estático (piso, muros, salida)
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                char = grid[row][col]
                rect = pygame.Rect(self.offset_x + (col * CELL_SIZE), 
                                   self.offset_y + (row * CELL_SIZE), 
                                   CELL_SIZE, CELL_SIZE)
                
                if char == '#':
                    pygame.draw.rect(self.screen, WALL_COLOR, rect)
                else:
                    pygame.draw.rect(self.screen, GRID_LINE_COLOR, rect, 1)

        # Dibujar salida
        exit_rect = pygame.Rect(self.offset_x + (self.exit_pos[0] * CELL_SIZE),
                                self.offset_y + (self.exit_pos[1] * CELL_SIZE),
                                CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, EXIT_COLOR, exit_rect)

        # 2. Dibujar entidades dinámicas sobre el escenario
        player_rect = pygame.Rect(self.offset_x + (self.player.x * CELL_SIZE) + 5,
                                  self.offset_y + (self.player.y * CELL_SIZE) + 5,
                                  CELL_SIZE - 10, CELL_SIZE - 10)
        pygame.draw.rect(self.screen, PLAYER_COLOR, player_rect, border_radius=8)

        agent_rect = pygame.Rect(self.offset_x + (self.agent.x * CELL_SIZE) + 5,
                                 self.offset_y + (self.agent.y * CELL_SIZE) + 5,
                                 CELL_SIZE - 10, CELL_SIZE - 10)
        pygame.draw.rect(self.screen, AGENT_COLOR, agent_rect, border_radius=8)

        # 3. Dibujar mensaje de fin de juego
        if self.game_over:
            msg_surf = self.font.render(self.message, True, TEXT_COLOR)
            msg_rect = msg_surf.get_rect(center=(self.screen.get_width() // 2, 40))
            self.screen.blit(msg_surf, msg_rect)