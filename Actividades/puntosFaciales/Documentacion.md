




# Modelar un proceso para la detección de vida

## ¿Cuáles son los parametros que tomaria para poder identificar que lo que se está viendo es alguien vivo (gestos, emociones, acciones) y no una imagen?

### Parametros a considerar:
>- Coordenada relativa de los punto en el area facial determinada dependiendo de la emoción o accción.
>- Distancia entre dos o más puntos (con las coordenadas relativas) de varias zonas caracteristicas como lo son las sejas, parpados, labios, bordes de la boca, etc.
    
## ¿Cuántos puntos son requeridos?
> <div align="justify"> Esto depende de cuales zonas del rostro se tomarán en cuenta. Por ejemplo, algúnas de las zonas mas relevantes a tomar en cuenta son las siguientes: </div>
>
> - Sejas
> - Boca (labios y bordes)
> - Mejillas
> - Ojos (parpados)

## ¿Cuales son los puntos que mas información nos dan?
> Clasificando por zona los puntos que mas información pueden proporcionar son los siguientes:
> - Boca (La forma de la boca cambia con las emociones como felicidad, enojo, tristeza, sorpresa):
> - Ojos (Los parpados son un punto importante a tomar en cuenta.)
> - Sejas

> <div align="justify">Al igual que la boca, los ojos tienen variacion en su forma, en este caso es en la apertura de los ojos, variando la apertura de estos (más especificamente los parpados), estos cambios son muy notorios con la felicidad, la sorpresa y la fatiga.<div>
>   - Parpados
>   - Pupilas (Estas pueden ser usadas para determinar si es algo vivo lo que se está capturando)

## ¿Cual sería una de las mejores estrategias para que un sistema de reconocimiento facial no sea violado?
