#!/usr/bin/env python3

########### Descripcion ##############
# Este nodo se encarga de publicar el color del ping pong que se debe coger
# Toma la entrada del teclado 'y' para amarillo, 'b' para azul y 'r' para rojo
# Se envia el mensaje con la letra presionada hasta que se presione nuevamente otra tecla valida

# Para usar ros
import rospy
from std_msgs.msg import String
# Manejo de las acciones del teclado 
from pynput.keyboard import Key, Listener

# Variables globales
current_msg = ""

# define key press event callback
# Metodo que se encarga las acciones al robot donde se define el color con las teclas y b r
# Cambia el mensaje a enviar si se presiona: y b r
def on_press(key):
    global current_msg
    try:
        k = key.char  # single-char keys
        if k=='y' or k=='b' or k=='r' :
            current_msg = k
        else:
            print('Invalid key. To send a color please press y, b or r')
            
    except:
        k = key.name  # other keys
        print('Invalid key. To send a color please press y, b or r')
    
    print(k)

# define key release event callback
#Metodo que se encarga de las acciones del robot, en donde se si no se presiona tecla se queda con el ultimo color presionado
def on_release(key):
    global current_msg
    print(current_msg)
    

def color():
    # setup ros publisher
    pub = rospy.Publisher('robot_manipulator/color', String, queue_size=10)
    rospy.init_node('color', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    # setup keyboard listener
    listener = Listener(on_press=on_press, on_release=on_release, suppress=False)
    listener.start()
    while not rospy.is_shutdown():
        rospy.loginfo(current_msg)
        pub.publish(current_msg)
        print(current_msg)
        rate.sleep()


if __name__ == '__main__':
    try:
        color()
    except rospy.ROSInterruptException:
        pass
