import socket 
import sys
import threading
import time

HEADER = 64
# TODO: cambiar?
PORT = 5050
# TODO: cambiar?
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
MAX_CONEXIONES= 5
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
    connected = True
    while connected:
        # msg contiene el movimiento realizado por el Visitante
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            print(f" He recibido del servidor de colas [{addr}] el mensaje:\n{msg}")
            # TODO: Actualizar mapa
            # TODO: Quitar msg == FIN (Es automático)
            if msg == FIN:
                connected = False
            else:
                print("Enviando mapa actualizado...")
                connectToKAFKA(ADDR_KAFKA, msg)
                # TODO: conn y addr tienen que ser los de FAKFA?
                # conn.send(f"{msg}".encode(FORMAT))

    print("ADIOS. TE ESPERO EN OTRA OCASION")
    conn.close()

# Función que se encarga de concetar con el gestor de colas y enviarle el mapa actualizado
def connectToKAFKA(ADDR_KAFKA, msg): # (CLIENTE de KAFKA)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR_KAFKA)
    print (f"Establecida conexión en [{ADDR}]")
    # TODO: Enviar a Kafka el mapa actualizado
    while msg != FIN:
        print("SERVIDR: ", client.recv(2048).decode(FORMAT))
        msg = input()
    send(FIN, client)
    client.close()

# Engine empieza a escuchar al gestor de colas (Kafka)
def start(ADDR_KAFKA, PORT_ENGINE): # (SERVIDOR DE KAFKA)
    server.listen()
    print(f"[LISTENING] Servidor a la escucha en {SERVER}")
    CONEX_ACTIVAS = threading.active_count()-1
    print(f"{CONEX_ACTIVAS} / {MAX_CONEXIONES}")
    while True:
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

if  (len(sys.argv) == 4):
    SERVER_FAKFA = sys.argv[1]
    PORT_FAKFA = int(sys.argv[2])
    ADDR_KAFKA = (SERVER_FAKFA, PORT_FAKFA)

    PORT_ENGINE = sys.argv[3]

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    print("[STARTING ENGINE] Servidor inicializándose...")
    start(ADDR_KAFKA, PORT_ENGINE)
else:
    print ("Oops!. Parece que algo falló.\nNecesito estos argumentos:<ServerIP_FAKFA> <Puerto_FAKFA> <Puerto_Escucha>")