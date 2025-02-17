import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

def cargar_y_mostrar_raw(filename, width=1280, height=720):
    """
    Carga y muestra una imagen en formato .raw (Mono8, escala de grises).
    
    :param filename: Ruta del archivo .raw
    :param width: Ancho de la imagen (1280 por defecto)
    :param height: Alto de la imagen (720 por defecto)
    """
    try:
        # Leer los datos binarios
        raw_data = np.fromfile(filename, dtype=np.uint8)
        
        # Verificar tamaño esperado
        expected_size = width * height
        if raw_data.size != expected_size:
            print(f"Error: Tamaño incorrecto. Se esperaban {expected_size} bytes, pero se encontraron {raw_data.size}.")
            return
        
        # Reestructurar los datos en la forma de la imagen
        image = raw_data.reshape((height, width))

        # Mostrar la imagen
        plt.figure(figsize=(6, 4))
        plt.imshow(image, cmap="gray")
        plt.axis("off")
        plt.title(f"Imagen: {filename}")
        plt.show()
    
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")

def seleccionar_y_visualizar():
    """Abre un cuadro de diálogo para seleccionar un archivo .raw y lo muestra."""
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter
    file_path = filedialog.askopenfilename(title="Selecciona un archivo .raw", filetypes=[("RAW files", "*.raw")])
    
    if file_path:
        cargar_y_mostrar_raw(file_path, width=1280, height=720)

if __name__ == "__main__":
    seleccionar_y_visualizar()
