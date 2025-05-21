import pygame
import random
import cv2 as cv
import numpy as np
#from arbolDecision import generar_arbol
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras import Input
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier



# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
w, h = 1280, 720
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego: Disparo de Bala, Salto, Nave y Menú")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = '#1E1E1E'

# Variables del jugador, bala, nave, fondo, etc.
jugador = None
bala = None
fondo = None
nave = None
menu = None

velocidad_jugador = 5

# Variables de salto
salto = False
salto_altura = 17  # Velocidad inicial de salto
gravedad = 1
en_suelo = True

# Variables de pausa y menú
pausa = False
fuente = pygame.font.SysFont('Arial', 24)
menu_activo = True
modo_auto = False  # Indica si el modo de juego es automático

# Lista para guardar los datos de velocidad, distancia y salto (target)
datos_modelo = []

run_img = pygame.image.load('assets/knight/Knight_1/Run.png')

w_p, w_d = 71, 55
h_p, h_d = 86, 50
n_f = 7

# Cargar las imágenes
jugador_frames = []
for i in range(n_f):
    frame = run_img.subsurface(pygame.Rect(i * w_p, 0, w_p, h_p))
    # Escalamos ahora a (w_p, h_p) en lugar de (w_p*2, h_p*2)
    frame = pygame.transform.scale(frame, (w_p, h_p))
    jugador_frames.append(frame)

bala_img = pygame.image.load('assets/sprites/purple_ball.png')
bala2_img = pygame.image.load('assets/sprites/purple_ball.png')
fondo_img = pygame.image.load('assets/game/sky_bridge.png')
img = pygame.image.load('assets/game/dragon.png')
nave_img = img.subsurface(pygame.Rect(65, 60, w_d, h_d))
nave_img = pygame.transform.scale(nave_img, (w_d * 1.5, h_d * 1.5))
menu_img = pygame.image.load('assets/game/menu.png')

# Escalar la imagen de fondo para que coincida con el tamaño de la pantalla
fondo_img = pygame.transform.scale(fondo_img, (w, h))

