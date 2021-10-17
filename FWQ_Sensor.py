import socket
import sys
import time

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
XSEC= 3
FIN = "FIN"

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    
########## MAIN ##########

if  (len(sys.argv) == 4):
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (SERVER, PORT)
    ID = int(sys.argv[3])
    msg = ""
    start = time.time()
    while True:
        # Cada X segundos se conecta a STE para actualizar los tiempos de espera de las atracciones
        if (round((time.time() - start)) == XSEC):
            # TODO: SOCKETS != Streaming & QM?
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(ADDR)
            print (f"Establecida conexión con el gestor de colas [{ADDR}]")
            # TODO: Enviar el número de personas que se encuentran en la atracción correspondiente a ID
                ########
            print('Enviar mensaje (Debería ser automático)')
            msg = input()
            print('Enviando mensaje.... ' + msg + "\n")
            send(msg)
            print("SERVIDOR: ", client.recv(2048).decode(FORMAT))
                ########
            print('Finalizando conexión...')
            client.close()
            start = time.time() # Reseteamos el timer
else:
    print ("Oops!. Parece que algo falló. Necesito estos argumentos: <ServerIP_FAKFA> <Puerto_FAKFA> <ID_Atracción>")
