import socket 
import sys
import threading
import time

HEADER = 64
PORT = 5050
# TODO: cambiar?
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
# TODO: Quitar en un futuro
FIN = "FIN"
XSEC = 30

# Función que se encarga de enviar el mapa actualizado al gestor de colas
def send(msg, client):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

# Función que se encarga de actualizar el mapa según el movimiento recibido por argumentos
def handle_client(conn, addr):
    print(f"[NUEVA CONEXION] {addr} connected.")
    connected = True
    while connected:
        # msg contiene el movimiento realizado por el Visitante
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            print(f" He recibido del servidor de colas [{addr}] el mensaje:\n{msg}")
            if msg == FIN:
                connected = False
            else:
                print("Enviando mapa actualizado")
                conn.send(f"{msg}".encode(FORMAT))

    print("ADIOS. TE ESPERO EN OTRA OCASION")
    conn.close()

# Engine empieza a escuchar al gestor de colas (Kafka)
def start(MAX_CONEXIONES):
    server.listen()
    print(f"[LISTENING] Servidor a la escucha en {SERVER}")
    CONEX_ACTIVAS = threading.active_count()-1
    print(f"{CONEX_ACTIVAS} / {MAX_CONEXIONES}")
    print("wtf")
    start = time.time()
    print("wtf")
    while True:
        
        if (round((time.time() - start)) == XSEC):
            print("ichi bio keka")
            input()
            start = time.time()
        # conn, addr = server.accept()
        # CONEX_ACTIVAS = threading.active_count()
        if (CONEX_ACTIVAS <= MAX_CONEXIONES): 
            # thread = threading.Thread(target=handle_client, args=(conn, addr))
            # thread.start()
            print(f"[CONEXIONES ACTIVAS] {CONEX_ACTIVAS}")
            # print("CONEXIONES RESTANTES PARA CERRAR EL SERVICIO", MAX_CONEXIONES-CONEX_ACTIVAS)
        else:
            print("AFORO ALCANZADO")
            # conn.send("El parque ha alcanzado su aforo máximo, vuelve en otro momento.".encode(FORMAT))
            # conn.close()
            CONEX_ACTUALES = threading.active_count()-1
    
########## MAIN ##########

if  (len(sys.argv) == 6):
    SERVER_FAKFA = sys.argv[1]
    PORT_FAKFA = int(sys.argv[2])
    ADDR_FAKFA = (SERVER_FAKFA, PORT_FAKFA)

    SERVER_STE = sys.argv[3]
    PORT_STE = int(sys.argv[4])
    ADDR_STE = (SERVER_STE, PORT_STE)

    MAX_CONEXIONES = int(sys.argv[5])

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    print("[STARTING ENGINE] Servidor inicializándose...")
    start(10)
else:
    print ("Oops!. Parece que algo falló.\nNecesito estos argumentos:<ServerIP_FAKFA> <Puerto_FAKFA> <SERVERIP_STE> <PUERTO_STE> <Nº MAX VISITANTES>")
