import socket 
import sys
import threading

HEADER = 64
# TODO: cambiar?
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
FILE = "DATA.txt"

# Función para calcular el timepo de espera
def calculateWaitTime(tiempo, visitantes):
    return 0

# Función que escribe en el fichero donde se guardan los datos de las atracciones
def writeFile(msg):
    # Cada línea corresponde a una atracción y cada línea tiene el formato de: ID tiempo_ciclo nº_visitantes
    # Si ya existía entonces se actualiza la linea, en caso contrario se añade al final
    msg = msg.split(' ') # "ID nºvisitantes"
    fichero = open(FILE, "r")
    list_of_lines = fichero.readlines()
    fichero.close()

    existe= False
    for i, line in enumerate(list_of_lines):
        if line.startswith(msg[0]):
            existe= True
            info = list_of_lines[i]
            info = info.split(' ') # ID tiempo_ciclo nº_visitantes
            if msg[2] == "+":
                visitantes = int(info[2]) + int(msg[1])# Sumamos los visitantes antiguos + los nuevos
            else:
                visitantes = int(info[2]) - int(msg[1]) # Sumamos los visitantes antiguos + los nuevos
                if(visitantes < 0): 
                    visitantes = 0
            list_of_lines[i] = msg[0] + ' ' + visitantes + '\n'
    
    fichero = open(FILE, "w")
    if(existe):
        fichero.writelines(list_of_lines)
    else:
        fichero.write(msg[0] + ' ' + msg[1] + '\n')
    fichero.close()


# Función que devuelve un string con todos los tiempos guardados en el fichero
def readFile():
    fichero = open(FILE, 'r')
    list_of_lines = fichero.readlines()
    fichero.close()
    res= ""
    for line in list_of_lines:
        line.split()
        # ID-TiempoEspera ID-TiempoEspera ...
        res += line[0] + '-' + calculateWaitTime(line[1], line[2]) + ' '
    return res


# Recibimos petición de Engine
def handle_client(conn, addr):
    print(f"[NUEVA CONEXION] {addr} connected.")
    print("Engine se ha conectado")
    # TODO: Enviar a Engine los nuevos tiempo de espera
    print("Extrayendo datos del fichero")
    msg = readFile()
    print("Enviando datos a Engine")
    conn.send(f"{msg}".encode(FORMAT))
        
    # Terminamos de enviar la información a Engine sobre los tiempo de espera
    print("Fin de la conexión")
    x = input()
    conn.close()


def start(ADDR_KAFKA):
    server.listen()
    print(f"[LISTENING] Servidor a la escucha en {SERVER}")

    # Escuchamos indefinidamente
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        # TODO: Gestionar los mensajes recibidos por el gestor de colas (Sensores)
        msg=""
        writeFile(msg)
    

########## MAIN ##########

if  (len(sys.argv) == 4):
    SERVER_FAKFA = sys.argv[1]
    PORT_FAKFA = int(sys.argv[2])
    ADDR_KAFKA = (SERVER_FAKFA, PORT_FAKFA)

    PORT = int(sys.argv[3])
    ADDR = (SERVER, PORT)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    print("[STARTING WTS] Servidor inicializándose...")
    start(ADDR_KAFKA)
else:
    print ("Oops!. Parece que algo falló.\nNecesito estos argumentos:<ServerIP_FAKFA> <Puerto_FAKFA> <Puerto_Escucha>")