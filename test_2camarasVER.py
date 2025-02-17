from pypylon import pylon
import cv2
import numpy as np

# Obtener lista de dispositivos
tl_factory = pylon.TlFactory.GetInstance()
devices = tl_factory.EnumerateDevices()

if len(devices) < 2:
    print("Se requieren 2 cámaras conectadas. Detectadas:", len(devices))
    exit()

# Crear objetos de cámara
camera1 = pylon.InstantCamera(tl_factory.CreateDevice(devices[0]))
camera2 = pylon.InstantCamera(tl_factory.CreateDevice(devices[1]))

# Abrir cámaras
camera1.Open()
camera2.Open()

# Configuración opcional (reducir resolución o FPS para estabilidad)
camera1.AcquisitionFrameRateEnable = True
camera1.AcquisitionFrameRate = 10
camera2.AcquisitionFrameRateEnable = True
camera2.AcquisitionFrameRate = 10

camera1.Width = 1920
camera1.Height = 1080
camera2.Width = 1920
camera2.Height = 1080

# Iniciar captura
camera1.StartGrabbing()
camera2.StartGrabbing()

# Conversores para OpenCV
converter = pylon.ImageFormatConverter()
converter.OutputPixelFormat = pylon.PixelType_RGB8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

while camera1.IsGrabbing() and camera2.IsGrabbing():
    grab1 = camera1.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    grab2 = camera2.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grab1.GrabSucceeded() and grab2.GrabSucceeded():
        img1 = converter.Convert(grab1).GetArray()
        img2 = converter.Convert(grab2).GetArray()

        # Mostrar imágenes en ventanas separadas
        cv2.imshow("Camara 1", img1)
        cv2.imshow("Camara 2", img2)

        # Guardar imágenes
        cv2.imwrite("cam1.jpg", img1)
        cv2.imwrite("cam2.jpg", img2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    grab1.Release()
    grab2.Release()

# Cerrar cámaras y ventanas
camera1.Close()
camera2.Close()
cv2.destroyAllWindows()
