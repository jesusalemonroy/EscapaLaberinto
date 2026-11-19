# entities/entity.py
class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_valid_neighbors(self, current_x, current_y, grid_parser):
        """
        Retorna una lista de coordenadas (x, y) de las celdas adyacentes válidas.
        Solo permite movimientos arriba, abajo, izquierda y derecha.
        """
        neighbors = []
        # Direcciones permitidas: Arriba, Abajo, Izquierda, Derecha
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        for dx, dy in directions:
            nx = current_x + dx
            ny = current_y + dy
            
            # Validar límites de la cuadrícula (10x10) y obstáculos
            if 0 <= nx < 10 and 0 <= ny < 10:
                if not grid_parser.is_obstacle(nx, ny):
                    neighbors.append((nx, ny))
                    
        return neighbors