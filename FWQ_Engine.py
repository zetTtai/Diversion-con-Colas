import socket 
import sys
import threading
import time
import sqlite3
import traceback
from kafka import KafkaConsumer
from kafka import KafkaProducer

HEADER = 64
# TODO: cambiar?
PORT = 5050
# TODO: cambiar?
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
XSEC = 30


# Función que se encarga de enviar el mapa actualizado al gestor de colas
def send(msg, client):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def handle_client(conn, addr):
    print(f"[NUEVA CONEXION] {addr} connected.")
    while True:
        # msg contiene el movimiento realizado por el Visitante
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f" He recibido del servidor de colas [{addr}] el mensaje:\n{msg}")

            # TODO: Actualizar mapa
            print("Enviando mapa actualizado...")
        break
    print("ADIOS. TE ESPERO EN OTRA OCASION")
    conn.close()

def actualizarTiemposEspera(msg): # msg=  ID-Tiempo ID-Tiempo ...
    conn = sqlite3.connect('db/database.db')
    print(f"Establecida conexión con la base de datos")
    cursor = conn.cursor()

    msg =  msg.split(' ')
    for info in msg:
        info = info.split('-')
        try:
            cursor.execute(f'UPDATE atracciones SET wait_time = "{info[1]}" where id = {info[0]}')
            conn.commit()
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

    conn.close()


# Función que se encarga de actualizar los tiempos de espera de las atracciones
def connectToSTE(ADDR_STE): # (CLIENTE de STE)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR_STE)
    print (f"Establecida conexión en [{ADDR}]")
    # TODO: Recibir mensaje de STE y actualizar tiempos de espera de la Base de Datos
    # print("SERVIDR: ", client.recv(2048).decode(FORMAT))
    actualizarTiemposEspera(client.recv(2048).decode(FORMAT))
    client.close()


def updateMap(msg):
    return ""

# Engine empieza a escuchar al gestor de colas (Kafka)
def start(SERVER_KAFKA, PORT_KAFKA, MAX_CONEXIONES): # (SERVIDOR DE KAFKA)
    server.listen()
    print(f"[LISTENING] Servidor a la escucha en {SERVER}")
    CONEX_ACTIVAS = threading.active_count()-1
    # print(f"{CONEX_ACTIVAS} / {MAX_CONEXIONES}")
    start = time.time()
    while True:
        # Cada X segundos se conecta a STE para actualizar los tiempos de espera de las atracciones
        if (round((time.time() - start)) == XSEC):
            connectToSTE(ADDR_STE)
            start = time.time() # Reseteamos el timer

        # Recibimos un movimiento
        consumer=KafkaConsumer('engine',bootstrap_servers=f'{SERVER_KAFKA}:{PORT_KAFKA}',auto_offset_reset='earliest')
        for message in consumer:
            print(message)
            # TODO: Actualizar mapa
            map = updateMap(message)
            producer= KafkaProducer(bootstrap_servers=f'{SERVER_KAFKA}:{PORT_KAFKA}')
            # Enviamos el mapa 
            producer.send('visitantes',map.encode(FORMAT))

        # conn, addr = server.accept()
        # CONEX_ACTIVAS = threading.active_count()
        # if (CONEX_ACTIVAS <= MAX_CONEXIONES): 
        #     thread = threading.Thread(target=handle_client, args=(conn, addr))
        #     thread.start()
        #     print(f"[CONEXIONES ACTIVAS] {CONEX_ACTIVAS}")
        #     print("CONEXIONES RESTANTES PARA CERRAR EL SERVICIO", MAX_CONEXIONES-CONEX_ACTIVAS)
        # else:
        #     print("AFORO ALCANZADO")
        #     conn.send("El parque ha alcanzado su aforo máximo, vuelve en otro momento.".encode(FORMAT))
        #     conn.close()
        #     CONEX_ACTUALES = threading.active_count()-1
    
########## MAIN ##########

if  (len(sys.argv) == 6):
    SERVER_KAFKA = sys.argv[1]
    PORT_KAFKA = int(sys.argv[2])

    SERVER_STE = sys.argv[3]
    PORT_STE = int(sys.argv[4])
    ADDR_STE = (SERVER_STE, PORT_STE)

    MAX_CONEXIONES = int(sys.argv[5])

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    print("[STARTING ENGINE] Servidor inicializándose...")
    start(SERVER_KAFKA, PORT_KAFKA, ADDR_STE, MAX_CONEXIONES)
else:
    print ("Oops!. Parece que algo falló.\nNecesito estos argumentos:<ServerIP_FAKFA> <Puerto_FAKFA> <SERVERIP_STE> <PUERTO_STE> <Nº MAX VISITANTES>")
