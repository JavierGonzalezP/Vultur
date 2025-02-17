import tkinter as tk
from tkinter import messagebox
import json
import os

CONFIG_FILE = "config.json"

# Función para cargar la configuración
def cargar_configuracion():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    return {}

# Función para guardar la configuración
def guardar_configuracion():
    nueva_config = {
        "Cámara1": {
            "ExposureTime": int(entry_exposure1.get()),
            "Gain": float(entry_gain1.get()),
            "Width": int(entry_width1.get()),
            "Height": int(entry_height1.get()),
            "PixelFormat": entry_pixel1.get(),
            "FrameRate": float(entry_fps1.get())
        },
        "Cámara2": {
            "ExposureTime": int(entry_exposure2.get()),
            "Gain": float(entry_gain2.get()),
            "Width": int(entry_width2.get()),
            "Height": int(entry_height2.get()),
            "PixelFormat": entry_pixel2.get(),
            "FrameRate": float(entry_fps2.get())
        }
    }

    with open(CONFIG_FILE, "w") as file:
        json.dump(nueva_config, file, indent=4)

    messagebox.showinfo("Guardado", "Configuración guardada exitosamente.")

# Cargar configuración existente
config = cargar_configuracion()

# Crear ventana
root = tk.Tk()
root.title("Configuración de Cámaras")

# Cámara 1
tk.Label(root, text="Cámara 1").grid(row=0, column=1)
tk.Label(root, text="Exposure Time:").grid(row=1, column=0)
entry_exposure1 = tk.Entry(root)
entry_exposure1.grid(row=1, column=1)
entry_exposure1.insert(0, config.get("Cámara1", {}).get("ExposureTime", ""))

tk.Label(root, text="Gain:").grid(row=2, column=0)
entry_gain1 = tk.Entry(root)
entry_gain1.grid(row=2, column=1)
entry_gain1.insert(0, config.get("Cámara1", {}).get("Gain", ""))

tk.Label(root, text="Width:").grid(row=3, column=0)
entry_width1 = tk.Entry(root)
entry_width1.grid(row=3, column=1)
entry_width1.insert(0, config.get("Cámara1", {}).get("Width", ""))

tk.Label(root, text="Height:").grid(row=4, column=0)
entry_height1 = tk.Entry(root)
entry_height1.grid(row=4, column=1)
entry_height1.insert(0, config.get("Cámara1", {}).get("Height", ""))

tk.Label(root, text="Pixel Format:").grid(row=5, column=0)
entry_pixel1 = tk.Entry(root)
entry_pixel1.grid(row=5, column=1)
entry_pixel1.insert(0, config.get("Cámara1", {}).get("PixelFormat", ""))

tk.Label(root, text="Frame Rate:").grid(row=6, column=0)
entry_fps1 = tk.Entry(root)
entry_fps1.grid(row=6, column=1)
entry_fps1.insert(0, config.get("Cámara1", {}).get("FrameRate", ""))

# Cámara 2
tk.Label(root, text="Cámara 2").grid(row=0, column=3)
tk.Label(root, text="Exposure Time:").grid(row=1, column=2)
entry_exposure2 = tk.Entry(root)
entry_exposure2.grid(row=1, column=3)
entry_exposure2.insert(0, config.get("Cámara2", {}).get("ExposureTime", ""))

tk.Label(root, text="Gain:").grid(row=2, column=2)
entry_gain2 = tk.Entry(root)
entry_gain2.grid(row=2, column=3)
entry_gain2.insert(0, config.get("Cámara2", {}).get("Gain", ""))

tk.Label(root, text="Width:").grid(row=3, column=2)
entry_width2 = tk.Entry(root)
entry_width2.grid(row=3, column=3)
entry_width2.insert(0, config.get("Cámara2", {}).get("Width", ""))

tk.Label(root, text="Height:").grid(row=4, column=2)
entry_height2 = tk.Entry(root)
entry_height2.grid(row=4, column=3)
entry_height2.insert(0, config.get("Cámara2", {}).get("Height", ""))

tk.Label(root, text="Pixel Format:").grid(row=5, column=2)
entry_pixel2 = tk.Entry(root)
entry_pixel2.grid(row=5, column=3)
entry_pixel2.insert(0, config.get("Cámara2", {}).get("PixelFormat", ""))

tk.Label(root, text="Frame Rate:").grid(row=6, column=2)
entry_fps2 = tk.Entry(root)
entry_fps2.grid(row=6, column=3)
entry_fps2.insert(0, config.get("Cámara2", {}).get("FrameRate", ""))

# Botón para guardar configuración
tk.Button(root, text="Guardar Configuración", command=guardar_configuracion).grid(row=7, column=1, columnspan=3)

# Iniciar la interfaz
root.mainloop()

