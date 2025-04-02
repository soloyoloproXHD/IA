import cv2
import mediapipe as mp
import numpy as np

# Inicializar MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=2, 
                                  min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Captura de video
cap = cv2.VideoCapture(0)

# Lista de índices de landmarks específicos (ojos, boca, cejas y nariz)
selected_points = [33, 133, 362, 263, 61, 291, 70, 105, 107, 336, 334, 300, 4, 48, 278, 8]  # Ojos, boca, cejas y nariz

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
                
                # Calcular proporciones
                proporcion_ojos_boca = (d_ojo_izq + d_ojo_der) / (2 * d_boca)
                proporcion_cejas_nariz = (d_ceja_izq + d_ceja_der) / (2 * d_nariz)
                
                # Determinar simetría
                simetria = "Simetrica" if abs(d_ojo_izq - d_ojo_der) < 10 and abs(d_ceja_izq - d_ceja_der) < 10 else "No Simetrica"
                
                # Mostrar proporciones y simetría en el marco
                cv2.putText(frame, f"Proporcion Ojos-Boca: {proporcion_ojos_boca:.2f}", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                cv2.putText(frame, f"Proporcion Cejas-Nariz: {proporcion_cejas_nariz:.2f}", (10, 60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                cv2.putText(frame, f"Simetria: {simetria}", (10, 90), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                
                # Dibujar líneas entre puntos clave
                cv2.line(frame, puntos[33], puntos[133], (23, 255, 23), 2)  # Ojo izquierdo
                cv2.line(frame, puntos[362], puntos[263], (23, 255, 23), 2)  # Ojo derecho
                cv2.line(frame, puntos[61], puntos[291], (23, 255, 23), 2)  # Boca
                cv2.line(frame, puntos[4], puntos[8], (0, 255, 255), 2)  # Nariz

    cv2.imshow('PuntosFacialesMediaPipe', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()