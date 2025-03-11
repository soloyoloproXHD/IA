import pygame
import math

ANCHO_VENTANA = 800
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))

pygame.display.set_caption("A*")

#Definición de colores (RGB)
BLANCO = (255,255,255)
NEGRO = (0,0,0)
GRIS = (128,128,128)
VERDE = (0,255,0)
ROJO = (255,0,0)
NARANJA = (255,165,0)
AZUL = (0, 255, 255)
PURPURA = (128,0,128)

pygame.font.init()
FUENTE = pygame.font.SysFont("Arial", 16)

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
    
    def get_pos(self):
        return self.fila, self.col
    
    def es_pared(self):
        return self.color == NEGRO
    
    def es_inicio(self):
        return self.color == NARANJA
    
    def es_fin(self):
        return self.color == PURPURA
    
    def restablecer(self):
        self.color = BLANCO
        self.g = float("inf")
        self.h = float("inf")
        self.h = float("inf")
    
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
    #!-----------------------------------------------------------------------------
    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))
        
        if self.color == VERDE:
            pygame.draw.rect(ventana, NEGRO, (self.x, self.y, self.ancho, self.ancho), width=3)
        
        if self.color not in [BLANCO, NEGRO]:
            g, h, f = (("0" if x == float("inf") else int(x)) for x in (self.g, self.h, self.f))
            
            for i, (label, value) in enumerate(zip("ghf", (g,h,f))):
                ventana.blit(FUENTE.render(f"{label}: {value}", True, NEGRO), (self.x + 5, self.y + 5 + i * 15))
    #!-----------------------------------------------------------------------------
    def evaluar_v(self, grid, nodos_camino):
        self.vecinos = []
        direcciones = [
            (1, 0, 10), (-1, 0, 10), (0, 1, 10), (0, -1, 10),  # X, Y
            (1, 1, 14), (1, -1, 14), (-1, 1, 14), (-1, -1, 14) # Diagonales
        ]
        for d in direcciones:
            nueva_fila = self.fila + d[0]
            nueva_col = self.col + d[1]
            if 0 <= nueva_fila < self.total_filas and 0 <= nueva_col < self.total_filas:
                vecino = grid[nueva_fila][nueva_col]
                if not vecino.es_pared():
                    costo_g = self.g + d[2]
                    if costo_g < vecino.g:
                        vecino.g = costo_g
                        vecino.h = h(vecino, fin)
                        vecino.f = vecino.g + vecino.h
                        self.vecinos.append(vecino)

                        nodos_camino[vecino] = self
                        
#!-----------------------------------------------------------------------------
def h(p1, p2): #Heuristica usada: Manhattan (h(n) = |x1 - x2| + |y1 - y2|)
    x1, y1 = p1.get_pos()
    x2, y2 = p2.get_pos()
    h = (abs(x1 - x2) + abs(y1 - y2)) * 10
    # h = math.sqrt((x2-x1)**2 + (y2-y1)**2) * 10
    print(h)
    return h

def camino(nodos_camino, actual, dibujar): #Esta funcion reconstruirá el camino mas rapido encontrado
    while actual in nodos_camino:
        actual = nodos_camino[actual]
        actual.hacer_camino()
        dibujar()
        pygame.time.delay(100)

def a_estrella(dibujar, grid, inicio, fin): #Algoritmo de busqueda A*
    nodos_camino = {}
    inicio.g = 0
    inicio.h = h(inicio, fin)
    inicio.f = inicio.g + inicio.h
    
    lista_abierta = [inicio]
    
    while lista_abierta:
        lista_abierta.sort(key=lambda nodo: nodo.f)
        nodo_actual = lista_abierta.pop(0)
        
        if nodo_actual == fin:
            camino(nodos_camino, nodo_actual, dibujar) #Esta funcion debe de mostrar el camino mas rapido encontrado
            return True
        
        
        nodo_actual.evaluar_v(grid, nodos_camino) #Esta función deve de evaluar los vecinos del nodo actual para encontrar el camino mas rapido
        for vecino in nodo_actual.vecinos:
            if vecino == fin:
                nodos_camino[vecino] = nodo_actual
                camino(nodos_camino, vecino, dibujar)
                fin.hacer_camino()
                return True
            
            if vecino.color not in [NARANJA, AZUL]:  
                vecino.hacer_abierto()
                if vecino not in lista_abierta:
                    lista_abierta.append(vecino)
                nodos_camino[vecino] = nodo_actual
        
        nodo_actual.hacer_cerrado()
        dibujar()
        pygame.time.delay(200)
        
    return print("No hay camino") # En caso de no encontrar un camino, se mostrara el mensaje en consola
#!-----------------------------------------------------------------------------       
def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i,j,ancho_nodo,filas)
            grid[i].append(nodo)
    return grid

def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))

def dibujar(ventana, grid, filas, ancho):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)

    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()

def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col
   

def main(ventana, ancho):
    global fin
    FILAS = 10
    grid = crear_grid(FILAS, ancho)

    inicio = None
    fin = None

    corriendo = True

    while corriendo:
        dibujar(ventana, grid, FILAS, ancho)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            if pygame.mouse.get_pressed()[0]:  # Click izquierdo
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                if not inicio and nodo != fin:
                    inicio = nodo
                    inicio.hacer_inicio()

                elif not fin and nodo != inicio:
                    fin = nodo
                    fin.hacer_fin()

                elif nodo != fin and nodo != inicio:
                    nodo.hacer_pared()

            elif pygame.mouse.get_pressed()[2]:  # Click derecho
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                nodo.restablecer()
                if nodo == inicio:
                    inicio = None
                elif nodo == fin:
                    fin = None
            
            if event.type == pygame.KEYDOWN: #Mapeo de eventos de teclado para ejecutar el algoritmo
                if event.key == pygame.K_KP_ENTER and inicio and fin: #Se estableció la tecla Enter para ejecutar la funcion a_estrella
                    a_estrella(lambda: dibujar(ventana, grid, FILAS, ancho), grid, inicio, fin)
                elif event.key == pygame.K_ESCAPE: #Se estableció la tecla Escape para reiniciar el grid
                    grid = crear_grid(FILAS, ancho)
                    inicio = None
                    fin = None

    pygame.quit()

main(VENTANA, ANCHO_VENTANA)