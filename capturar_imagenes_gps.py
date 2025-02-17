from pypylon import pylon
import numpy as np
import json
import datetime
import time
import pandas as pd
from pymavlink import mavutil

# Intentar configurar conexión con el Pixhawk (GPS)
try:
    connection = mavutil.mavlink_connection('/dev/ttyAMA0', baud=57600)
    heartbeat = connection.wait_heartbeat(timeout=10)  # Tiempo de espera para el heartbeat
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
        lat = msg.lat / 1e7  # Convertir de grados * 1e7 a grados decimales
        lon = msg.lon / 1e7
        alt = msg.alt / 1000.0  # Convertir de mm a metros
        return lat, lon, alt
    else:
        return None, None, None

def capturar_imagenes():
    try:
        with open("config.json", "r") as f:
            config = json.load(f)

        # Crear objetos de cámara y configurar
        tl_factory = pylon.TlFactory.GetInstance()
        devices = tl_factory.EnumerateDevices()

        if len(devices) < 2:
            print("No se detectaron cámaras.")
            return

        camera1 = pylon.InstantCamera(tl_factory.CreateDevice(devices[0]))
        camera2 = pylon.InstantCamera(tl_factory.CreateDevice(devices[1]))

        # Abrir cámaras
        camera1.Open()
        camera2.Open()

        # Configurar parámetros de Cámara 1
        camera1.ExposureTime.SetValue(config["Cámara1"]["ExposureTime"])
        camera1.Gain.SetValue(config["Cámara1"]["Gain"])
        camera1.Width.SetValue(config["Cámara1"]["Width"])
        camera1.Height.SetValue(config["Cámara1"]["Height"])
        camera1.PixelFormat.SetValue(config["Cámara1"]["PixelFormat"])
        camera1.AcquisitionFrameRateEnable.SetValue(True)
        camera1.AcquisitionFrameRate.SetValue(config["Cámara1"]["FrameRate"])

        # Configurar parámetros de Cámara 2
        camera2.ExposureTime.SetValue(config["Cámara2"]["ExposureTime"])
        camera2.Gain.SetValue(config["Cámara2"]["Gain"])
        camera2.Width.SetValue(config["Cámara2"]["Width"])
        camera2.Height.SetValue(config["Cámara2"]["Height"])
        camera2.PixelFormat.SetValue(config["Cámara2"]["PixelFormat"])
        camera2.AcquisitionFrameRateEnable.SetValue(True)
        camera2.AcquisitionFrameRate.SetValue(config["Cámara2"]["FrameRate"])

        # Iniciar captura y guardar imágenes
        camera1.StartGrabbing()
        camera2.StartGrabbing()

        # Crear lista para almacenar datos
        datos = []

        for i in range(8):
            grab1 = camera1.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            grab2 = camera2.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            if grab1.GrabSucceeded() and grab2.GrabSucceeded():
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

                # Guardar imagen de cámara 1
                img1_raw = grab1.Array.tobytes()
                filename1 = f"cam1_{timestamp}.raw"
                with open(filename1, "wb") as f:
                    f.write(img1_raw)

                # Guardar imagen de cámara 2
                img2_raw = grab2.Array.tobytes()
                filename2 = f"cam_{timestamp}.raw"
                with open(filename2, "wb") as f:
                    f.write(img2_raw)

                # Obtener posición GPS
                lat, lon, alt = obtener_posicion_gps()

                # Guardar datos en lista
                datos.append([filename1, filename2, lat, lon, alt])

                print(f"Imagen {i+1} capturada: {filename1} y {filename2} - GPS: {lat}, {lon}, {alt}")

            grab1.Release()
            grab2.Release()

        # Guardar en Excel
        df = pd.DataFrame(datos, columns=["Imagen Cámara 1", "Imagen Cámara 2", "Latitud", "Longitud", "Altitud"])
        df.to_excel("capturar_imagenes.xlsx", index=False)

        print("Captura de imágenes completada.")

    except Exception as e:
        print(f"Hubo un problema al capturar las imágenes: {e}")

if __name__ == "__main__":
    capturar_imagenes()
