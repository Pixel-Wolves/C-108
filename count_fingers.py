import cv2
import mediapipe as mp

cap = cv2.VideoCapture(1)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

tipIds = [4, 8, 12, 16, 20]

# Definir una función para contar dedos
def countFingers(image, hand_landmarks, handNo=0):
    # Obtener todos los puntos de referencia de la mano visible
    if hand_landmarks:
        landmarks=hand_landmarks[handNo].landmark
        print(landmarks)
        # Contar dedos
        fingers=[]
        for im_index in tipIds:
            # Obtener puntas de los dedos y valores de posición y
            finger_tip_y=landmarks[im_index].y
            finger_bottom_y=landmarks[im_index-2].y

            # Obtener punta del pulgar y valor de posición y
            thumb_tip_x=landmarks[im_index].x
            thumb_bottom_x=landmarks[im_index-2].x

            # Verificar si algun dedo esta abierto o cerrado
            if im_index!=4:
                if finger_tip_y<finger_bottom_y:
                    fingers.append(1)
                    print("El dedo con ID",im_index,"esta abierto")
                if finger_tip_y>=finger_bottom_y:
                    fingers.append(0)
                    print("El dedo con ID",im_index,"esta cerrado")
            else:
                if thumb_tip_x<thumb_bottom_x:
                    fingers.append(1)
                    print("El pulgar esta abierto")
                if thumb_tip_x>=thumb_bottom_x:
                    fingers.append(0)
                    print("El pulgar esta cerrado")
            
        total_fingers=fingers.count(1)
        print(total_fingers)
        text = f'Fingers: {total_fingers}' 
        cv2.putText(image, text, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

# Definir una función para
def drawHandLanmarks(image, hand_landmarks):

    # Dibujar conexiones entre los puntos de referencia
    if hand_landmarks:

      for landmarks in hand_landmarks:
               
        mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)


while True:
    success, image = cap.read()

    image = cv2.flip(image, 1)
    
    # Detectar los puntos de referencia de las manos
    results = hands.process(image)

    # Obtener la posición de los puntos de referencia del resultado procesado
    hand_landmarks = results.multi_hand_landmarks

    # Dibujar puntos de referencia
    drawHandLanmarks(image, hand_landmarks)

    # Obtener la posición de los dedos de la mano
    countFingers(image,hand_landmarks)

    cv2.imshow("Controlador de medios", image)

    # Cerrar la ventana al presionar la barra espaciadora
    key = cv2.waitKey(1)
    if key == 32:
        break

cv2.destroyAllWindows()
