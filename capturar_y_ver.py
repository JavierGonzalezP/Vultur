import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from pypylon import pylon

def capturar_imagen_basler(filename, width=1280, height=720):
    """
    Captura una imagen con una cámara Basler y la guarda en formato RAW.
    """
    try:
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        camera.Open()
        camera.StartGrabbing()
        grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        
        if grab_result.GrabSucceeded():
            image = grab_result.Array
            image.tofile(filename)
        
        grab_result.Release()
        camera.Close()
    except Exception as e:
        print(f"Error al capturar la imagen: {e}")

def cargar_y_mostrar_raw(filename, width=1280, height=720):
    """
    Carga y muestra una imagen en formato .raw (Mono8, escala de grises) ajustada a 480x300.
    """
    try:
        raw_data = np.fromfile(filename, dtype=np.uint8)
        expected_size = width * height
        if raw_data.size != expected_size:
            print(f"Error: Tamaño incorrecto. Se esperaban {expected_size} bytes, pero se encontraron {raw_data.size}.")
            return
        
        image = raw_data.reshape((height, width))
        
        plt.rcParams['toolbar'] = 'None'  # Ocultar barra de herramientas
        fig = plt.figure(figsize=(4.8, 2.5))
        ax = fig.add_axes([0, 0, 1, 1])  # Eliminar márgenes
        ax.imshow(image, cmap="gray")
        ax.axis("off")
        plt.show()
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")

if __name__ == "__main__":
    filename = "captura.raw"
    capturar_imagen_basler(filename)
    cargar_y_mostrar_raw(filename, width=1280, height=720)
