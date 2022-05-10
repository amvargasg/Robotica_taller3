
#!/usr/bin/env python3

import cv2
import numpy as np

# Funcion que dibuja el contorno del objeto
def dibujar(mask,color):
  # Esta funcion retorna dos valores, solo importa el primero que es seran los contornos
  contornos,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  # Se recorren los contornos para encontrar aquellos cuya area sea mayor a 3000 pixeles
  for c in contornos:
    area = cv2.contourArea(c)
    if area > 3000:
      # Se encuentran los momentos del contorno para encontrar el centro (para que no haya division entre 0 se pone el if)
      M = cv2.moments(c)
      if (M["m00"]==0): M["m00"]=1
      x = int(M["m10"]/M["m00"])
      y = int(M['m01']/M['m00'])
      print('Coordenadas: ')
      print(str(x) + ',' + str(y))
      # Se mejora la visualizacion del contorno
      nuevoContorno = cv2.convexHull(c)
      # Se dibuja un circulo en el centro del objeto y se escriben sus coordenadas
      cv2.circle(frame,(x,y),7,(0,255,0),-1)
      cv2.putText(frame,'{},{}'.format(x,y),(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
      # Se dibujan los contornos mejorados
      cv2.drawContours(frame, [nuevoContorno], 0, color, 3)

# Video a usar 0 significa camara integrada del pc, se puede pasar tambien la ruta de un video
cap = cv2.VideoCapture(0)

# Definicion del rango de la mascara
azulBajo = np.array([100,100,20],np.uint8)
azulAlto = np.array([125,255,255],np.uint8)
amarilloBajo = np.array([15,100,20],np.uint8)
amarilloAlto = np.array([45,255,255],np.uint8)
redBajo1 = np.array([0,100,20],np.uint8)
redAlto1 = np.array([8,255,255],np.uint8)
redBajo2 = np.array([175,100,20],np.uint8)
redAlto2 = np.array([179,255,255],np.uint8)

# Definir la fuente que se va a utilizar para escribir en la imagen
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
  # Lee el video cuadro por cuadro
  # ret: booleano que indica si está leyendo del marco (osea dentro de la imagen)
  # frame: matriz tridimencional con la info del cuadro (el color del pixel)
  ret,frame = cap.read()
  if ret == True:
    # Transformar al espacio de color de RGB a HSV
    frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # Crear las mascaras con los rangos de colorLow a colorHigh
    maskAzul = cv2.inRange(frameHSV,azulBajo,azulAlto)
    maskAmarillo = cv2.inRange(frameHSV,amarilloBajo,amarilloAlto)
    # Se tienen dos para el rojo porque se tiene que contar el espacio del inicio y del final del arreglo (que son rojos - ver imagen HSV)
    maskRed1 = cv2.inRange(frameHSV,redBajo1,redAlto1)
    maskRed2 = cv2.inRange(frameHSV,redBajo2,redAlto2)
    maskRed = cv2.add(maskRed1,maskRed2)

    # Se usa la funcion dibujar con la mascara definida para dibujar el contorno del color deseado
    dibujar(maskAzul,(255,0,0))
    dibujar(maskAmarillo,(0,255,255))
    dibujar(maskRed,(0,0,255))

    # Mostrar la imagen en una ventana
    cv2.imshow('frame',frame)

    # Espera la entrada del teclado, cuando es s se para el while y se cierran las ventanas
    if cv2.waitKey(1) & 0xFF == ord('s'):
      break
cap.release()
cv2.destroyAllWindows()

