# Modelar una red neuronal que pueda identificar emociones a travéz de los valores obtenidos de los landmarks que genera mediapipe.

## Alumno: Cornejo Cornejo Hiram Abif

- ## Definir el tipo de red neuronal y describir cada una de sus partes.
<div align="justify">
    Una opcion podría ser utilizar una Perceptrón Multicapa (MLP) ya que esta es capaz de realizar tareas de clasificación y regresión. Esto es importante debido a que algo esencial para poder detectar emociones seria poder clasificar estas mismas.
</div>

- ### Partes de su Estructura:
    - Capa de Entrada
    > En esta capa se reciben los valores de los landmarks faciales detectados por mediapipe.
    Ahora, debemos tomar en cuenta que mediapipe tiene 468 puntos y cada punto nos proporciona una coordenada con los parametros *x*, *y*, *z* (3 parametros). Por lo que la capa de entrada tendria 1404 neuronas (esto puede variar).
- Definir los patrones a utilizar.
    - Landmaks Faciales
    > En este caso los patrones serian las coordenadas de cada punto de las landmaks, pero, esto puede ser fraccionado a utilizar solamente los puntos clave por sección de interes, como lo son, las **sejas**, **ojos**, **boca**, **mejillas** e iclusive la **nariz** podría ser una sección determinante.
    Suponiendo que utilizamos todos los puntos (porque no se cuantos puntos tenga cada sección para hacer algún subconjunto ahora xD) y cada punto nos da 3 parametros (x,y,z) de los cuales hay **468** puntos, entonces cada pátron de entrada seria un vector de **1404** valores.

    En este caso las coordenadas seria obtimo si se normalizan para tener valores entre **0** y **1** ó **-1** y **1**.

- Definir que  fúncion de activación es necesaria para este problema.
    - ReLu: Esta ayuda a aprender por medio de representaciónes no lineales de los datos.
    -  Softmax: En este caso como el **problema** es de **clasificación multiclase** este convierte las salidas en probabilidades.
- Definir el número máximo de entradas.
    - 1404
    >El numero máximo de valores que recibiria la red en este caso, considerando que asumimos el uso de los 468 puntos de **Mediapipe**, cada uno con sus 3 valores, el numero máximo de entradas seria:

        - 468 puntos * 3 valores = 1404 entradas

    > Nota: Este valor se podría reducir vastante utilizando solamente un subconjunto de puntos que represente las sección de interes.
- ¿Qué valores a la salida de la red podrían esperar?
    - Numero de Salidas
    > EL numero de salidas creo que variaria dependiendo de cuantas emociones son las que de quieren detectar suponiendo que queremos detectar **felicidad**, **enojo** y **sorpresa** entonces tendriamos **3** salidas, definiendo así una salida para cada emoción.
    Para este problema los valores de salida serían una **probabilidad** o **predicción** que representaria la "posibilidad" de que la entrada (en este caso un rostro) corresponda a determinada emoción.
- ¿Cuáles son los valores máximos que puede tener el bias?