import socket 
import sys
import threading
import json
import random
import time
from kafka import KafkaConsumer

HEADER = 2048
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
FILE = "DATA.json"

# Función que escribe en el fichero donde se guardan los datos de las atracciones
def updateFile(msg):
    fichero = open(FILE,"r")
    data = ""
    try:
        data = json.load(fichero)
    except:
        print("DATA.json está vacío")
    fichero.close()
    fichero = open(FILE,"w")
    existe = False
    if data == "":
        data = {"datos" : []}
        data = json.dumps(data)
        data = json.loads(data)
    newdata = {"datos" : []}
    for info in data["datos"]:
        if info["id"] == msg["sensor_id"]:
            existe = True
            info["visitantes"] = msg["population"]
            info["timestamp"] = msg["timestamp"]
            newdata["datos"].append(info)
        else:
            newdata["datos"].append(info)
    if not existe:
        info = {
            "id" : msg["sensor_id"],
            "visitantes" : msg["population"],
            "capacidad" :  str(random.randint(50, 100)),
            "tiempo_ciclo" : str(random.randint(10,60)),
            "timestamp" : msg["timestamp"]
        }
        info = json.dumps(info)
        info = json.loads(info)
        newdata["datos"].append(info)
    newdata = json.dumps(newdata)
    fichero.write(newdata)
    fichero.close()
    print("Fichero actualizado")

# Función que devuelve un string con todos los tiempos guardados en el fichero
def readFile():
    fichero = open(FILE,"r")
    data = ""
    try:
        data = json.load(fichero)
    except:
        print("DATA.json está vacío")
    res = []
    if data != "":
        for info in data["datos"]:
            # T= número de personas que hay en cola (recibidas del sensor) /número de personas que caben en cada ciclo) * tiempo de cada ciclo.
            tiempo_espera = (int(info["visitantes"])/int(info["capacidad"]))*int(info["tiempo_ciclo"])
            item = {
                "id": info["id"],
                "tiempo" : tiempo_espera
            }
            res.append(item)
    msg = {"datos" : res}
    return msg


# Recibimos petición de Engine
def handle_client(conn, addr):
    print(f"[NUEVA CONEXION] {addr} connected.")
    print("Engine se ha conectado")
        
    print("Extrayendo datos del fichero")
    msg = json.dumps(readFile()) # Lo convertimos a JSON
    print("Enviando datos a Engine")
    conn.send(f"{msg}".encode(FORMAT))
    # Terminamos de enviar la información a Engine sobre los tiempo de espera
    print("Fin de la conexión")
    conn.close()

def connectionSTEtoEngine():
    print("\n[Esperando conexión con ENGINE]")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

def connectionSTEtoSensor(SERVER_KAFKA, PORT_KAFKA):
    start = time.time()*1000
    while True:
        consumer=KafkaConsumer('sensor',bootstrap_servers=f'{SERVER_KAFKA}:{PORT_KAFKA}',auto_offset_reset='earliest')
        for message in consumer:
            message = json.loads(message.value)
            if "timestamp" in message:
                if message["timestamp"] - start > 0.0:
                    print(message["timestamp"] - start)
                    print("Leyendo mensaje")
                    updateFile(message)

def start(SERVER_KAFKA, PORT_KAFKA):
    server.listen()
    print(f"[LISTENING] Servidor a la escucha en {SERVER}")
    # Escuchamos indefinidamente
    threadEngine = threading.Thread(target=connectionSTEtoEngine, args=())
    threadSensor = threading.Thread(target=connectionSTEtoSensor, args=(SERVER_KAFKA, PORT_KAFKA))

    threadEngine.start()
    threadSensor.start()

########## MAIN ##########

if  (len(sys.argv) == 4):
    SERVER_KAFKA = sys.argv[1]
    PORT_KAFKA = int(sys.argv[2])

    PORT = int(sys.argv[3])
    ADDR = (SERVER, PORT)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    print("[STARTING WTS] Servidor inicializándose...")
    start(SERVER_KAFKA, PORT_KAFKA)
else:
    print ("Oops!. Parece que algo falló.\nNecesito estos argumentos:<ServerIP_FAKFA> <Puerto_FAKFA> <Puerto_Escucha>")