>[!NOTE]
Descripción del proceso de modelado

# Modelar una red neuronal que pueda jugar al 5 en linea sin gravedad en un tablero de 20*20.

- ## Definir el tipo de red neuronal y describir cada una de sus partes
    ### Tipo de red: Convolucional (CNN)
    <div align="justify">
        Normalmente utilizadas en el procesamiento de imagenes debido a que detectan patrones y características visuales.
        En este caso podría servir para dectar la posición de las piezas de los jugadores y esta aprenda a posicionar 5 piezas seguidas del mismo tipo e interrumpir el alineamiento de las piezas enemigas.
    </div>

    ### Partes:
    - #### Capas de entrada:
        - Posicion de las piezas aliadas
        - Posicion de las piezas enemigas
        - Tamaño del tablero

    - #### Capas Oculta
        >[!WARNING]
        No estoy seguro de que describir aquí.
        
    - #### Capas de Salida:
        - Retorno de puntaje de las predicciones para cada posible jugada y estrategia.
        

 - ## Definir los patrones a utilizar
    - Alineacion de las piezas consecutivamente de 1 a 5.
    - Bloqueo de la alineacion de 5 piezas enemigas.
    - Oportunidades de alinear 5 piezas para ganar.
    - Posibles ahogamientos en donde ningun jugador pueda ganar.
    - Estrategias de posicionamiento.

>    - Definir que función de activación es necesaria para este problema

>    - Definir el numero máximo de entradas

>    - ¿Qué valores a la salida de la red se podrían esperar?

>    - ¿Cuales son los valores máximos que puede tener el bias?
