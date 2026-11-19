# ui/screens/screen.py
from abc import ABC, abstractmethod

class Screen(ABC):
    """
    Clase base abstracta para todas las pantallas del juego.
    Aplica el patrón State para que el gestor principal pueda intercambiarlas.
    """
    
    def __init__(self, screen_surface):
        self.screen = screen_surface

    @abstractmethod
    def handle_events(self, events):
        """
        Procesa la entrada del usuario (teclado, ratón).
        Debe retornar una cadena con el nombre del siguiente estado 
        (ej. "GAME_SCREEN", "QUIT") o el estado actual si no hay cambios.
        """
        pass

    @abstractmethod
    def update(self):
        """
        Actualiza la lógica de la pantalla. 
        En el caso del juego, aquí se procesará el sistema por turnos 
        (movimiento del jugador y cálculo del agente).
        """
        pass

    @abstractmethod
    def draw(self):
        """
        Renderiza los elementos gráficos en la superficie principal.
        """
        pass