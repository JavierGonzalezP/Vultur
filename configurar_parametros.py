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
root.geometry("480x300")  # Establece el tamaño de la ventana
root.resizable(False, False)  # Evita que la ventana sea redimensionable

# Reorganizar la UI en una cuadrícula más compacta
tk.Label(root, text="Cámara 1").grid(row=0, column=0, columnspan=2)
tk.Label(root, text="Cámara 2").grid(row=0, column=2, columnspan=2)

parametros = ["Exposure Time", "Gain", "Width", "Height", "Pixel Format", "Frame Rate"]
entries_c1 = []
entries_c2 = []

for i, param in enumerate(parametros):
    tk.Label(root, text=f"{param}:").grid(row=i+1, column=0, sticky="e", padx=5, pady=2)
    entry = tk.Entry(root, width=10)
    entry.grid(row=i+1, column=1, padx=5, pady=2)
    entry.insert(0, config.get("Cámara1", {}).get(param.replace(" ", ""), ""))
    entries_c1.append(entry)

    tk.Label(root, text=f"{param}:").grid(row=i+1, column=2, sticky="e", padx=5, pady=2)
    entry = tk.Entry(root, width=10)
    entry.grid(row=i+1, column=3, padx=5, pady=2)
    entry.insert(0, config.get("Cámara2", {}).get(param.replace(" ", ""), ""))
    entries_c2.append(entry)

# Botón para guardar configuración
tk.Button(root, text="Guardar Configuración", command=guardar_configuracion).grid(row=len(parametros) + 1, column=0, columnspan=4, pady=10)

# Asignar entradas a variables globales
entry_exposure1, entry_gain1, entry_width1, entry_height1, entry_pixel1, entry_fps1 = entries_c1
entry_exposure2, entry_gain2, entry_width2, entry_height2, entry_pixel2, entry_fps2 = entries_c2

# Iniciar la interfaz
root.mainloop()
