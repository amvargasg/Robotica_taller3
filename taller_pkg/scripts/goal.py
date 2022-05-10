#!/usr/bin/env python3

########### Descripcion ##############
# Este nodo se encarga de publicar el la coordenada objetivo
# Toma la entrada del teclado 
# Se envia el mensaje con la letra presionada hasta que se presione nuevamente otra tecla valida

# Para usar ros
import rospy
from std_msgs.msg import String

# Variables globales
coordenada = ""
    

def goal():
    # setup ros publisher
    pub = rospy.Publisher('robot_manipulator/goal', String, queue_size=10)
    rospy.init_node('goal', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    
    while not rospy.is_shutdown():
        # Wait for user input
        coordenada = input()
        rospy.loginfo(coordenada)
        pub.publish(coordenada)
        print(coordenada)
        rate.sleep()


if __name__ == '__main__':
    try:
        goal()
    except rospy.ROSInterruptException:
        pass
