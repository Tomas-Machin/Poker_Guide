
# 🃏 Poker_Guide

Bienvenido al repositorio de **Poker_Guide**, un programa de póker desarrollado para dar soporte a las desiciones de los jugadores en el juego de póker Texas Hold'em.

---

## 📋 Descripción

### Version 1.0

Este programa implementa una versión del póker Texas Hold'em con reglas estándar, turnos automáticos, y lógica de evaluación de manos.
El programa no te permite jugar pero si dar soporte a toma de decisiones. Evaluará diferentes variables y determinará cual es la mejor de las acciones en tu turno.

Características:
- Evaluación precisa de manos
- Modelo probabilistico

---

## 🚀 Instalación

Clona el repositorio y navega al directorio:

```bash
git https://github.com/Tomas-Machin/Poker_Guide.git
cd Poker_Guide
```

---

## 📖 Manual de usuario

1. Una vez dentro de la carpeta **Poker_Guide** deberá introducir el siguiente comando por el terminal para poder ejecutar el programa:

```bash
py main.py
```

Una vez introducido, el programa deberá tardar unos 20 segundos la primera vez en ejecutar (posteriormente tardará entre 4 y 5 segundos).

2. En la consola se mostrará informacion que el usuario deberá introducir a forma de formulario para poder empezar la partida. Esta información será:

- El numero de jugadores que hay en la mesa (**2 - 7**).
- Las ciegas de la partida (**>0.02**).
- La posición en la que se encuentra el usuario **["UTG", "MP", "HJ", "CO", "BU", "SB", "BB"]**.
- La mano del usuario con el formato: **AS 10C** siendo los palos H, S, C, D (Hearts, Spades, Cloves, Diamonds).
- Las fichas en términos de ciegas de cada jugador (fichas / ciegas de la mesa).

3. Una vez introducida dicha información la partica comenzará. En la consola aparecerá información sobre la ronda en la que se encuentra y el jugador que esta tomando turno. El usuario deberá introducir las apuestas realizadas por cada jugador.

- ***En caso de ser el turno del usuario, aparecerán una serie de probabilidades en las diferentes acciones que puede realizar. Esa es la ayuda proporcionada por el modelo probabilisico utilizado para poder mejorar la decisión tomada por el usuario.***

4. El usuario debera repetir el proceso hasta que se termine la partida. Ya sea por que quede un jugador en la partida o haya u showdown en la ronda final.

- Como alternativa en caso de que el usuario no quiera poner los datos de una partida en la que no participa, puede detener el programa y volver a ejecutarlo cuando empiece una nueva partida.

5. Finalmente, el usuario deberá proporcionar al sistema la información de las cartas comunitarias mostradas al inicio de las rondas POSTFLOP, TURN y RIVER.
