import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import sys
import io

class InterfazApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interfaz de Ejecución de Códigos")
        
        # Variable para almacenar el proceso del script de captura
        self.capture_process = None

        # Botones para ejecutar los scripts
        tk.Button(root, text="Detectar Cámaras", command=self.detectar_camaras).pack(pady=10)
        tk.Button(root, text="Abrir Configuración de Cámaras", command=self.abrir_configuracion).pack(pady=10)
        tk.Button(root, text="Capturar Imágenes", command=self.capturar_imagenes).pack(pady=10)
        tk.Button(root, text="Detener Captura", command=self.detener_captura).pack(pady=10)

        # Consola para mostrar salida del script
        self.text_console = tk.Text(root, height=10, width=60)
        self.text_console.pack(pady=10)
        
        # Redirigir la salida estándar a la consola
        sys.stdout = self

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

        threading.Thread(target=self.ejecutar_script_captura, args=('capturar_imagenes.py',), daemon=True).start()

    def detener_captura(self):
        """ Detiene el script de captura de imágenes si está en ejecución. """
        if self.capture_process is not None:
            self.capture_process.terminate()  # Envía una señal para finalizar el proceso
            self.write("Proceso de captura detenido.\n")
            self.capture_process = None
        else:
            messagebox.showinfo("Información", "No hay un proceso de captura en ejecución.")
            
            
# Crear la ventana principal
root = tk.Tk()
app = InterfazApp(root)
root.mainloop()
