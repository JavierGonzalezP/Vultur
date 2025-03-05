from pymavlink import mavutil
import time

# Conexión al Pixhawk vía MAVLink (cambia el puerto y la velocidad según tu configuración)
connection_string = '/dev/serial0'
baud_rate = 115200
print("Conectando al Pixhawk...")
master = mavutil.mavlink_connection(connection_string, baud=57600)

# Espera a la primera señal heart--++beat para confirmar la conexión
master.wait_heartbeat()
print("Heartbeat recibido.")

# Bucle para leer mensajes de GPS_RAW_INT
try:
    while True:
        # Recibir el siguiente mensaje
        msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True, timeout=5)
        if msg is not None:
            # Los campos típicos son:
            # lat, lon, alt (en gradosE7, mm, respectivamente), y satellites_visible
            lat = msg.lat / 1e7
            lon = msg.lon / 1e7
            alt = msg.alt / 1000.0  # Convertido a metros (si el valor
            print("GPS - Lat: {:.7f}, Lon: {:.7f}, Alt: {} m".format(lat, lon, alt))
        time.sleep(1)
except KeyboardInterrupt:
    print("Terminando la lectura de GPS.")
