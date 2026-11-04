# entities/player.py
from entities.entity import Entity

class Player(Entity):
    def move(self, dx, dy, grid_parser):
        """
        Intenta mover al jugador en la dirección dada por dx, dy.
        Retorna True si el movimiento fue exitoso, False si fue inválido.
        """
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < 10 and 0 <= new_y < 10:
            if not grid_parser.is_obstacle(new_x, new_y):
                self.x = new_x
                self.y = new_y
                return True
        return False