import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import sys
import io
import signal
import RPi.GPIO as GPIO

class InterfazApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interfaz de Ejecución de Códigos")
        
        # Ajustar el tamaño de la ventana para la resolución 320x480
        self.root.geometry("480x300")

        # Variable para almacenar el proceso del script de captura
        self.capture_process = None

        # Crear un marco para los botones (a la izquierda)
        self.frame_botones = tk.Frame(root)
        self.frame_botones.grid(row=0, column=0, padx=10, pady=10)

        # Botones para ejecutar los scripts
        tk.Button(self.frame_botones, text="Detectar Cámaras", command=self.detectar_camaras, height=2, width=20).grid(row=0, column=0, pady=5)
        tk.Button(self.frame_botones, text="Abrir Configuración", command=self.abrir_configuracion, height=2, width=20).grid(row=1, column=0, pady=5)
        tk.Button(self.frame_botones, text="Capturar Imágenes", command=self.capturar_imagenes, height=2, width=20).grid(row=2, column=0, pady=5)
        tk.Button(self.frame_botones, text="Detener Captura", command=self.detener_captura, height=2, width=20).grid(row=3, column=0, pady=5)

        # Crear un marco para la consola (a la derecha)
        self.frame_consola = tk.Frame(root)
        self.frame_consola.grid(row=0, column=1, padx=30, pady=5)

        # Consola para mostrar salida del script, ajustada al tamaño de pantalla
        self.text_console = tk.Text(self.frame_consola, height=20, width=35, font=("Helvetica", 8))
        self.text_console.grid(row=0, column=0, pady=5)

        # Redirigir la salida estándar a la consola
        sys.stdout = self

        # Configuración del GPIO para el pulsador de captura
        GPIO.setmode(GPIO.BCM)
        self.pulsador_gpio = 13  # Elige un pin GPIO para el pulsador
        GPIO.setup(self.pulsador_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Configura el pulsador con pull-up

        # Detectar evento en el GPIO para ejecutar el script
        GPIO.add_event_detect(self.pulsador_gpio, GPIO.FALLING, callback=self.ejecutar_script_pulsador, bouncetime=300)

    def write(self, text):
        """ Redirige la salida estándar a la consola de la interfaz. """
        self.text_console.insert(tk.END, text)
        self.text_console.see(tk.END)  # Desplazamiento automático hacia abajo
        self.text_console.update()

    def flush(self):
        pass

    def ejecutar_script(self, script):
        """ Ejecuta un script en un hilo separado y captura su salida. """
        try:
            process = subprocess.Popen(['python3', script],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT,
                                       text=True)

            for line in process.stdout:
                self.write(line)

            process.stdout.close()
            process.wait()
        except Exception as e:
            self.write(f"Error ejecutando {script}: {e}\n")

    def ejecutar_script_captura(self, script):
        """ Ejecuta el script de captura de imágenes y almacena el proceso para poder detenerlo. """
        try:
            # Inicia el proceso y lo almacena en la variable capture_process
            self.capture_process = subprocess.Popen(['python3', script],
                                                    stdout=subprocess.PIPE,
                                                    stderr=subprocess.STDOUT,
                                                    text=True)
            for line in self.capture_process.stdout:
                self.write(line)
            self.capture_process.stdout.close()
            self.capture_process.wait()
            self.capture_process = None
        except Exception as e:
            self.write(f"Error ejecutando {script}: {e}\n")
            self.capture_process = None

    def detectar_camaras(self):
        threading.Thread(target=self.ejecutar_script, args=('detectar_camaras.py',), daemon=True).start()

    def abrir_configuracion(self):
        threading.Thread(target=self.ejecutar_script, args=('configurar_parametros.py',), daemon=True).start()

    def capturar_imagenes(self):
        """ Ejecuta el script de captura de imágenes y lo guarda para poder detenerlo. """
        # Si ya se está ejecutando un proceso de captura, avisar al usuario
        if self.capture_process is not None:
            messagebox.showinfo("Información", "El script de captura ya está en ejecución.")
            return

        threading.Thread(target=self.ejecutar_script_captura, args=('capturar_imagenes_gps.py',), daemon=True).start()

    def detener_captura(self):
        if self.capture_process is not None:
            self.capture_process.send_signal(signal.SIGINT)  # Emula Ctrl+C
            self.write("Deteniendo proceso de captura...\n")
            self.capture_process.wait()  # Espera a que termine
            self.capture_process = None
            self.write("Proceso de captura detenido y datos guardados.\n")
        else:
            messagebox.showinfo("Información", "No hay un proceso de captura en ejecución.")
    
    def ejecutar_script_pulsador(self, channel):
        """ Callback cuando se presiona el pulsador físico. Ejecuta el script de captura. """
        # Si ya se está ejecutando un proceso de captura, avisar al usuario
        if self.capture_process is not None:
            self.write("El script de captura ya está en ejecución.\n")
            return

        self.write("Pulsador presionado, ejecutando el script de captura...\n")
        threading.Thread(target=self.ejecutar_script_captura, args=('capturar_imagenes_gps.py',), daemon=True).start()

# Crear la ventana principal
root = tk.Tk()
app = InterfazApp(root)
root.mainloop()
