# ui/screens/game_screen.py
import pygame
from entities.player import Player
from entities.agents.a_star_agent import AStarAgent
from entities.agents.minimax_agent import MinimaxAgent
from entities.agents.logic_agent import LogicAgent

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

        self.offset_x = (screen.get_width() - (GRID_WIDTH * CELL_SIZE)) // 2
        self.offset_y = (screen.get_height() - (GRID_HEIGHT * CELL_SIZE)) // 2

        self.font = pygame.font.SysFont("consolas", 28, bold=True)
        self.small_font = pygame.font.SysFont("consolas", 18)

        self._setup_level()

    def _create_agent_for_level(self, level_num, agent_pos):
        if level_num == 1:
            return AStarAgent(*agent_pos)
        elif level_num == 2:
            return MinimaxAgent(*agent_pos)
        elif level_num == 3:
            return LogicAgent(*agent_pos)
        raise ValueError(f"Nivel no soportado: {level_num}")

    def _setup_level(self):
        self.parser = self.level_manager.parser
        self.player = Player(*self.parser.player_pos)
        self.agent = self._create_agent_for_level(
            self.level_manager.current_level,
            self.parser.agent_pos
        )
        self.exit_pos = self.parser.exit_pos

        self.game_over = False
        self.level_cleared = False
        self.campaign_completed = False
        self.message = ""

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return "QUIT"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.level_manager.reset()
                    return "START_SCREEN"

                # Avanzar al siguiente nivel tras completar el actual
                if self.level_cleared and not self.campaign_completed:
                    if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                        if self.level_manager.next_level():
                            self._setup_level()
                    continue

                # Reiniciar nivel o campaña si fue capturado o terminó el juego
                if self.game_over:
                    if event.key == pygame.K_r:
                        if self.campaign_completed:
                            self.level_manager.reset()
                        else:
                            self.level_manager.load_level(self.level_manager.current_level)
                        self._setup_level()
                    continue

                # Manejo de turnos si el juego está activo
                dx, dy = 0, 0
                if event.key in [pygame.K_w, pygame.K_UP]:
                    dy = -1
                elif event.key in [pygame.K_s, pygame.K_DOWN]:
                    dy = 1
                elif event.key in [pygame.K_a, pygame.K_LEFT]:
                    dx = -1
                elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                    dx = 1

                if dx != 0 or dy != 0:
                    # 1. Turno del Jugador
                    movimiento_valido = self.player.move(dx, dy, self.parser)

                    if movimiento_valido:
                        # Verificar primero si el jugador llegó a la salida o pisó al agente
                        self.check_game_state()
                        if not self.game_over:
                            # 2. Turno del Agente
                            self.agent.take_turn((self.player.x, self.player.y), self.parser)
                            # 3. Evaluar captura tras movimiento del agente
                            self.check_game_state()

        return "GAME_SCREEN"

    def check_game_state(self):
        lvl = self.level_manager.current_level
        if (self.player.x, self.player.y) == self.exit_pos:
            self.game_over = True
            self.level_cleared = True
            if lvl < self.level_manager.max_levels:
                self.message = f"NIVEL {lvl} COMPLETADO - [ENTER] SIGUIENTE"
            else:
                self.campaign_completed = True
                self.message = "¡JUEGO COMPLETADO! - [R] REINICIAR"
        elif (self.agent.x, self.agent.y) == (self.player.x, self.player.y):
            self.game_over = True
            self.level_cleared = False
            self.message = "CAPTURADO - [R] REINTENTAR"

    def update(self):
        pass

    def draw(self):
        self.screen.fill(BG_COLOR)
        grid = self.parser.grid

        # 1. Dibujar escenario estático
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                char = grid[row][col]
                rect = pygame.Rect(
                    self.offset_x + (col * CELL_SIZE),
                    self.offset_y + (row * CELL_SIZE),
                    CELL_SIZE, CELL_SIZE
                )
                if char == '#':
                    pygame.draw.rect(self.screen, WALL_COLOR, rect)
                else:
                    pygame.draw.rect(self.screen, GRID_LINE_COLOR, rect, 1)

        # Dibujar salida
        exit_rect = pygame.Rect(
            self.offset_x + (self.exit_pos[0] * CELL_SIZE),
            self.offset_y + (self.exit_pos[1] * CELL_SIZE),
            CELL_SIZE, CELL_SIZE
        )
        pygame.draw.rect(self.screen, EXIT_COLOR, exit_rect)

        # 2. Dibujar entidades dinámicas
        player_rect = pygame.Rect(
            self.offset_x + (self.player.x * CELL_SIZE) + 5,
            self.offset_y + (self.player.y * CELL_SIZE) + 5,
            CELL_SIZE - 10, CELL_SIZE - 10
        )
        pygame.draw.rect(self.screen, PLAYER_COLOR, player_rect, border_radius=8)

        agent_rect = pygame.Rect(
            self.offset_x + (self.agent.x * CELL_SIZE) + 5,
            self.offset_y + (self.agent.y * CELL_SIZE) + 5,
            CELL_SIZE - 10, CELL_SIZE - 10
        )
        pygame.draw.rect(self.screen, AGENT_COLOR, agent_rect, border_radius=8)

        # 3. HUD superior/inferior (Nivel actual e inferencia del agente en Nivel 3)
        hud_text = f"Nivel {self.level_manager.current_level}/3"
        if isinstance(self.agent, LogicAgent):
            hud_text += f" | Agente BC: {self.agent.last_inference}"
        hud_surf = self.small_font.render(hud_text, True, TEXT_COLOR)
        self.screen.blit(hud_surf, (20, 15))

        # 4. Mensaje de fin de nivel / captura
        if self.game_over:
            msg_surf = self.font.render(self.message, True, TEXT_COLOR)
            msg_rect = msg_surf.get_rect(center=(self.screen.get_width() // 2, 45))
            self.screen.blit(msg_surf, msg_rect)