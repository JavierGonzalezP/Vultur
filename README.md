# **Bienvenidos al repositorio de Vultur**🚀
 **Por favor leer todas las instrucciones**
# **Estructura de Scripts**
El sistema de Vultur está conformado por una serie de scripts desarrollados en Python que pueden ser ejecutados según la necesidad del operador.
- **Interfaz**: el script "interfaz.py" ejecuta una interfaz gráfica en la cual el operador puede interactuar mediante botones para ejecutar scripts o hacer configuraciones en los parámetros de las cámaras.
- **Detectar Cámaras**: dentro de la interfaz, si se pulsa el botón "Detectar Cámaras" se ejecuta script "detectar_camaras.py" que detecta si se tienen conectadas cámaras en la Raspberry e imprime el resultado enumerandolas junto con su modelo e ID.
- **Configurar parámetros**:  dentro de la interaz, si se pulsa el botón "Configurar Cámaras" se ejecuta el script "configurar_camaras.py" que abre una ventana en la cual se pueden configurar los parámetros de las cámaras escenciales para la captura de imágenes. Estas configuraciones se guardan en el archivo "config.json".
-**Capturar Imágenes**: dentro de la interfaz, si se pulsa el botón "Capturar Imágenes" se ejecuta el script "capturar_imagenes_gps.py" que se encarga de hacer la conexión al Pixhawk con el GPS y luego iniciar la captura de imágenes. En caso de que el Pixhawk no realice la conexión con la Raspberry o el GPS no se encuentre funcionando, el script continua de todas formas con la captura de imágenes sin datos GPS. Además, el script guarda la posición GPS de cada imagen en un archivo "capturar_imagenes.xlsx".

  
