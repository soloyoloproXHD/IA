# Informe: Modelos para implementar en Pasher

## Introducción
El problema planteado consiste en determinar si es posible utilizar un modelo de regresión lineal para predecir el momento adecuado en el que un personaje debe saltar un obstáculo que se aproxima a diferentes velocidades. Además, se explorarán otros modelos alternativos que podrían ser utilizados para resolver este problema, descartando el uso de redes neuronales y árboles de decisión.

## Uso de Regresión Lineal para Phaser con pygame
La regresión lineal es un modelo estadístico que busca establecer una relación lineal entre una variable dependiente y una o más variables independientes. En este caso, podríamos intentar modelar la relación entre la velocidad del obstáculo y el tiempo óptimo para saltar.

Algunas posibles limitaciones son las siguientes:

- **Relación no lineal**: La relación entre la velocidad del obstáculo y el momento de salto puede no ser estrictamente lineal, especialmente si se consideran factores como la aceleración o la distancia inicial.
- **Factores adicionales**: El modelo no puede manejar fácilmente otros factores relevantes, como la altura del obstáculo o las capacidades físicas del personaje.

Por lo tanto, aunque es posible utilizar un modelo de regresión lineal, su precisión y utilidad pueden ser limitadas en este caso.

Retomando la clase, el profesor ha indicado que se es posible, pero en efecto, su precisión dejaria que desear.

## Modelos Alternativos
Existen otros modelos que podrían llegar a funcionar:

1. **Máquinas de Soporte Vectorial (SVM)**: Las SVM pueden ser útiles para modelar relaciones no lineales mediante el uso de kernels. Esto permitiría capturar patrones más complejos entre las variables.

2. **Regresión Polinómica**: Una extensión de la regresión lineal que permite modelar relaciones no lineales al incluir términos polinómicos. Esto podría ser útil si la relación entre las variables sigue un patrón predecible.

## Conclusión
Aunque es posible utilizar un modelo de regresión lineal, su efectividad puede ser limitada debido a la naturaleza potencialmente no lineal de la relación entre las variables.