import socket 
import sys
import threading
import time
import sqlite3

HEADER = 64
# TODO: cambiar?
PORT = 5050
# TODO: cambiar?
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
XSEC = 30
# TODO: Quitar en un futuro
FIN = "FIN"


# Función que se encarga de enviar el mapa actualizado al gestor de colas
def send(msg, client):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

# Función que se encarga de actualizar el mapa según el movimiento recibido por argumentos
def handle_client(conn, addr, ADDR_KAFKA):
    print(f"[NUEVA CONEXION] {addr} connected.")
    while True:
        # msg contiene el movimiento realizado por el Visitante
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f" He recibido del servidor de colas [{addr}] el mensaje:\n{msg}")

            # TODO: Actualizar mapa
            # TODO: conn y addr tienen que ser los de FAKFA?
            print("Enviando mapa actualizado...")
            # connectToKAFKA(ADDR_KAFKA, msg)
            # conn.send(f"{msg}".encode(FORMAT))
        break
    print("ADIOS. TE ESPERO EN OTRA OCASION")
    conn.close()

# TODO: Streaming & QM??
# Función que se encarga de concetar con el gestor de colas y enviarle el mapa actualizado
# def connectToKAFKA(ADDR_KAFKA, msg):
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client.connect(ADDR_KAFKA)
#     print (f"Establecida conexión en [{ADDR}]")
#     # TODO: Enviar a Kafka el mapa actualizado
#     while msg != FIN:
#         print("SERVIDR: ", client.recv(2048).decode(FORMAT))
#         msg = input()
#     send(FIN, client)
#     client.close()

# Función que se encarga de actualizar los tiempos de espera de las atracciones
def connectToSTE(ADDR_STE): # (CLIENTE de STE)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR_STE)
    print (f"Establecida conexión en [{ADDR}]")
    msg = ""
    # TODO: Recibir mensaje de STE y actualizar tiempos de espera de la Base de Datos
    while msg != FIN:
        print("SERVIDR: ", client.recv(2048).decode(FORMAT))
        msg = input()
    send(FIN, client)
    client.close()

# Engine empieza a escuchar al gestor de colas (Kafka)
def start(ADDR_KAFKA, ADDR_STE, MAX_CONEXIONES): # (SERVIDOR DE KAFKA)
    server.listen()
    print(f"[LISTENING] Servidor a la escucha en {SERVER}")
    CONEX_ACTIVAS = threading.active_count()-1
    print(f"{CONEX_ACTIVAS} / {MAX_CONEXIONES}")
    start = time.time()
    while True:
        # Cada X segundos se conecta a STE para actualizar los tiempos de espera de las atracciones
        if (round((time.time() - start)) == XSEC):
            connectToSTE(ADDR_STE)
            start = time.time() # Reseteamos el timer

        conn, addr = server.accept()
        CONEX_ACTIVAS = threading.active_count()
        if (CONEX_ACTIVAS <= MAX_CONEXIONES): 
            thread = threading.Thread(target=handle_client, args=(conn, addr, ADDR_KAFKA))
            thread.start()
            print(f"[CONEXIONES ACTIVAS] {CONEX_ACTIVAS}")
            print("CONEXIONES RESTANTES PARA CERRAR EL SERVICIO", MAX_CONEXIONES-CONEX_ACTIVAS)
        else:
            print("AFORO ALCANZADO")
            conn.send("El parque ha alcanzado su aforo máximo, vuelve en otro momento.".encode(FORMAT))
            conn.close()
            CONEX_ACTUALES = threading.active_count()-1
    
########## MAIN ##########

if  (len(sys.argv) == 6):
    SERVER_FAKFA = sys.argv[1]
    PORT_FAKFA = int(sys.argv[2])
    ADDR_KAFKA = (SERVER_FAKFA, PORT_FAKFA)

    SERVER_STE = sys.argv[3]
    PORT_STE = int(sys.argv[4])
    ADDR_STE = (SERVER_STE, PORT_STE)

    MAX_CONEXIONES = int(sys.argv[5])

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    print("[STARTING ENGINE] Servidor inicializándose...")
    start(ADDR_KAFKA, ADDR_STE, MAX_CONEXIONES)
else:
    print ("Oops!. Parece que algo falló.\nNecesito estos argumentos:<ServerIP_FAKFA> <Puerto_FAKFA> <SERVERIP_STE> <PUERTO_STE> <Nº MAX VISITANTES>")
