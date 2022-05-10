# Robotica_taller3 - Grupo 12

Antes de empezar: Se descarga el paquete que se encuentra en este repositorio

Requerimientos: Se requiere tener tanto ROS como Python instalado para el debido funcionamiento, se requiere tener instaladas las siguientes librerias de python: OpenCV, pynput, numpy, tkinter y matplotlib

Pasos: El primer paso es abrir una terminal, en la cual se debe inicializar ROS con el comando Roscore

En una diferente terminal se abre el workspace cd catkin_ws(el nombre del work space es definido por el usuario utilizando el paquete) y correr el comando source devel/setup.bash el cual carga las dependencias de Ros y del paquete creado

Se deben dirigir a la carpeta contendido los códigos con el comando cd scripts. Una vez ahi se deben permisos a los archivos .py con el comando

    chmod +x archivo.py

Punto 1: 

Punto 2: Para ejecutar este punto se deben correr los scripts interfaz.py y el script de arduino. El arduino publica los cambios de posiciones en los angulos en en topico robot_angulo por medio del cual se puede hacer la grafica en el plano tridimensional. El comando para correrlos es rosrun taller_pkg interfaz.py y rosrun taller_pkg planner.py Se debe estar corriendo el planner al momento de introducir las coordenadas para que no se pierda la instruccion.

Punto 3: Para ejecutar este punto se deben correr los scripts goal.py y planner.py, en el goal se espera una entrada del usuario por medio de la consola con las cooordenadas que son el objetivo, estas son publicadas en un topico al que se sucribe el nodo del planner.py. El comando para correrlos es rosrun taller_pkg goal.py y rosrun taller_pkg serial_node.py /dev/ttyUSB0 (siendo este ultimo parametro el puerto usado por el arduino) Se debe estar corriendo el planner al momento de introducir las coordenadas para que no se pierda la instruccion.

Punto 4: Para ejecutar este punto se deben correr los scripts color.py, visualDetection.py y planner.py. En el nodo color se espera que el usuario presione una de las siguientes teclas: b,r,y. Cada una de estas corresponde a un color, el mensaje de ese color se publica en el topico al que el nodo visual se suscribe en el script visualDetection.py. Una vez definido el color se crea la mascara para analizar la imagen de la camara, luego se encuentran los momentos de los contornos de las figuras con ese color en la imagen y se obtiene las coordenadas del centro de esa figura. Esta coordenada se publica para que el nodo planner pueda planear la ruta del manipulador para llegar a la coordenada dada. El comando para correrlos es rosrun taller_pkg color.py , rosrun taller_pkg visualDetection.py y rosrun taller_pkg planner.py Se debe correr en ese orden porque en es en ese orden en el que se obtienen los mensajes.
