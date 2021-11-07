import socket 
import sys
import threading
import json
import random
from kafka import KafkaConsumer

HEADER = 2048
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
FILE = "DATA.txt"

# Función que escribe en el fichero donde se guardan los datos de las atracciones
def updateFile(msg):
    # Cada línea corresponde a una atracción y cada línea tiene el formato de: ID tiempo_ciclo nº_visitantes
    # Si ya existía entonces se actualiza la linea, en caso contrario se añade al final
    # Convertimos el mensaje a JSON
    msg = json.loads(msg)
    fichero = open(FILE, "r")
    list_of_lines = fichero.readlines() # Obtenemos todas las lineas almacenadas en el fichero
    fichero.close()
    existe = False
    for i,line in enumerate(list_of_lines):
        info = list_of_lines[i].split(' ') # ID tiempo_ciclo capacidad nº_visitantes
        if info[0] == msg["sensor_id"]:
            existe = True
            visitantes = int(msg["population"])# Sustituimos los visitantes antiguos por los nuevos
            if(visitantes < 0): 
                visitantes = 0
            list_of_lines[i] = str(info[0]) + ' ' + str(info[1]) + ' ' + str(info[2]) + ' ' + str(visitantes) + '\n'

    if existe:
        fichero = open(FILE, "w")
        fichero.writelines(list_of_lines)
    else:
        fichero = open(FILE, "a")
        fichero.write(str(msg["sensor_id"]) + ' ' + str(random.randint(10,60)) + ' ' + str(random.randint(50, 100)) + ' '+ str(msg["population"]) + '\n')
    print("Fichero actualizado")
    fichero.close()


# Función que devuelve un string con todos los tiempos guardados en el fichero
def readFile():
    fichero = open(FILE, 'r')
    list_of_lines = fichero.readlines()
    fichero.close()
    res= []
    for line in list_of_lines: # ID tiempo_ciclo capacidad nº_visitantes
        line = line.split(' ')
        # T= número de personas que hay en cola (recibidas del sensor) /número de personas que caben en cada ciclo) * tiempo de cada ciclo.
        tiempo_espera = (int(line[3])/int(line[2])) * int(line[1])
        item = {
            "id": line[0],
            "tiempo" : tiempo_espera
        }
        res.append(item)
    msg = {
        "datos" : res
    }
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
    while True:
        consumer=KafkaConsumer('sensor',bootstrap_servers=f'{SERVER_KAFKA}:{PORT_KAFKA}',auto_offset_reset='earliest')
        for message in consumer:
            print("Leyendo mensaje")
            updateFile(message.value)

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