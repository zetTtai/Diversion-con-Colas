import socket 
import threading
import sys

HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
FIN = "FIN"
MAX_CONEXIONES = 5

def handle_client(conn, addr):
    print(f"[NUEVA CONEXION] {addr} connected.")
    while True:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            print(f" He recibido del cliente [{addr}] el mensaje: {msg}")
            msg = msg.split(" ")
            # TODO: Gestionar la información dada por el usuario y guardarla en SQLite
            break;

    print("ADIOS. TE ESPERO EN OTRA OCASION")
    conn.close()
        
def start():
    server.listen()
    print(f"[LISTENING] Servidor a la escucha en {SERVER}")
    CONEX_ACTIVAS = threading.active_count()-1
    print(CONEX_ACTIVAS)
    while True:
        conn, addr = server.accept()
        CONEX_ACTIVAS = threading.active_count()
        if (CONEX_ACTIVAS <= MAX_CONEXIONES): 
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[CONEXIONES ACTIVAS] {CONEX_ACTIVAS}")
            print("CONEXIONES RESTANTES PARA CERRAR EL SERVICIO", MAX_CONEXIONES-CONEX_ACTIVAS)
        else:
            print("OOppsss... DEMASIADAS CONEXIONES. ESPERANDO A QUE ALGUIEN SE VAYA")
            conn.send("OOppsss... DEMASIADAS CONEXIONES. Tendrás que esperar a que alguien se vaya".encode(FORMAT))
            conn.close()
            CONEX_ACTUALES = threading.active_count()-1
        

######################### MAIN ##########################

if(len(sys.argv) == 2):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    PORT= int(sys.argv[1])
    ADDR = (SERVER, PORT)
    server.bind(ADDR)

    print("[STARTING] Servidor inicializándose...")

    start()
else:
    print ("Oops!. Parece que algo falló. Necesito estos argumentos: <Puerto_Escucha>")

