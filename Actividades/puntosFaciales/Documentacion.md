




# Modelar un proceso para la detección de vida

## ¿Cuales son los parametros que tomaria para poder identificar que lo que se está viendo es alguien vivo (gestos, emociones, acciones) y no una imagen?

### Parametros a considerar:
>- Coordenada de los punto en el area facial dependiendo de la          emoción o accción.
>- Distancia entre dos o más puntos de varias zonas caracteristicas como lo son las sejas, barbilla y boca.
>- Cambios de iluminación frame x frame.
    
## Cuantos puntos son requeridos?
> Esto depende de cuales zonas del rostro se tomarán en cuenta. Por ejemplo, algúnas de las zonas mas relevantes a tomar en cuenta son las siguientes:
> - Sejas
> - Boca
> - Barbilla
> - Ojos

## ¿Cuales son los puntos que mas información nos dan?
> Clasificando por zona los puntos que mas información pueden proporcionar son los siguientes:
> - Boca (La forma de la boca cambia con las emociones como felicidad, enojo, sorpresa):
>   - Labios
> - Ojos:
Al igual que la boca, los ojos tienen variacion en su forma, en este caso es en la apertura de los ojos, variando la apertura de estos (más especificamente los parpados), estos cambios son muy notorios con la felicidad, la sorpresa y la fatiga.
>   - Parpados
>   - Pupilas

Cual sería una de las mejores estrategias para que un sistema de reconocimiento facial no sea violado?
