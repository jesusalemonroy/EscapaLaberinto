# entities/agents/a_star_agent.py
import heapq
from entities.entity import Entity

class AStarAgent(Entity):
    def heuristic(self, pos, goal):
        """Función heurística h(n): Distancia Manhattan."""
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    def calculate_path(self, goal_pos, grid_parser):
        """
        Algoritmo 5: A*(G, s, meta)[cite: 5].
        Calcula la ruta óptima hacia la posición actual del jugador.
        """
        s = (self.x, self.y)
        meta = goal_pos
        
        # 1 inicializar frontera con s y f(s) = h(s)[cite: 5]
        # La tupla para heapq es (f(n), id_desempate, nodo_coordenada)
        frontera = []
        heapq.heappush(frontera, (self.heuristic(s, meta), 0, s))
        
        # 2 g(s) = 0, padre(s) = NULO[cite: 5]
        g = {s: 0}
        padre = {s: None}
        
        tie_breaker = 1 # Para evitar errores de comparación en heapq con tuplas iguales
        
        # 3 while la frontera no esté vacía do[cite: 5]
        while frontera:
            # 4 extraer n con menor f(n)[cite: 5]
            _, _, n = heapq.heappop(frontera)
            
            # 5 if n = meta then[cite: 5]
            if n == meta:
                # 6 reconstruir y retornar ruta[cite: 5]
                ruta = []
                actual = n
                while actual is not None:
                    ruta.append(actual)
                    actual = padre[actual]
                ruta.reverse() # Invertir para que vaya desde 's' hasta 'meta'
                return ruta
            
            # 8 foreach vecino v de n do[cite: 5]
            vecinos = self.get_valid_neighbors(n[0], n[1], grid_parser)
            for v in vecinos:
                # 9 gnuevo = g(n) + costo(n, v)[cite: 5]
                # El costo entre celdas adyacentes es unitario (1)
                gnuevo = g[n] + 1
                
                # 10 if v no explorado o gnuevo < g(v) then[cite: 5]
                if v not in g or gnuevo < g[v]:
                    # 11 g(v) = gnuevo, f(v) = g(v) + h(v)[cite: 5]
                    g[v] = gnuevo
                    f_v = gnuevo + self.heuristic(v, meta)
                    
                    # 12 padre(v) = n, insertar v en frontera[cite: 5]
                    padre[v] = n
                    heapq.heappush(frontera, (f_v, tie_breaker, v))
                    tie_breaker += 1
                    
        # 16 return "no hay ruta"[cite: 5]
        return []

    def take_turn(self, player_pos, grid_parser):
        """
        Ejecuta el turno del agente recalculando la ruta y moviéndose un solo paso.
        """
        ruta = self.calculate_path(player_pos, grid_parser)
        
        # El índice 0 es la posición actual del agente. 
        # El índice 1 es el primer paso de la ruta hacia el jugador.
        if len(ruta) > 1:
            siguiente_paso = ruta[1]
            self.x, self.y = siguiente_paso[0], siguiente_paso[1]