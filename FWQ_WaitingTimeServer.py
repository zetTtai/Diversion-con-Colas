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

# Recibimos petición de Engine
def handle_client(conn, addr, PORT_ENGINE):
    print(f"[NUEVA CONEXION] {addr} connected.")
    # Comprobamos que quien se conecta es Engine
    if(conn.port == PORT_ENGINE):
        while True:
            # msg contiene el movimiento realizado por el Visitante
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                print(f" He recibido de Engine [{addr}] el mensaje:\n{msg}")
                # TODO: Enviar a Engine los nuevos tiempo de espera
                
            # Terminamos de enviar la información a Engine sobre los tiempo de espera
            print("Fin de la conexión")
            x = input()
            break;
        conn.close()
    else:
        conn.send(f"ERROR: Tu puerto [{conn.port}] no es válido.".encode(FORMAT))
        conn.close()

# TODO: No se conecta por sockets
# def connectToKAFKA(ADDR_KAFKA, msg): # (CLIENTE de KAFKA)
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client.connect(ADDR_KAFKA)
#     print (f"Establecida conexión en [{ADDR}]")
#     # TODO: Enviar a Kafka el mapa actualizado
#     while msg != FIN:
#         print("SERVIDR: ", client.recv(2048).decode(FORMAT))
#         msg = input()
#     send(FIN, client)
#     client.close()


def start(ADDR_KAFKA, PORT_ENGINE): # (SERVIDOR DE KAFKA)
    server.listen()
    print(f"[LISTENING] Servidor a la escucha en {SERVER}")

    # Escuchamos indefinidamente
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr, PORT_ENGINE))
        thread.start()
    

########## MAIN ##########

if  (len(sys.argv) == 4):
    SERVER_FAKFA = sys.argv[1]
    PORT_FAKFA = int(sys.argv[2])
    ADDR_KAFKA = (SERVER_FAKFA, PORT_FAKFA)

    PORT_ENGINE = int(sys.argv[3])

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    print("[STARTING WTS] Servidor inicializándose...")
    start(ADDR_KAFKA, PORT_ENGINE)
else:
    print ("Oops!. Parece que algo falló.\nNecesito estos argumentos:<ServerIP_FAKFA> <Puerto_FAKFA> <Puerto_Escucha>")