# Crear el rectángulo del jugador y de la bala
jugador = pygame.Rect(50, h - 100, 32, 48)
bala = pygame.Rect(w - 50, h - 90, 16, 16)
bala2 = pygame.Rect(w//16, h//8, 16, 16)
nave = pygame.Rect(w - 100, h - 100, 64, 64)
menu_rect = pygame.Rect(w // 2 - 135, h // 2 - 90, 270, 180)  # Tamaño del menú

# Variables para la animación del jugador
current_frame = 0
frame_speed = 15  # Cuántos frames antes de cambiar a la siguiente imagen
frame_count = 0

# Variables para la bala
velocidad_bala = -10  # Velocidad de la bala hacia la izquierda
bala_disparada = False

velocidad_bala2 = 8
bala_disparada2 = False

# Variables para el fondo en movimiento
fondo_x1 = 0
fondo_x2 = w

# Ajustar el desplazamiento para centrar el asset en la hitbox sin mover la posición:
offset_x = (jugador.width - w_p) // 2
offset_y = jugador.height - h_p


modelo_nn = None
modelo_arbol = None
modelo_knn = None

def red_neuronal():
    global modelo_nn
    datos = np.array(datos_modelo, dtype=float)
    X = datos[:, :3]
    y = datos[:, 3].astype(int)
    
    from tensorflow.keras.utils import to_categorical

    y_cat = to_categorical(y, num_classes=4)
    
    modelo = Sequential([
        Input(shape=(X.shape[1],)),
        Dense(64, activation='sigmoid'),
        Dense(32, activation='sigmoid'),
        Dense(4, activation='softmax'),
    ])
    
    modelo.compile(optimizer='adam',
                   loss='categorical_crossentropy',
                   metrics=['accuracy'])
    
    print("Entrenando red neuronal…")
    modelo.fit(X, y_cat, epochs=200, batch_size=32, verbose=1)
    modelo_nn = modelo
    print("Entrenamiento completado.")

def generar_arbol_decision():
    global datos_modelo, modelo_arbol
    
    if not datos_modelo:
        print("No hay datos suficientes para generar el árbol de decisión.")
        return
    datos = np.array(datos_modelo, dtype=float)
    X = datos[:, :3]
    y = datos[:, 3].astype(int)
    
    modelo = DecisionTreeClassifier(max_depth=5)
    modelo.fit(X, y)
    modelo_arbol = modelo
    
    print("Árbol de decisión entrenado tilín.")
    #print("Datos recopilados para el modelo:", datos_modelo)
    #generar_arbol(datos_modelo, columnas, clases)

def generar_knn():
    global datos_modelo, modelo_knn
    
    if not datos_modelo:
        print("No hay datos suficientes para generar el KNN.")
        return
    
    datos = np.array(datos_modelo, dtype=float)
    X = datos[:, :3]
    y = datos[:, 3].astype(int)
    
    modelo = KNeighborsClassifier(n_neighbors=3)
    modelo.fit(X, y)
    
    modelo_knn = modelo
    print("KNN entrenado tilín.")

# Función para disparar la bala
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-8, -3)  # Velocidad aleatoria negativa para la bala
        bala_disparada = True

def disparar_segunda_bala():
    global bala_disparada2, velocidad_bala2
    if not bala_disparada2:
        bala_disparada2 = True

# Función para reiniciar la posición de la bala
def reset_bala():
    global bala, bala_disparada
    bala.x = w - 50  # Reiniciar la posición de la bala
    bala_disparada = False
    
def reset_bala2():
    global bala2, bala_disparada2
    # Reiniciar la posición de la segunda bala
    bala2.y = h//8
    bala_disparada2 = False

# Función para manejar el salto
def manejar_salto():
    global jugador, salto, salto_altura, gravedad, en_suelo

    if salto:
        jugador.y -= salto_altura  # Mover al jugador hacia arriba
        salto_altura -= gravedad  # Aplicar gravedad (reduce la velocidad del salto)

        # Si el jugador llega al suelo, detener el salto
        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto = False
            salto_altura = 17  # Restablecer la velocidad de salto
            en_suelo = True

# Función para actualizar el juego
def update():
    global bala, bala2, velocidad_bala, velocidad_bala2, current_frame, frame_count, fondo_x1, fondo_x2, modelo_nn, modelo_arbol

    # Mover el fondo
    fondo_x1 -= 1
    fondo_x2 -= 1

    # Si el primer fondo sale de la pantalla, lo movemos detrás del segundo
    if fondo_x1 <= -w:
        fondo_x1 = w

    # Si el segundo fondo sale de la pantalla, lo movemos detrás del primero
    if fondo_x2 <= -w:
        fondo_x2 = w

    # Dibujar los fondos
    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

    # Animación del jugador
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0

    # Dibujar el jugador con la animación, aplicando el desplazamiento
    pantalla.blit(jugador_frames[current_frame], (jugador.x + offset_x, jugador.y + offset_y))

    # Dibujar la nave
    pantalla.blit(nave_img, (nave.x, nave.y))

    # Mover y dibujar la bala
    if bala_disparada:
        bala.x += velocidad_bala
    if bala_disparada2:
        bala2.y += velocidad_bala2

    # Si la bala sale de la pantalla, reiniciar su posición
    if bala.x < 0:
        reset_bala()
    if bala2.y > h:
        reset_bala2()

    pantalla.blit(bala_img, (bala.x, bala.y))
    pantalla.blit(bala2_img, (bala2.x, bala2.y))

    # Colisión entre la bala y el jugador
    if (jugador.colliderect(bala) and modo_auto) or (jugador.colliderect(bala2) and modo_auto):
        modelo_nn = None
        modelo_arbol = None
        print("Colisión detectada!")
        reiniciar_juego()  # Terminar el juego y mostrar el menú
    
    if jugador.colliderect(bala) or jugador.colliderect(bala2):
        print("Colisión detectada!")
        reiniciar_juego()  # Terminar el juego y mostrar el menú

# Función para guardar datos del modelo en modo manual
def guardar_datos():
    global jugador, bala, bala2, velocidad_bala, salto
    
    distancia = abs(jugador.x - bala.x)  # Distancia entre el jugador y la bala
    distancia2 = abs(jugador.y - bala2.y)
    
    accion = 0
    
    if salto:
        accion = 1
    else:
        
        if jugador.x < 50 - jugador.width//2:
            accion = 2
        if jugador.x > 50 + jugador.width//2:
            accion = 3
    
    # Guardar velocidad de la bala, distancia vertical y horizontal y la acción
    datos_modelo.append([velocidad_bala, distancia, distancia2, accion])

# Función para pausar el juego y guardar los datos
def pausa_juego():
    global pausa
    pausa = not pausa
    if pausa:
        print("Juego pausado. Datos registrados hasta ahora:", datos_modelo)
    else:
        print("Juego reanudado.")

# Función para mostrar el menú y seleccionar el modo de juego
def mostrar_menu():
    global menu_activo, modo_auto
    pantalla.fill(NEGRO)
    texto = fuente.render("Presiona 'A' para Auto, 'M' para Manual, o 'Q' para Salir", True, BLANCO)
    pantalla.blit(texto, (w // 4, h // 2))
    pygame.display.flip()

    while menu_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:
                    #modo_auto = True
                    #menu_activo = False
                    menu_modelos()
                elif evento.key == pygame.K_m:
                    modo_auto = False
                    menu_activo = False
                    datos_modelo = None
                elif evento.key == pygame.K_q:
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    red_neuronal()

def menu_modelos():
    global menu_activo, modo_auto, modelo_nn
    pantalla.fill(GRIS)
    pantalla.blit(fuente.render("1.- Red Neuronal", True, BLANCO), (w//4, h//5.5))
    pantalla.blit(fuente.render("2.- Arbol de Desición", True, BLANCO), (w//4, h//4))
    pantalla.blit(fuente.render("3.- K Neighborn", True, BLANCO), (w//4, h//3))
    pygame.display.flip()

    # Bucle hasta pulsar 1-4 o cerrar
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1:
                    red_neuronal()
                    modo_auto = True
                    menu_activo = False
                    return
                elif e.key == pygame.K_2:
                    generar_arbol_decision()
                    modo_auto = True
                    menu_activo = False
                    return
                elif e.key == pygame.K_3:
                    generar_knn()
                    modo_auto = True
                    menu_activo = False
                    return
                # elif para K_3

# Función para reiniciar el juego tras la colisión
def reiniciar_juego():
    global menu_activo, jugador, bala, nave, bala_disparada, salto, en_suelo
    menu_activo = True  # Activar de nuevo el menú
    jugador.x, jugador.y = 50, h - 100  # Reiniciar posición del jugador
    bala.x = w - 50  # Reiniciar posición de la bala
    bala2.y = h//8  # Reiniciar posición de la segunda bala
    nave.x, nave.y = w - 100, h - 100  # Reiniciar posición de la nave
    bala_disparada = False
    salto = False
    en_suelo = True
    # Mostrar los datos recopilados hasta el momento
    print("Datos recopilados para el modelo: ", datos_modelo)
    mostrar_menu()  # Mostrar el menú de nuevo para seleccionar modo

def logica_auto(accion):
    global salto, en_suelo
    if accion == 1 and en_suelo:  # Esquivar bala
        salto = True
        en_suelo = False
    if accion == 2:  # Esquivar bala2
        jugador.x = max(0, jugador.x - velocidad_jugador)  # Moverse hacia la izquierda
    if accion == 3:
        jugador.x = min(w//10, jugador.x + velocidad_jugador)  # Moverse hacia la derecha
    if accion == 0:
        # Volver al centro si no hace nada
        if jugador.x < 50:
            jugador.x = min(50, jugador.x + velocidad_jugador)
        elif jugador.x > 50:
            jugador.x = max(50, jugador.x - velocidad_jugador)
                    
    if salto:
        manejar_salto()

def main():
    global salto, en_suelo, bala_disparada

    reloj = pygame.time.Clock()
    mostrar_menu()  # Mostrar el menú al inicio
    correr = True

    while correr:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo and not pausa:  # Detectar la tecla espacio para saltar
                    salto = True
                    en_suelo = False
                if evento.key == pygame.K_p:  # Presiona 'p' para pausar el juego
                    pausa_juego()
                    mostrar_menu()
                if evento.key == pygame.K_q:  # Presiona 'q' para terminar el juego
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()

        if not pausa:
            
            if not modo_auto:
                
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    jugador.x = max(0, jugador.x - velocidad_jugador)
                elif keys[pygame.K_RIGHT]:
                    jugador.x = min(w//10, jugador.x + velocidad_jugador)
                else:
                    if jugador.x < 50:
                        jugador.x = min(50, jugador.x + velocidad_jugador)
                    elif jugador.x > 50:
                        jugador.x = max(50, jugador.x - velocidad_jugador)
                
                if salto:
                    manejar_salto()
                # Guardar los datos si estamos en modo manual
                guardar_datos()
            
            else:
                x_input = np.array([[velocidad_bala, abs(jugador.x - bala.x), abs(jugador.y - bala2.y)]])
                accion = None
                if modelo_nn:
                    
                    pred = modelo_nn.predict(x_input, verbose=0)[0]
                    accion = np.argmax(pred)
                    
                    logica_auto(accion)
                    print("Vector de salidas de la red neuronal:", pred)
                    print("Predicción de la red neuronal:", accion)

                    
                elif modelo_arbol:
                    accion = modelo_arbol.predict(x_input)[0]
                    
                    logica_auto(accion)
                    print("Predicción del árbol de decisión:", accion)
                    
                elif modelo_knn:
                    accion = modelo_knn.predict(x_input)[0]
                    logica_auto(accion)
                    print("Predicción del KNN:", accion)
                    
                    


            # Actualizar el juego
            if not bala_disparada:
                disparar_bala()
            if not bala_disparada2:
                disparar_segunda_bala()
            update()

        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(60)  # Limitar el juego a 30 FPS

    pygame.quit()

if __name__ == "__main__":
    main()



