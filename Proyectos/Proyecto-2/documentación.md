
# 📝 Documentación - Proyecto-2 💀

## Descripción General

Este proyecto consistio en implementar un juego en `pygame` donde un personaje debe esquivar balas mediante salto o movimiento lateral. El jugador puede controlar manualmente al personaje para recolectar datos de entrenamiento para posteriormente poder activar un modo automático con inteligencia artificial (IA) utilizando modelos de machine learning: red neuronal, árbol de decisión o KNN.

---

## Funciones principales necesarias para el uso de los modelos de IA

### `guardar_datos()`

Guarda ejemplos para entrenamiento de modelos. Cada entrada contiene los siguientes valores:
- `velocidad_bala`: velocidad actual de la bala horizontal.
- `distancia`: distancia horizontal entre el jugador y la bala.
- `distancia2`: distancia vertical entre el jugador y la segunda bala.
- `acción`: valor objetivo. Puede ser:
  - `0`: quedarse quieto
  - `1`: saltar
  - `2`: moverse a la izquierda
  - `3`: moverse a la derecha

> 💡 Se usa en modo manual para recolectar datos reales que alimentan los modelos IA.


```python
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
```


---

### 🧠 `red_neuronal()`

En esta funcion se entrena una red neuronal `MLPClassifier` con los datos recopilados al jugar en modo manual:
- Usa `StandardScaler` para normalizar las características.
- Arquitectura simple con una capa oculta de 30 neuronas.

Devuelve `True` si el modelo fue entrenado exitosamente.


```python
def red_neuronal():
    global datos_modelo, modelo_nn, menu_activo, scaler_nn
    
    if not datos_modelo:
        return False
    
    datos = np.array(datos_modelo, dtype=float)
    X = datos[:, :3]
    y = datos[:, 3].astype(int)
```


---

### 🌲 `generar_arbol_decision()`

Entrena un modelo de árbol de decisión (`DecisionTreeClassifier`) con los datos almacenados.

- Profundidad máxima limitada a 5 para evitar sobreajuste.


```python
def generar_arbol_decision():
    global datos_modelo, modelo_arbol
    
    if not datos_modelo:
        return False
    
    datos = np.array(datos_modelo, dtype=float)
    X = datos[:, :3]
    y = datos[:, 3].astype(int)
    
    modelo = DecisionTreeClassifier(max_depth=5)
    modelo.fit(X, y)
    modelo_arbol = modelo
    
    print("Árbol de decisión entrenado tilín.")
    #print("Datos recopilados para el modelo:", datos_modelo)
    #generar_arbol(datos_modelo, columnas, clases)
    return True
```


---

### 🏫🏫 `generar_knn()`

Entrena un modelo `KNeighborsClassifier` (KNN) con `n_neighbors=3`.

Se requiere que existan datos recopilados para funcionar.


```python
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
```


---

## 🎮 Funciones de juego y lógica

### `logica_auto(accion)`

Ejecuta acciones del jugador basadas en la predicción del modelo IA:
- `accion == 1`: saltar (si está en el suelo).
- `accion == 2`: moverse a la izquierda.
- `accion == 3`: moverse a la derecha.
- `accion == 0`: volver a posición central.

También llama a `manejar_salto()` si se activa el salto.


```python
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
```


---

## 📜 Menús del juego

Se utilizaron 2 menús, el menú principal es el de nos permite seleccionar entre el modo manual y los modos automaticos, el segundo se utiliza para seleccionar que modelo de IA se generará para jugar utilizando los datos recopilados en el modo manual.

### `mostrar_menu()`

Interfaz inicial donde el jugador elige:
- `A`: modo automático (redirige a `menu_modelos()`).
- `M`: modo manual (sin IA, permite recolectar datos).
- `Q`: salir del juego.


```python
def mostrar_menu():
    global menu_activo, modo_auto, modelo_nn
    pantalla.fill(NEGRO)
    texto = fuente.render("Presiona 'A' para Auto, 'M' para Manual, o 'Q' para Salir", True, BLANCO)
    pantalla.blit(texto, (w // 4, h // 2))
    pygame.display.flip()
```


---

### `menu_modelos()`

Permite seleccionar el modelo IA a usar:
- `1`: red neuronal.
- `2`: árbol de decisión.
- `3`: KNN.

Activa `modo_auto` si se genera exitosamente el modelo.


```python
def menu_modelos():
    global menu_activo, modo_auto, modelo_nn, m_arbol, m_knn, m_neuronal
    pantalla.fill(GRIS)
    pantalla.blit(fuente.render("1.- Red Neuronal", True, BLANCO), (w//4, h//5.5))
    pantalla.blit(fuente.render("2.- Arbol de Desición", True, BLANCO), (w//4, h//4))
    pantalla.blit(fuente.render("3.- K Neighborn", True, BLANCO), (w//4, h//3))
    pantalla.blit(fuente.render("ESC.- Regresar al menú anterior", True, BLANCO), (w//4, h//2))
    pygame.display.flip()
```


---

## ⚙️ Ejecución del modo automático

Cuando `modo_auto = True`, se realiza lo siguiente:
1. Se construye un vector de entrada: `[velocidad_bala, distancia_horizontal, distancia_vertical]`.
2. Se usa el modelo seleccionado para predecir la acción.
3. Se ejecuta `logica_auto(accion)` para realizar el movimiento correspondiente.
4. Se imprime la predicción en consola (debug).

> 💡 Esto simula una IA que aprende a esquivar balas observando situaciones pasadas.

---

## 🚀 Ejecución

El juego comienza con:

```python
if __name__ == "__main__":
    main()
```

Esto lanza la ventana, muestra el menú y gestiona el ciclo principal (`main()`), que:
- Captura eventos.
- Actualiza estados.
- Aplica lógica IA o entrada manual.
- Dibuja la escena.

# 💀 Conclusiones

Está como el diavlo usar la red neuronal `Serialice` para una IA que funcione clasificando clases, así que es mejor leer las notas antes de comenzar a usar la primera wea que uno se encuentra `MLPClassifier` esta mucho mas sencillo para poder hacer un modelo clasificador.

> Moraleja: Hay que leer antes de empezar a trabajar. 💀