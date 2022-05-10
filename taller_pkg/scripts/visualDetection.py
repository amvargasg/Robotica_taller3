#!/usr/bin/env python3

# Para usar ROS
import rospy
from std_msgs.msg import String
# Para procesar la imagen
from multiprocessing.connection import wait
import cv2
import numpy as np


class PubSub(object):

    def __init__(self):
        # Definicion del rango de la mascara
        self.azulBajo = np.array([100,100,20],np.uint8)
        self.azulAlto = np.array([125,255,255],np.uint8)
        self.amarilloBajo = np.array([15,100,20],np.uint8)
        self.amarilloAlto = np.array([45,255,255],np.uint8)
        self.redBajo1 = np.array([0,100,20],np.uint8)
        self.redAlto1 = np.array([8,255,255],np.uint8)
        self.redBajo2 = np.array([175,100,20],np.uint8)
        self.redAlto2 = np.array([179,255,255],np.uint8)

        # Definir la fuente que se va a utilizar para escribir en la imagen
        self.font = cv2.FONT_HERSHEY_SIMPLEX

        # Video a usar 0 significa camara integrada del pc, se puede pasar tambien la ruta de un video
        self.cap = cv2.VideoCapture(0)

        self.coordenadas = 0,0


        rospy.init_node('visual')
        self.color_sub = rospy.Subscriber('robot_manipulator/color',String, self.visualizar)
        self.target_pub = rospy.Publisher('robot_manipulator/goal', String, queue_size=10)


         
    def visualizar(self, msg):
        coord = self.transformar_Img(msg)
        #print('El centro esta en '+ str(coord))
        self.target_pub.publish(str(coord))


    def transformar_Img(self,data):
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        color = data.data


        # Lee el video cuadro por cuadro
        # ret: booleano que indica si está leyendo del marco (osea dentro de la imagen)
        # frame: matriz tridimencional con la info del cuadro (el color del pixel)
        ret,frame = self.cap.read()
        if ret == True:
            # Transformar al espacio de color de RGB a HSV
            frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

            # Crear las mascaras con los rangos de colorLow a colorHigh
            maskAzul = cv2.inRange(frameHSV,self.azulBajo,self.azulAlto)
            maskAmarillo = cv2.inRange(frameHSV,self.amarilloBajo,self.amarilloAlto)
            # Se tienen dos para el rojo porque se tiene que contar el espacio del inicio y del final del arreglo (que son rojos - ver imagen HSV)
            maskRed1 = cv2.inRange(frameHSV,self.redBajo1,self.redAlto1)
            maskRed2 = cv2.inRange(frameHSV,self.redBajo2,self.redAlto2)
            maskRed = cv2.add(maskRed1,maskRed2)
            
            # Se usa la funcion dibujar con la mascara definida para dibujar el contorno del color deseado
            if color == 'b':
                self.coordenadas = self.dibujar(maskAzul,(255,0,0), frame)
            elif color == 'y':
                self.coordenadas = self.dibujar(maskAmarillo,(0,255,255), frame)
            elif color == 'r':
                self.coordenadas = self.dibujar(maskRed,(0,0,255),frame)
                
            return self.coordenadas
            

    # Funcion que dibuja el contorno del objeto
    def dibujar(self,mask,color, frame):
        self.coordenadas = 0,0
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
                self.coordenadas = x,y
                # Se mejora la visualizacion del contorno
                nuevoContorno = cv2.convexHull(c)
                # Se dibuja un circulo en el centro del objeto y se escriben sus coordenadas
                cv2.circle(frame,(x,y),7,(0,255,0),-1)
                cv2.putText(frame,'{},{}'.format(x,y),(x+10,y), self.font, 0.75,(0,255,0),1,cv2.LINE_AA)
                # Se dibujan los contornos mejorados
                cv2.drawContours(frame, [nuevoContorno], 0, color, 3)
        return self.coordenadas


if __name__ == '__main__':
    try:
        a = PubSub()
        rospy.spin()
    except rospy.ROSInterruptException: pass

