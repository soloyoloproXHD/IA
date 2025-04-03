import cv2
import mediapipe as mp
import numpy as np

# Inicializar MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=2, 
                                  min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Captura de video
cap = cv2.VideoCapture(0)

# Lista de índices de landmarks específicos
selected_points = [33, 133, 362, 263, 61, 291, 70, 105, 107, 336, 334, 300, 4, 48, 278, 8, 374, 386, 159, 145, 13, 14, 50, 280]

def distancia(p1, p2):
    """Calcula la distancia euclidiana entre dos puntos."""
    return np.linalg.norm(np.array(p1) - np.array(p2))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Espejo para mayor naturalidad
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            puntos = {}
            
            for idx in selected_points:
                x = int(face_landmarks.landmark[idx].x * frame.shape[1])
                y = int(face_landmarks.landmark[idx].y * frame.shape[0])
                puntos[idx] = (x, y)
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)  # Dibuja el punto en verde
            
            # Calcular y mostrar distancias entre puntos clave
            if all(idx in puntos for idx in selected_points):
                d_ojo_izq = distancia(puntos[33], puntos[133])
                d_ojo_der = distancia(puntos[362], puntos[263])
                d_boca = distancia(puntos[61], puntos[291])
                d_ceja_izq = distancia(puntos[70], puntos[107])
                d_ceja_der = distancia(puntos[300], puntos[336])
                d_nariz = distancia(puntos[4], puntos[8])
                
                # Dibujar líneas entre puntos clave
                cv2.line(frame, puntos[4], puntos[8], (0, 255, 255), 2)  # Nariz

                # Obtener la posición del punto de la nariz (índice 4)
                if 4 in puntos:
                    x_nariz, y_nariz = puntos[4]
                    # Mostrar la posición en el marco
                    cv2.putText(frame, f"Nariz: ({x_nariz}, {y_nariz})", (10, 120), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

                if 13 and 14 and 61 and 291 and 107 and 336 and 133 and 362 in puntos:
                    # Encontrar los límites del área facial
                    x_min = min(p[0] for p in puntos.values())
                    x_max = max(p[0] for p in puntos.values())
                    y_min = min(p[1] for p in puntos.values())
                    y_max = max(p[1] for p in puntos.values())
                    
                    # área facial
                    ancho_facial = x_max - x_min
                    alto_facial = y_max - y_min
                    
                    # Coordenadas absolutas de los puntos
                    x_boca_izq, y_boca_izq = puntos[61]
                    x_boca_der, y_boca_der = puntos[291]
                    
                    x_labio_sup, y_labio_sup = puntos[13]
                    x_labio_inf, y_labio_inf = puntos[14]
                    
                    x_seja_izq, y_seja_izq = puntos[107]
                    x_seja_der, y_seja_der = puntos[336]
                    
                    x_ojo_izq, y_ojo_izq = puntos[133]
                    x_ojo_der, y_ojo_der = puntos[362]

                    
                    # Coordenadas relativas de los puntos
                    x_relativo_boca_izq = (x_boca_izq - x_min) / ancho_facial
                    y_relativo_boca_izq = (y_boca_izq - y_min) / alto_facial
                    x_relativo_boca_der = (x_boca_der - x_min) / ancho_facial
                    y_relativo_boca_der = (y_boca_der - y_min) / alto_facial
                    
                    x_relativo_labio_sup = (x_labio_sup - x_min) / ancho_facial
                    y_relativo_labio_sup = (y_labio_sup - y_min) / alto_facial
                    x_relativo_labio_inf = (x_labio_inf - x_min) / ancho_facial
                    y_relativo_labio_inf = (y_labio_inf - y_min) / alto_facial
                    
                    x_relativo_seja_izq = (x_seja_izq - x_min) / ancho_facial
                    y_relativo_seja_izq = (y_seja_izq - y_min) / alto_facial
                    x_relativo_seja_der = (x_seja_der - x_min) / ancho_facial
                    y_relativo_seja_der = (y_seja_der - y_min) / alto_facial
                    
                    x_relativo_ojo_izq = (x_ojo_izq - x_min) / ancho_facial
                    y_relativo_ojo_izq = (y_ojo_izq - y_min) / alto_facial
                    x_relativo_ojo_der = (x_ojo_der - x_min) / ancho_facial
                    y_relativo_ojo_der = (y_ojo_der - y_min) / alto_facial
                    
                    
                    
                    # Calcular distancias horizontal o vertical entre los puntos
                    distancia_horizontal_boca = abs(x_relativo_boca_der - x_relativo_boca_izq)
                    distancia_vertical_boca = abs(y_relativo_labio_sup - y_relativo_labio_inf) #Se calcula respecto de los labios
                    distancia_seja_ojo_izq = abs(y_relativo_seja_izq - y_relativo_ojo_izq)
                    distancia_seja_ojo_der = abs(y_relativo_seja_der - y_relativo_ojo_der)

                    promedio_seja_ojo = (distancia_seja_ojo_izq + distancia_seja_ojo_der) / 2
                    
                    # Depuración: Imprimir valores
                    print(f"Ancho Facial: {ancho_facial}")
                    print(f"Alto Facial: {alto_facial}")
                    print(f"Distancia Horizontal Boca: {distancia_horizontal_boca}")
                    print(f"Distancia Vertical Boca: {distancia_vertical_boca}")
                    print(f"Distancia Seja Ojo Izq: {distancia_seja_ojo_izq}")
                    print(f"Distancia Seja Ojo Der: {distancia_seja_ojo_der}")
                    print(f"Promedio Seja Ojo: {promedio_seja_ojo}")

                    # Clasificar la expresión facial
                    if distancia_horizontal_boca > 0.50:  # Umbral para sonrisa
                        emocion = "Feliz"
                    elif distancia_horizontal_boca < 0.45 and promedio_seja_ojo > 0.24:
                        emocion = "Triste"
                    elif distancia_vertical_boca > 0.10 and promedio_seja_ojo > 0.24:
                        emocion = "Sorpresa"
                    elif distancia_vertical_boca < 0.45 and promedio_seja_ojo < 0.24: 
                        emocion = "Enojo"
                    else:
                        emocion = "Neutral"
                    
                    cv2.putText(frame, f"Emocion: {emocion}", (10, 240), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    
                    cv2.putText(frame, f"Boca Iz Relativa: ({x_relativo_boca_izq:.2f}, {y_relativo_boca_izq:.2f})", (10, 180),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                    cv2.putText(frame, f"Boca Der Relativa: ({x_relativo_boca_der:.2f}, {y_relativo_boca_der:.2f})", (10, 210),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.imshow('PuntosFacialesMediaPipe', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()