import socket 
import sys
import threading
import json
import random
from kafka import KafkaConsumer

HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
FILE = "DATA.txt"

CAPACITY = []

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
    for i, line in enumerate(list_of_lines):
        if line.startswith(msg["id"]):
            existe = True
            info = list_of_lines[i].split(' ') # ID tiempo_ciclo capacidad nº_visitantes
            if msg["option"] == "+":
                visitantes = int(info[3]) + int(msg["visitantes"])# Sumamos los visitantes antiguos + los nuevos
            else:
                visitantes = int(info[3]) - int(msg["visitantes"])# Restamos los visitantes antiguos - los nuevos
                if(visitantes < 0): 
                    visitantes = 0
            list_of_lines[i] = info[0] + ' ' + random.randint(10,60) + ' ' + info[2] + ' ' + visitantes + '\n'
    
    fichero = open(FILE, "w")
    if existe:
        fichero.writelines(list_of_lines)
    else:
        fichero.write(msg["id"] + ' ' + random.randint(10,60) + ' ' + random.randint(50, 100) + ' '+ msg["visitantes"] + '\n')
    fichero.close()


# Función que devuelve un string con todos los tiempos guardados en el fichero
def readFile():
    fichero = open(FILE, 'r')
    list_of_lines = fichero.readlines()
    fichero.close()
    res= []
    for i, line in list_of_lines: # ID tiempo_ciclo capacidad nº_visitantes
        line.split()
        # T= número de personas que hay en cola (recibidas del sensor) /número de personas que caben en cada ciclo) * tiempo de cada ciclo.
        # TODO: Cambiar
        tiempo_espera = (line[3]/line[2]) * line[1]
        # ID-TiempoEspera ID-TiempoEspera ...
        res += line[0] + '-' + tiempo_espera + ' '
        item = {
            "id": line[0],
            "tiempo_espera" : tiempo_espera
        }
        res.append(item)
    return res


# Recibimos petición de Engine
def handle_client(conn, addr):
    print(f"[NUEVA CONEXION] {addr} connected.")
    print("Engine se ha conectado")
    msg_length = conn.recv(HEADER).decode(FORMAT)
    # Primer mensaje para obtener la capacidad de las atracciones
    if msg_length:
        msg_length = int(msg_length)
        capacidades = conn.recv(msg_length).decode(FORMAT)
        CAPACITY = capacidades.split(' ') # Guardamos en memoria una lista con las capacidades de las atracciones del parque
        
    print("Extrayendo datos del fichero")
    msg = json.dumps(readFile()) # Lo convertimos a JSON
    print("Enviando datos a Engine")
    conn.send(f"{msg}".encode(FORMAT)) # TODO: Rezar
    # Terminamos de enviar la información a Engine sobre los tiempo de espera
    print("Fin de la conexión")
    x = input()
    conn.close()


def start(SERVER_KAFKA, PORT_KAFKA):
    server.listen()
    print(f"[LISTENING] Servidor a la escucha en {SERVER}")

    # Escuchamos indefinidamente
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        consumer=KafkaConsumer('ste',bootstrap_servers=f'{SERVER_KAFKA}:{PORT_KAFKA}',auto_offset_reset='earliest')
        for message in consumer:
            updateFile(message)
    

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