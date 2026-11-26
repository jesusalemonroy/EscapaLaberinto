# entities/agents/logic_agent.py
from entities.entity import Entity

class LogicAgent(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        # Ruta de patrullaje del guardián
        self.patrol_route = [(7, 1), (8, 1), (8, 2), (7, 2)] # (8,9) -> (9,9) -> (9,8) -> (8,8) -> (8,9)
        self.patrol_index = 0
        self.last_inference = "Patrullar"

        # Conjunto de 13 símbolos proposicionales (2^13 = 8192 modelos máx.)
        self.simbolos = [
            'Perc_Arriba', 'Perc_Abajo', 'Perc_Izq', 'Perc_Der',
            'Libre_Arriba', 'Libre_Abajo', 'Libre_Izq', 'Libre_Der',
            'Mover_Arriba', 'Mover_Abajo', 'Mover_Izq', 'Mover_Der',
            'Patrullar'
        ]

    # FUNCIONES PARA INFERENCIA LÓGICA 
    # TELL
    def decir(self, BC, sentencia):
        """Incorpora una nueva sentencia a la BC mediante conjunción (TELL)."""
        return lambda m: BC(m) and sentencia(m)

    def extender(self, p, valor, modelo):
        """Crea una copia del modelo parcial asignando p = valor."""
        nuevo = modelo.copy()
        nuevo[p] = valor
        return nuevo

    # ASK
    def comprobar_tv(self, BC, alfa, simbolos, modelo):
        """Verifica recursivamente por tablas de verdad si BC |= alfa (ASK)."""
        if len(simbolos) == 0:
            if BC(modelo):
                return alfa(modelo)
            else:
                return True

        p = simbolos[0]
        resto = simbolos[1:]

        return (
            self.comprobar_tv(BC, alfa, resto, self.extender(p, True, modelo))
            and
            self.comprobar_tv(BC, alfa, resto, self.extender(p, False, modelo))
        )

    # SENSORES DEL AGENTE Y CONSTRUCCIÓN DE LA BASE DE CONOCIMIENTO
    def percibir_alrededor(self, player_pos, parser):
        #Solo detecta al jugador en las 4 celdas ortogonalmente adyacentes
    
        vecinos = {
            'Arriba': (self.x, self.y - 1),
            'Abajo':  (self.x, self.y + 1),
            'Izq':    (self.x - 1, self.y),
            'Der':    (self.x + 1, self.y),
        }

        # Valida las celdas transitables mediante Entity.get_valid_neighbors.
        validos = self.get_valid_neighbors(self.x, self.y, parser)
        percepciones = {}
        celdas_libres = {}

        for direccion, coord in vecinos.items():
            percepciones[direccion] = (player_pos == coord)
            celdas_libres[direccion] = (coord in validos)

        return percepciones, celdas_libres, vecinos

    # Construye la BC por cada turno con las reglas y percepciones.
    def construir_bc(self, percepciones, celdas_libres):

        BC = lambda m: True
        direcciones = ['Arriba', 'Abajo', 'Izq', 'Der']

        # Reglas de lógica proposicional
        for d in direcciones:
            # Si obtiene percepción y la casilla está libre, entonces el guardián se mueve
            # (Perc_d AND Libre_d) => Mover_d
            BC = self.decir(
                BC,
                lambda m, d=d: (not (m[f'Perc_{d}'] and m[f'Libre_{d}'])) or m[f'Mover_{d}']
            )
            # Restricción: no moverse en dirección d si no se percibe al jugador o hay muro
            BC = self.decir(
                BC,
                lambda m, d=d: (m[f'Perc_{d}'] and m[f'Libre_{d}']) or (not m[f'Mover_{d}'])
            )

        # Si no detecta al jugador sigue patrullando
        # (~Perc_Arriba AND ~Perc_Abajo AND ~Perc_Izq AND ~Perc_Der) => Patrullar
        BC = self.decir(
            BC,
            lambda m: (
                not (
                    not m['Perc_Arriba'] and not m['Perc_Abajo'] and
                    not m['Perc_Izq'] and not m['Perc_Der']
                )
            ) or m['Patrullar']
        )
        # Si se percibe al jugador en alguna celda adyacente, se interrumpe el patrullaje
        BC = self.decir(
            BC,
            lambda m: (
                not (
                    m['Perc_Arriba'] or m['Perc_Abajo'] or
                    m['Perc_Izq'] or m['Perc_Der']
                )
            ) or (not m['Patrullar'])
        )

        # Hechos percibidos en el turno actual (TELL)
        for d in direcciones:
            val_perc = percepciones[d]
            val_libre = celdas_libres[d]
            BC = self.decir(BC, lambda m, d=d, v=val_perc: m[f'Perc_{d}'] == v)
            BC = self.decir(BC, lambda m, d=d, v=val_libre: m[f'Libre_{d}'] == v)

        return BC

    # EJECUCIÓN DEL TURNO (PERCIBIR -> TELL -> ASK -> ACTUAR)
    def siguiente_paso_patrulla(self, parser):
        # Avanza 1 celda por turno siguiendo el ciclo o regresando a la ruta.
        pos_actual = (self.x, self.y)
        validos = self.get_valid_neighbors(self.x, self.y, parser)

        if pos_actual in self.patrol_route:
            idx = self.patrol_route.index(pos_actual)
            self.patrol_index = (idx + 1) % len(self.patrol_route)
            destino = self.patrol_route[self.patrol_index]
            if destino in validos:
                return destino

        # Si el guardián salió de la ruta tras una persecución, regresa 1 celda por turno
        objetivo = self.patrol_route[self.patrol_index]
        if validos:
            return min(validos, key=lambda c: abs(c[0] - objetivo[0]) + abs(c[1] - objetivo[1]))

        return pos_actual

    def take_turn(self, player_pos, parser):
        percepciones, celdas_libres, vecinos = self.percibir_alrededor(player_pos, parser)
        BC = self.construir_bc(percepciones, celdas_libres)

        # Consultar acciones de captura mediante ASK (comprobar_tv)
        for direccion in ['Arriba', 'Abajo', 'Izq', 'Der']:
            alfa = lambda m, d=direccion: m[f'Mover_{d}']
            if self.comprobar_tv(BC, alfa, self.simbolos, {}):
                self.x, self.y = vecinos[direccion]
                self.last_inference = f"BC |= Mover_{direccion}"
                return

        # Si no hay captura inferida, consultar patrullaje
        if self.comprobar_tv(BC, lambda m: m['Patrullar'], self.simbolos, {}):
            self.x, self.y = self.siguiente_paso_patrulla(parser)
            self.last_inference = "BC |= Patrullar"