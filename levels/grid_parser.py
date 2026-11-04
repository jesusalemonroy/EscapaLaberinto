# levels/grid_parser.py

class LevelParser:
    def __init__(self, level_string):
        self.grid = []
        self.player_pos = None
        self.agent_pos = None
        self.exit_pos = None
        self.parse_grid(level_string)

    def parse_grid(self, level_string):
        """
        Lee una cadena multilínea de 10x10, almacena la matriz y 
        encuentra las coordenadas (x, y) de las entidades.
        """
        # Limpiar líneas vacías y espacios
        lines = [line.strip() for line in level_string.strip().split('\n') if line.strip()]
        
        if len(lines) != 10:
            raise ValueError(f"El laberinto debe tener exactamente 10 filas. Se encontraron {len(lines)}.")

        for y, row in enumerate(lines):
            if len(row) != 10:
                raise ValueError(f"La fila {y} debe tener exactamente 10 columnas.")
            
            grid_row = []
            for x, char in enumerate(row):
                grid_row.append(char)
                # Extraer coordenadas mapeadas a pantalla (0,0 en top-left)
                if char == 'P':
                    self.player_pos = (x, y)
                elif char == 'G':
                    self.agent_pos = (x, y)
                elif char == 'E':
                    self.exit_pos = (x, y)
            
            self.grid.append(grid_row)

    def is_obstacle(self, x, y):
        """Devuelve True si la celda (x, y) contiene un obstáculo (#)[cite: 1]."""
        if 0 <= x < 10 and 0 <= y < 10:
            return self.grid[y][x] == '#'
        return True # Fuera de límites se considera obstáculo