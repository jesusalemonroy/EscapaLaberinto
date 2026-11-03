# Escape del laberinto - Proyecto de IA

Videojuego por turnos desarrollado en Python y PyGame para la asignatura de Inteligencia Artificial (0406). El objetivo es guiar a un jugador humano a través de tres laberintos de $10\times10$ hasta la salida, evitando ser capturado por un agente inteligente.

## Características y Niveles

El juego consta de tres niveles consecutivos, cada uno implementando una técnica de Inteligencia Artificial distinta para el agente perseguidor:

* **Nivel 1 (Búsqueda A*):** El agente calcula la ruta óptima hacia el jugador utilizando el algoritmo $A^*$ con la distancia Manhattan como heurística.

* **Nivel 2 (Búsqueda Adversarial):** El agente utiliza el algoritmo Minimax con poda Alfa-Beta (profundidad de 4 movimientos) actuando como el jugador MAX.

* **Nivel 3 (Lógica Proposicional):** El agente sigue una ruta de patrullaje cíclica y, al detectar al jugador, utiliza una base de conocimiento y reglas de inferencia para capturarlo.

## Requisitos previos

* **Python:** 3.12 o 3.13 (Se recomienda evitar versiones en fase alfa como la 3.14 por compatibilidad de librerías).

* **PyGame:** 2.6.x o superior.

## Instalación y ejecución

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu-usuario/escape-del-laberinto.git
   cd escape-del-laberinto
   ```

2. Instala las dependencias necesarias:
   ```bash
   pip install pygame
   ```

3. Ejecuta el juego:
   ```bash
   python main.py
   ```

## Estructura del proyecto

El código está estructurado siguiendo principios de Programación Orientada a Objetos (OOP) con el patrón State para el manejo de pantallas y polimorfismo para la lógica de los distintos agentes (AStarAgent, MinimaxAgent, LogicAgent).