import socket 
import sys
import time
import sqlite3
import traceback
from kafka import KafkaConsumer
from kafka import KafkaProducer

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
# Variable global que controla cada cuantos X segundos se conecta a STE
XSEC = 10
# Variable global que controla las posiciones de todos los visitantes monitorizados
PosicionesVisitantes = []

# Función que se encarga de enviar el mapa actualizado al gestor de colas
def send(msg, client):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def actualizarTiemposEspera(msg): # msg=  ID-Tiempo ID-Tiempo ...
    conn = sqlite3.connect('db/database.db')
    print(f"Establecida conexión con la base de datos")
    cursor = conn.cursor()
    # TODO: Cambiar a leer JSONs
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

    conn.close() # Cerramos base de datos

# Función que se encarga de actualizar los tiempos de espera de las atracciones
def connectToSTE(ADDR_STE): # (CLIENTE de STE)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR_STE)
    print (f"Establecida conexión en [{ADDR}]")
    # print("SERVIDR: ", client.recv(2048).decode(FORMAT))
    actualizarTiemposEspera(client.recv(2048).decode(FORMAT))
    client.close()

# Devuelve verdadero si el visitante con la 'id' pasada por parametros está dentro del parque
def visitorInsidePark(id):
    conn = sqlite3.connect('db/database.db')
    print(f"Establecida conexión con la base de datos")
    cursor = conn.cursor()
    try:
        cursor.execute(f'SELECT * FROM visitantes WHERE id = {id} AND dentro = 1')
        rows = cursor.fetchall()
        # TODO: Comprobar que funciona bien
        if rows: 
            conn.close()
            return True
        else: # rows está vacío, por tanto, el visitante[id] NO está dentro
            conn.close()
            return False
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
        conn.close()
        return False

# Función que cambia el valor del atributo 'dentro' de un usuario específico
# La variable info solo puede tener como valores [1 y 0] [True False]
def visitanteEntrandoSaliendo(id, info):
    conn = sqlite3.connect('db/database.db')
    print(f"Establecida conexión con la base de datos")
    cursor = conn.cursor()
    try:
        cursor.execute(f'UPDATE visitantes SET dentro = "{info}" where id = {id}')
        conn.commit()
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
        conn.close()
    conn.close()

# TODO: To do
def updateMap(id, movimiento):
    return ""

def initializeMap():
    # Formato del mensaje mapa
    # Información de atracciones : "[ID]-[Tiemp_Espera]-[Posicion] []-[]-[] ..."
    # Información de visitantes  : "[ID]-[Posicion] []-[] ..."

    


    return ""

# Engine empieza a escuchar al gestor de colas (Kafka)
def start(SERVER_KAFKA, PORT_KAFKA, MAX_CONEXIONES): # (SERVIDOR DE KAFKA)
    server.listen()
    print(f"[LISTENING] Servidor a la escucha en {SERVER}")
    CONEX_ACTIVAS = 0
    print(f"{CONEX_ACTIVAS} / {MAX_CONEXIONES}")
    map = ""
    start = time.time()
    while True:
        # Cada X segundos se conecta a STE para actualizar los tiempos de espera de las atracciones
        if (round((time.time() - start)) == XSEC):
            connectToSTE(ADDR_STE)
            start = time.time() # Reseteamos el timer

        # Creamos el Productor
        producer= KafkaProducer(bootstrap_servers=f'{SERVER_KAFKA}:{PORT_KAFKA}')

        if (CONEX_ACTIVAS <= MAX_CONEXIONES):
            # Recibimos un mensaje de 'visitantes' donde se almacenan los movimientos de los visitantes
            # Y Engine es CONSUMIDOR de este topic
            consumer=KafkaConsumer('visitantes',bootstrap_servers=f'{SERVER_KAFKA}:{PORT_KAFKA}',auto_offset_reset='earliest')
            for message in consumer:
                # TODO: Cambiar a leer un JSON
                print(message) # [ACCION] [ID_Visitante] ([Movimiento])
                message = message.split(' ')
                if (message[0] == "Entrar"):
                    print(f"El visitante[{message[1]}] quiere entrar")
                    # Comprobar que el visitante no está dentro del parque
                    if(visitorInsidePark(message[1]) == False):
                        visitanteEntrandoSaliendo(message[1],1) # Hacemos que el usuario entre al parque
                        CONEX_ACTIVAS += 1
                        producer.send('mapa',"Disfrute de su visita")
                        if(map == ""):
                            map = initializeMap()
                        else:
                            map = updateMap()
                        # TODO: Enviar mapa al visitante que acaba de entrar
                        # El topic mapa será el que contenga toda la información del mapa que luego los visitantes CONSUMIRAN
                        producer.send('mapa',map.encode(FORMAT))
                        print("CONEXIONES RESTANTES PARA CERRAR EL SERVICIO", MAX_CONEXIONES-CONEX_ACTIVAS)
                    else:
                        print("No puede entrar si ya está dentro")
                        producer.send('mapa',"Ya estás dentro del parque.".encode(FORMAT))
                elif(message[0] == "Salir"):
                    print(f"El visitante[{message[1]}] quiere salir")
                    # Comprobar que el visitante está dentro del parque
                    if(visitorInsidePark(message[1]) == True):
                        visitanteEntrandoSaliendo(message[1],0) # Hacemos que el usuario salga al parque
                        CONEX_ACTIVAS -= 1
                        producer.send('visitantes',"Esperamos que haya disfrutado de su visita, ¡venga en otra ocasión!")
                        print("CONEXIONES RESTANTES PARA CERRAR EL SERVICIO", MAX_CONEXIONES-CONEX_ACTIVAS)
                    else:
                        print("No puede salir si ya esta fuera")
                        producer.send('mapa',"Ya estás fuera del parque.".encode(FORMAT))
                elif(message[0] == "Movimiento"):
                    print(f"El visitante[{message[1]}] ha envaido un movimiento")
                    # Comprobar que el visitante no está dentro del parque
                    if(visitorInsidePark(message[1]) == True):
                        map = updateMap(message[1], message[2])
                        # Enviamos el mapa actualizado
                        producer.send('mapa',map.encode(FORMAT))
                    else:
                        print("No puede realizar movimientos porque no está dentro del parque")
                        producer.send('visitantes',"No estás dentro del parque.".encode(FORMAT))
        else:
            print("AFORO ALCANZADO")
            # TODO: Se le envia a todos? Un topic por cada visitante
            producer.send('mapa',"El parque ha alcanzado su aforo máximo, vuelve en otro momento.".encode(FORMAT))
    
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
