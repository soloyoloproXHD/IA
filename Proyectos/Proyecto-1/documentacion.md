# 📝 Documentación del Algoritmo A* con Python

## 🏹  Objetivo
EL objetivo de este proyecto es demostrar el funcionamiento del algoritmo **`A*`** cuya funcionalidad es encontrar el camino más rapido entre un punto **`A`** y un punto **`B`**, en este proyecto la busqueda del camino se lleva a cabo dentro de una cuadricula simetrica **`(..., 10*10, 11*11, 12*12,...)`** donde el costo de desplazamiento **`vertical`** y **`horizontal`** es de **`10`**, ahora, en el caso del costo para el desplazamiento en **`diagonal`** es de **`14`**.

---

## 🟦 Configuración Inicial

Se define el tamaño de la ventana y se establecen los colores que se utilizarán en la representación visual:

```python
import pygame

ANCHO_VENTANA = 800
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("A*")

# Definición de colores (RGB)
BLANCO = (255,255,255)
NEGRO = (0,0,0)
GRIS = (128,128,128)
VERDE = (0,255,0)
ROJO = (255,0,0)
NARANJA = (255,165,0)
AZUL = (0, 255, 255)
PURPURA = (128,0,128)
```

> **Importante:**
> Se usa **`pygame.display.set_mode`** para crear la ventana y **`pygame.display.set_caption`** para darle un título.

---

## Clase `Nodo`
#### Constructor de la clase

```python
class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.vecinos = []
        self.g = float("inf")
        self.h = float("inf")
        self.f = float("inf")
```

> **Importante:**
> Los valores **`g`**, **`h`** y **`f`** representan los costos en el algoritmo **`A*`**:
> - **`g`**: Costo de desplazamiento.
> - **`h`**: Estimación de costo desde el nodo actual hasta el nodo objetivo.
> - **`f`**: Suma de **`g`** y **`h`** que representa el costo total de desplazamiento.

### 🟥 Métodos Importantes

Algunos métodos de `Nodo` permiten cambiar su estado:

```python
def get_pos(self):
    return self.fila, self.col
    
def es_pared(self):
    return self.color == NEGRO
    
def es_inicio(self):
    return self.color == NARANJA
    
def es_fin(self):
    return self.color == PURPURA
     
def hacer_inicio(self):
    self.color = NARANJA
    
def hacer_pared(self):
    self.color = NEGRO
        
def hacer_fin(self):
    self.color = PURPURA
    
def hacer_abierto(self):
    self.color = AZUL
    
def hacer_cerrado(self):
    self.color = GRIS
    
def hacer_camino(self):
    self.color = VERDE
```

> **Nota:**
> Estos métodos se utilizan para cambiar el color del nodo e identificar los nodos como lo son las paredes en color **`NEGRO`**, el inicio en color **`NARANJA`** y el **`DESTINO`** en color morado.

---

## `*️⃣` Algoritmo A*

El algoritmo implementado evalúa los nodos vecinos y elige el camino óptimo basado en el costo total `f`.

```python
def a_estrella(dibujar, grid, inicio, fin):
    nodos_camino = {}
    inicio.g = 0
    inicio.h = h(inicio, fin)
    inicio.f = inicio.g + inicio.h
    
    lista_abierta = [inicio]
    
    while lista_abierta:
        lista_abierta.sort(key=lambda nodo: nodo.f)
        nodo_actual = lista_abierta.pop(0)
        
        nodo_actual.evaluar_v(grid, nodos_camino)
        
        for vecino in nodo_actual.vecinos:
            if vecino == fin:
                nodos_camino[vecino] = nodo_actual
                camino(nodos_camino, vecino, dibujar)
                return True
            
            if vecino.color not in [NARANJA, AZUL]:
                vecino.hacer_abierto()
                if vecino not in lista_abierta:
                    lista_abierta.append(vecino)
                nodos_camino[vecino] = nodo_actual
        
        if nodo_actual != inicio:
            nodo_actual.hacer_cerrado()
            dibujar()
    
    return print("No se ha encontrado un camino")
```

