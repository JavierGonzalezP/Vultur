from pypylon import pylon
import numpy as np
import json
import datetime
import time
import pandas as pd
from pymavlink import mavutil
import os
import signal
import RPi.GPIO as GPIO

detener = False
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Crear carpeta para guardar imágenes y datos
timestamp_inicio = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
carpeta_guardado = f"capturas_{timestamp_inicio}"
os.makedirs(carpeta_guardado, exist_ok=True)

# Nombre del archivo Excel dentro de la carpeta
archivo_excel = os.path.join(carpeta_guardado, "captura_datos_gps.xlsx")

# Intentar configurar conexión con el Pixhawk (GPS)
try:
    connection = mavutil.mavlink_connection('/dev/serial0', baud=57600)
    heartbeat = connection.wait_heartbeat(timeout=10)
    if heartbeat:
        print("Heartbeat recibido.")
        gps_enabled = True
    else:
        print("No se recibió el heartbeat en el tiempo límite.")
        gps_enabled = False
except Exception as e:
    print(f"No se pudo conectar al Pixhawk: {e}")
    gps_enabled = False


def obtener_posicion_gps():
    """ Obtiene la posición GPS desde el Pixhawk mediante MAVLink. """
    if not gps_enabled:
        return None, None, None
    
    msg = connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True, timeout=1)
    if msg:
        lat = msg.lat / 1e7
        lon = msg.lon / 1e7
        alt = msg.alt / 1000.0
        return lat, lon, alt
    else:
        return None, None, None


def guardar_datos_excel(datos):
    df_nuevo = pd.DataFrame(datos, columns=["Imagen Cámara 1", "Imagen Cámara 2", "Latitud", "Longitud", "Altitud"])
    
    if os.path.exists(archivo_excel):
        with pd.ExcelWriter(archivo_excel, mode='a', if_sheet_exists='overlay') as writer:
            existing_df = pd.read_excel(archivo_excel, sheet_name="Sheet1")
            start_row = existing_df.shape[0] + 1
            df_nuevo.to_excel(writer, index=False, header=False, startrow=start_row)
    else:
        df_nuevo.to_excel(archivo_excel, index=False)


def manejar_senal(signum, frame):
    global detener
    print("\nSeñal de terminación recibida. Guardando datos...")
    detener = True  # Se detendrá el bucle en la siguiente iteración


# Capturar SIGINT (Ctrl+C) y SIGTERM (terminate)
signal.signal(signal.SIGINT, manejar_senal)
signal.signal(signal.SIGTERM, manejar_senal)

def manejar_pulsador(channel):
    """ Callback cuando se presiona el pulsador físico. """
    global detener
    print("\nPulsador presionado. Guardando datos y cerrando...")
    detener = True  # Se detiene el bucle de captura
    
# Detectar evento en el GPIO (flanco de bajada)
GPIO.add_event_detect(21, GPIO.FALLING, callback=manejar_pulsador, bouncetime=300)


def capturar_imagenes():
    global detener
    datos = []
    contador = 1

    try:
        with open("config.json", "r") as f:
            config = json.load(f)

        tl_factory = pylon.TlFactory.GetInstance()
        devices = tl_factory.EnumerateDevices()

        if len(devices) < 2:
            print("No se detectaron cámaras.")
            return

        camera1 = pylon.InstantCamera(tl_factory.CreateDevice(devices[0]))
        camera2 = pylon.InstantCamera(tl_factory.CreateDevice(devices[1]))

        camera1.Open()
        camera2.Open()

        camera1.ExposureTime.SetValue(config["Cámara1"]["ExposureTime"])
        camera1.Gain.SetValue(config["Cámara1"]["Gain"])
        camera1.Width.SetValue(config["Cámara1"]["Width"])
        camera1.Height.SetValue(config["Cámara1"]["Height"])
        camera1.PixelFormat.SetValue(config["Cámara1"]["PixelFormat"])
        camera1.AcquisitionFrameRateEnable.SetValue(True)
        camera1.AcquisitionFrameRate.SetValue(config["Cámara1"]["FrameRate"])

        camera2.ExposureTime.SetValue(config["Cámara2"]["ExposureTime"])
        camera2.Gain.SetValue(config["Cámara2"]["Gain"])
        camera2.Width.SetValue(config["Cámara2"]["Width"])
        camera2.Height.SetValue(config["Cámara2"]["Height"])
        camera2.PixelFormat.SetValue(config["Cámara2"]["PixelFormat"])
        camera2.AcquisitionFrameRateEnable.SetValue(True)
        camera2.AcquisitionFrameRate.SetValue(config["Cámara2"]["FrameRate"])

        camera1.StartGrabbing()
        camera2.StartGrabbing()

        while not detener:
            grab1 = camera1.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            grab2 = camera2.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            if grab1.GrabSucceeded() and grab2.GrabSucceeded():
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

                # Guardar imagen de cámara 1
                filename1 = os.path.join(carpeta_guardado, f"cam1_{timestamp}_{contador}.raw")
                with open(filename1, "wb") as f:
                    f.write(grab1.Array.tobytes())

                # Guardar imagen de cámara 2
                filename2 = os.path.join(carpeta_guardado, f"cam2_{timestamp}_{contador}.raw")
                with open(filename2, "wb") as f:
                    f.write(grab2.Array.tobytes())

                # Obtener posición GPS
                lat, lon, alt = obtener_posicion_gps()

                # Guardar datos en lista
                datos.append([filename1, filename2, lat, lon, alt])

                print(f"Imagen {contador} capturada: {filename1} y {filename2} - GPS: {lat}, {lon}, {alt}")

            grab1.Release()
            grab2.Release()

            contador += 1

    except Exception as e:
        print(f"Hubo un problema: {e}")

    finally:
        guardar_datos_excel(datos)  # Guardar datos antes de salir
        camera1.Close()
        camera2.Close()
        print(f"Datos guardados en {archivo_excel} y cámaras cerradas correctamente.")


if __name__ == "__main__":
    capturar_imagenes()

