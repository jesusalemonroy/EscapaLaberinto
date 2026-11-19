# entities/agents/minimax_agent.py
from entities.entity import Entity


class MinimaxAgent(Entity):
    """
    Agente perseguidor para el Nivel 2: Búsqueda adversarial.
    Implementa Minimax con poda alfa-beta y profundidad limitada (4 movimientos individuales).
    """

    def __init__(self, x, y, max_depth=4):
        super().__init__(x, y)
        self.max_depth = max_depth

    def heuristic(self, pos1, pos2):
        """Distancia Manhattan entre dos coordenadas (x, y)."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def test_terminal(self, estado):
        
        # Determina si el estado es terminal:
      
        return (
            estado["agente"] == estado["jugador"]
            or estado["jugador"] == estado["salida"]
        )

    def eval_estado(self, estado, profundidad):
        """
        Función de utilidad y evaluación heurística desde la perspectiva de MAX (agente).
        - Captura: +1000 (+ profundidad para premiar capturas más rápidas).
        - Escape: -1000 (- profundidad para penalizar escapes más rápidos).
        - No terminal: minimiza distancia al jugador y maximiza distancia del jugador a la salida.
        """
        agente = estado["agente"]
        jugador = estado["jugador"]
        salida = estado["salida"]

        if agente == jugador:
            return 1000 + profundidad
        if jugador == salida:
            return -1000 - profundidad

        dist_agente_jugador = self.heuristic(agente, jugador)
        dist_jugador_salida = self.heuristic(jugador, salida)

        return (-2 * dist_agente_jugador) + dist_jugador_salida

    def sucesores(self, estado, grid_parser):
        """
        Genera los pares (accion, nuevo_estado) para el jugador en turno.
        - turno == 'MAX': mueve el agente perseguidor.
        - turno == 'MIN': mueve el jugador humano.
        """
        if self.test_terminal(estado):
            return []

        turno = estado["turno"]
        lista = []

        if turno == "MAX":
            ax, ay = estado["agente"]
            for nueva_pos in self.get_valid_neighbors(ax, ay, grid_parser):
                nuevo_estado = {
                    "agente": nueva_pos,
                    "jugador": estado["jugador"],
                    "salida": estado["salida"],
                    "turno": "MIN",
                }
                lista.append((nueva_pos, nuevo_estado))
        else:
            jx, jy = estado["jugador"]
            for nueva_pos in self.get_valid_neighbors(jx, jy, grid_parser):
                nuevo_estado = {
                    "agente": estado["agente"],
                    "jugador": nueva_pos,
                    "salida": estado["salida"],
                    "turno": "MAX",
                }
                lista.append((nueva_pos, nuevo_estado))

        return lista

    def max_valor_ab(self, estado, alfa, beta, profundidad, grid_parser):
        if self.test_terminal(estado) or profundidad == 0:
            return self.eval_estado(estado, profundidad)

        v = -float("inf")

        for accion, s in self.sucesores(estado, grid_parser):
            v = max(v, self.min_valor_ab(s, alfa, beta, profundidad - 1, grid_parser))

            if v >= beta:
                return v

            alfa = max(alfa, v)

        return v

    def min_valor_ab(self, estado, alfa, beta, profundidad, grid_parser):
        if self.test_terminal(estado) or profundidad == 0:
            return self.eval_estado(estado, profundidad)

        v = float("inf")

        for accion, s in self.sucesores(estado, grid_parser):
            v = min(v, self.max_valor_ab(s, alfa, beta, profundidad - 1, grid_parser))

            if v <= alfa:
                return v

            beta = min(beta, v)

        return v

    def decision_alfa_beta(self, estado, grid_parser):
        """
        Selecciona la mejor acción para MAX explorando hasta self.max_depth
        movimientos individuales (el primer movimiento cuenta como 1).
        """
        mejor_valor = -float("inf")
        mejor_accion = estado["agente"]

        alfa = -float("inf")
        beta = float("inf")

        for accion, s in self.sucesores(estado, grid_parser):
            v = self.min_valor_ab(s, alfa, beta, self.max_depth - 1, grid_parser)

            if v > mejor_valor:
                mejor_valor = v
                mejor_accion = accion

            alfa = max(alfa, mejor_valor)

        return mejor_accion

    def take_turn(self, player_pos, grid_parser, exit_pos=None):
        """
        Ejecuta el turno del agente calculando el mejor movimiento con poda alfa-beta
        y avanzando una sola celda.
        """
        if exit_pos is None:
            # Toma la salida desde grid_parser si existe; si no, usa la esquina superior derecha (9, 0)
            exit_pos = getattr(grid_parser, "exit_pos", (9, 0))

        estado_actual = {
            "agente": (self.x, self.y),
            "jugador": player_pos,
            "salida": exit_pos,
            "turno": "MAX",
        }

        siguiente_paso = self.decision_alfa_beta(estado_actual, grid_parser)
        self.x, self.y = siguiente_paso[0], siguiente_paso[1]