> **Importante:**
> - `lista_abierta`: Contiene los nodos a evaluar.
> - `nodos_camino`: Guarda los nodos recorridos para reconstruir el camino.
> - Se ordena la `lista_abierta` por `f` para evaluar siempre el nodo más prometedor.

---

## 🏙️ Función `h`: Heurística Manhattan

Se utiliza la distancia Manhattan como heurística para estimar el costo restante.

```python
def h(p1, p2):
    X1, Y1 = p1.get_pos()
    X2, Y2 = p2.get_pos()
    return (abs(X1 - X2) + abs(Y1 - Y2)) * 10
```

> **Tip:**
> La distancia **Manhattan** es adecuada para movimientos en una cuadrícula donde solo se permiten movimientos horizontales y verticales.

---

## 🧑‍💻 Interacción con el Usuario

Se permiten los siguientes controles:

- **Click Izquierdo**: Colocar el nodo de inicio, el nodo final o una pared.
- **Click Derecho**: Eliminar un nodo.
- **Enter**: Ejecutar el algoritmo A* mandando llamar la función **`a_estrella()`**.
- **Esc**: Reiniciar la cuadrícula.

```python
if event.type == pygame.KEYDOWN:
    if event.key == pygame.K_KP_ENTER and inicio and fin:
        a_estrella(lambda: dibujar(ventana, grid, FILAS, ancho), grid, inicio, fin)
    elif event.key == pygame.K_ESCAPE:
        grid = crear_grid(FILAS, ancho)
        inicio = None
        fin = None
```

> **Importante:**
> El algoritmo solo se ejecuta si el usuario ha definido un nodo de inicio y un nodo de fin.

---

# 🍖 Fundamento de resolución para el problema de los canivales

> Perdone si lo que escribí a continuación son puras weas 💀

## Representación del Estado

Cada estado se define por una tupla `(M, C, B)` donde:

- `M`: Número de misioneros en la orilla izquierda.
- `C`: Número de caníbales en la orilla izquierda.
- `B`: Posición de la barca:
  - `0`: La barca está en la orilla izquierda.
  - `1`: La barca está en la orilla derecha.

### Ejemplo de estados:
- `(3, 3, 0)`: Estado inicial — todos en la orilla izquierda.
- `(0, 0, 1)`: Estado objetivo — todos en la orilla derecha.

---

## 💵 Función de Costo `g(n)`

- Cada cruce del río se considera un paso con costo uniforme:  
  `g(n) = número de pasos realizados desde el inicio`.

---

## 🏙️ Función Heurística `h(n)` — Distancia de Manhattan

La heurística estima el número mínimo de cruces necesarios para llevar a todas las personas restantes a la otra orilla.

## 📉 Función de Evaluación `f(n)`

El algoritmo A* utiliza:

\[
f(n) = g(n) + h(n)
\]

Donde:
- `g(n)`: Costo real desde el nodo inicial hasta el nodo actual.
- `h(n)`: Estimación del costo desde el nodo actual hasta el nodo objetivo.

---

## 📏 Reglas y Restricciones del Problema

Al generar estados vecinos, se deben cumplir las siguientes condiciones:

- Nunca debe haber más caníbales que misioneros en una orilla.
- La barca puede transportar entre 1 y 2 personas.
- No se deben repetir estados ya visitados.

---

## `*️⃣` Proceso del Algoritmo A*

1. Inicializar con el estado `(3, 3, 0)`.
2. Generar estados vecinos válidos según las reglas.
3. Evaluar `f(n)` para cada nuevo estado.
4. Elegir el estado con menor `f(n)` para continuar la búsqueda.
5. Repetir hasta alcanzar el estado objetivo `(0, 0, 1)`.

# 💀 Conclusiones

Verdaderamente este proyecto salio porque dios me vió a los ojos, no vale la pena validar el moviemiento en diagonal, casi se me quema el cerebro intentando definir la logica para eso.

> Aquí dejo el enlace a la pagina de los emojis, estan bonitos: https://yaytext.com/es/emoji/