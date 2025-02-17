from pypylon import pylon

def detectar_camaras():
    try:
        tl_factory = pylon.TlFactory.GetInstance()
        devices = tl_factory.EnumerateDevices()
        
        if len(devices) == 0:
            print("No se detectaron cámaras.")
        else:
            camera_list = "\n".join([f"{i+1}. {device.GetFriendlyName()}" for i, device in enumerate(devices)])
            print(f"Se detectaron las siguientes cámaras:\n{camera_list}")
    except Exception as e:
        print(f"Hubo un problema detectando las cámaras: {e}")

if __name__ == "__main__":
    detectar_camaras()
