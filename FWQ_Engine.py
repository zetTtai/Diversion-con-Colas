import socket 
import sys
import time
import sqlite3
import json
import traceback
import threading
from kafka import KafkaConsumer
from kafka import KafkaProducer

HEADER = 2048
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
# Variable global que controla cada cuantos X segundos se conecta a STE
XSEC = 10
# Variable global para controlar el tamaño del mapa
MAXSIZE = 19
# Variable global que controla las posiciones de todos los visitantes monitorizados: Lista de tuplas [(ID, X, Y)]
POSICIONESVISITANTES = []

RESPUESTA = {
    "0": {
        "status" : "0",
        "message" : "OK"
    },

    "1": {
        "status" : "1",
        "message" : "Opcion es incorrecta [Entrar | Salir | Movimiento]"
    },

    "2": {
        "status" : "2",
        "message" : "Credenciales incorrectas, recuerde que debe estar registrado antes de entrar al parque."
    }, 

    "3": {
        "status" : "3",
        "message" : "Ya estas dentro del parque."
    },

    "4": {
        "status" : "4",
        "message" : "No estas fuera del parque."
    },

    "5": {
        "status" : "5",
        "message" : "Aforo maximo alcanzado, vuelva en otro momento"
    }
}

# Función que se encarga de enviar el mapa actualizado al gestor de colas
def send(msg, client):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def actualizarTiemposEspera(msg):
    conn = sqlite3.connect('db/database.db')
    print(f"Establecida conexión con la base de datos")
    cursor = conn.cursor()

    msg = json.loads(msg)
    for data in msg["datos"]:
        try:
            cursor.execute(f"SELECT * FROM atracciones WHERE id = '{data['id']}'")
            rows = cursor.fetchall()
            if rows: # Sólo actualizamos si la id existe en la base de datos
                cursor.execute(f'UPDATE atracciones SET wait_time = "{data["tiempo"]}" where id = "{data["id"]}"') # TODO: Comprobar que pasa cuando la ID no existe
                conn.commit()
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            conn.close()
    conn.close() # Cerramos base de datos

def visitorInsidePark(id):
    for visitante in POSICIONESVISITANTES:
        print(visitante)
        if visitante[0] == id:
            return True
    return False

def validateUser(id, password):
    conn = sqlite3.connect('db/database.db')
    print(f"Establecida conexión con la base de datos")
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM visitantes WHERE id = ? AND password = ?', (id, password))
        rows = cursor.fetchall()
        conn.close()
        if rows: # No está vacío
            return True
        else:
            return False
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
        conn.close()
        return False

def movement(origin, mov):
    # mov puede ser "-1" | "0" | "1"
    origin += int(mov)

    if origin > MAXSIZE:
        origin = 0
    elif origin < 0:
        origin = 19
    return origin

def updateMap(userID, mapa, id, movX, movY):
    mapa = json.loads(mapa)
    coordenada = ()

    # Actualizamos a QUIEN va enviado el mapa
    mapa["usuario"] = userID

    # Actualizamos tiempo de espera de las atracciones
    conn = sqlite3.connect('db/database.db')
    print(f"Establecida conexión con la base de datos")
    cursor = conn.cursor()
    try:
        cursor.execute(f'SELECT tiempo_espera FROM atracciones')
        rows = cursor.fetchall()
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
        conn.close()
    conn.close()
    # Suponiendo que todas las atracciones siguen el mismo orden que en la base de datos
    for row, atraccion in rows, mapa["atracciones"]:
        atraccion["tiempo"] = row[0]
    
    # Actualizamos la lista de posiciones
    if id == 0 and movX == 0 and movY == 0: # Nuevo visitante
        atracciones = mapa["atracciones"]
        visitantes = []
        for visitante in POSICIONESVISITANTES:
            data = {
                "id": visitante[0],
                "X" : visitante[1],
                "Y" : visitante[2]
            }
            visitantes.append(data)
        # Volvemos a montar el mapa pero esta vez añadiendo el nuevo visitante que está en POSICIONESVISITANTES
        mapa = {
            "usuario" : userID,
            "atracciones" : atracciones,
            "visitantes" : visitantes
        }
    else:
        for visitante in POSICIONESVISITANTES:
            if visitante[0] == id:
                visitante[1] = movement(visitante[1], movX)
                visitante[2] = movement(visitante[2], movY)
                coordenada = (visitante[1], visitante[2])
        # Actualizamos JSON
        for visitante in mapa["visitantes"]:
            if visitante["id"] == id:
                visitante["X"] = coordenada[0]
                visitante["Y"] == coordenada[1]

    mapa = json.dumps(mapa)
    return mapa

def initializeMap(userID):
    # Formato del mensaje mapa {
        # usuario : userID # Usuario al que va enviado el mapa
        # atracciones : [{id, tiempo, X, Y} ...] 
        # visitantes : [{id, X, Y} ...]
    # }
    atracciones = []
    conn = sqlite3.connect('db/database.db')
    print(f"Establecida conexión con la base de datos")
    cursor = conn.cursor()
    try:
        cursor.execute(f'SELECT * FROM atracciones')
        rows = cursor.fetchall()
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
        conn.close()
        return ""
    conn.close()
    for row in rows:
        position = row[2].split(' ')
        data = {
            "id": row[0],
            "tiempo" : row[1],
            "X" : position[0],
            "Y" : position[1]
        }
        atracciones.append(data)

    visitantes = []
    for visitante in POSICIONESVISITANTES:
        data = {
            "id": visitante[0],
            "X" : visitante[1],
            "Y" : visitante[2]
        }
        visitantes.append(data)

    mapa = {
        "usuario" : userID,
        "atracciones" : atracciones,
        "visitantes" : visitantes
    }
    # Convertimos a JSON
    mapa = json.dumps(mapa)
    return mapa

def sendResponse(userID, code):
    respuesta = json.dumps(RESPUESTA[code])
    respuesta = json.loads(respuesta)

    respuesta = {
        "id" : userID,
        "status" : respuesta["status"], 
        "message" : respuesta["message"]
    }

    respuesta = json.dumps(respuesta)
    return respuesta;

def connectionEngineKafka(SERVER_KAFKA, PORT_KAFKA, MAX_CONEXIONES):
    CONEX_ACTIVAS = 0
    print(f"{CONEX_ACTIVAS} / {MAX_CONEXIONES}")
    map = ""
    # Creamos el Productor
    producer= KafkaProducer(bootstrap_servers=f'{SERVER_KAFKA}:{PORT_KAFKA}')
    while True:
        if CONEX_ACTIVAS <= MAX_CONEXIONES:
            # Recibimos un mensaje de 'visitantes' donde se almacenan los movimientos de los visitantes
            # Y Engine es CONSUMIDOR de este topic
            consumer=KafkaConsumer('visitantes',bootstrap_servers=f'{SERVER_KAFKA}:{PORT_KAFKA}',auto_offset_reset='earliest')
            for message in consumer:
                print("Leemos el mensaje:")
                print(message.value) # {action: "", id: "", name: "", password: "", X:"", Y:""}
                message = message.value
                message = json.loads(message) # Convertimos a JSON
                if ("status" in message) == False:
                    if message["action"] == "Entrar":
                        print(f"El visitante[{message['id']}] quiere entrar")
                        if not visitorInsidePark(message["id"]):
                            #Validamos que esté registrado en la base de datos
                            if validateUser(message["id"], message["password"]) == True:
                                # Añadimos visitante a POSICIONESVISITANTES e inicializamos su posición en (0,0)
                                POSICIONESVISITANTES.append((message["id"], 0, 0))
                                CONEX_ACTIVAS += 1
                                if map == "":
                                    map = initializeMap(message["id"])
                                else:
                                    map = updateMap(message["id"], map, 0, 0, 0)
                                # El topic mapa será el que contenga toda la información del mapa que luego los visitantes CONSUMIRAN
                                producer.send('mapa',map.encode(FORMAT))
                                producer.send('visitantes', sendResponse(message["id"], "0").encode(FORMAT))
                                print("CONEXIONES RESTANTES PARA CERRAR EL SERVICIO", MAX_CONEXIONES-CONEX_ACTIVAS)
                            else:
                                producer.send('visitantes', sendResponse(message["id"], "2").encode(FORMAT))
                                print(f"El visitante[{message['id']}] NO está registrado")
                        else:
                            print("No puede entrar si ya está dentro")
                            # producer.send('mapa',"Ya estás dentro del parque.".encode(FORMAT))
                            producer.send('visitantes', sendResponse(message["id"], "3").encode(FORMAT))
                    elif message["action"] == "Salir":
                        print(f"El visitante[{message['id']}] quiere salir")
                        # Comprobar que el visitante está dentro del parque
                        if visitorInsidePark(message["id"]) == True:
                            #Validamos que esté registrado en la base de datos
                            if validateUser(message["id"], message["password"]) == True:
                            # Eliminamos visitante de POSICIONESVISITANTES
                                for visitante in POSICIONESVISITANTES:
                                    if visitante[0] == message["id"]:
                                        POSICIONESVISITANTES.remove(visitante)
                                        break
                                CONEX_ACTIVAS -= 1
                                producer.send('visitantes', sendResponse(message["id"], "0").encode(FORMAT))
                                print("CONEXIONES RESTANTES PARA CERRAR EL SERVICIO", MAX_CONEXIONES-CONEX_ACTIVAS)
                            else:
                                producer.send('visitantes', sendResponse(message["id"], "2").encode(FORMAT))
                                print(f"El visitante[{message['id']}] NO está registrado")
                        else:
                            print("No puede salir si ya esta fuera")
                            # producer.send('mapa',"Ya estás fuera del parque.".encode(FORMAT))
                            producer.send('visitantes', sendResponse(message["id"], "4").encode(FORMAT))
                    elif message["action"] == "Movimiento":
                        print(f"El visitante[{message['id']}] ha enviado un movimiento")
                        # Comprobar que el visitante no está dentro del parque
                        if visitorInsidePark(message["id"]) == True:
                            #Validamos que esté registrado en la base de datos
                            if validateUser(message["id"], message["password"]) == True:
                                map = updateMap(message["id"], map, message["id"], message["X"], message["Y"])
                                # Enviamos el mapa actualizado
                                producer.send('mapa',map.encode(FORMAT))
                                producer.send('visitantes', sendResponse(message["id"], "0"))
                            else:
                                producer.send('visitantes', sendResponse(message["id"], "2").encode(FORMAT))
                                print(f"El visitante[{message['id']}] NO está registrado")
                        else:
                            print("No puede realizar movimientos porque no está dentro del parque")
                            # producer.send('visitantes',"No estás dentro del parque.".encode(FORMAT))
                            producer.send('visitantes', sendResponse(message["id"], "4").encode(FORMAT))
                    else:
                        print("Action no controlada")
                        producer.send('visitantes', sendResponse(message["id"], "1").encode(FORMAT))
        else:
            print("AFORO ALCANZADO")
            producer.send('visitantes', sendResponse(message["id"], "5").encode(FORMAT))

# Función que se encarga de actualizar los tiempos de espera de las atracciones
def connectionEngineSTE(SERVER_STE, PORT_STE):
    ADDR_STE = (SERVER_STE, PORT_STE)
    start = time.time()
    while True:
        if round((time.time() - start)) >= XSEC:
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(ADDR_STE)
                print (f"Establecida conexión en [{ADDR_STE}] (Servidor de Tiempos de Espera)")
                # print("SERVIDR: ", client.recv(2048).decode(FORMAT))
                actualizarTiemposEspera(client.recv(2048).decode(FORMAT))
                client.close()
                start = time.time() # Reseteamos el timer
            except ConnectionRefusedError as error:
                print(f"No se ha podido conectar con STE en [{ADDR_STE}]")
                start = time.time()

def start(SERVER_KAFKA, PORT_KAFKA, SERVER_STE, PORT_STE, MAX_CONEXIONES):
    server.listen()
    print(f"[LISTENING] Servidor a la escucha en {SERVER}")

    threadKafka = threading.Thread(target=connectionEngineKafka, args=(SERVER_KAFKA, PORT_KAFKA, MAX_CONEXIONES))
    threadSTE = threading.Thread(target=connectionEngineSTE, args=(SERVER_STE, PORT_STE))

    threadKafka.start()
    threadSTE.start()

########## MAIN ##########

if  (len(sys.argv) == 6):
    SERVER_KAFKA = sys.argv[1]
    PORT_KAFKA = int(sys.argv[2])

    SERVER_STE = sys.argv[3]
    PORT_STE = int(sys.argv[4])

    MAX_CONEXIONES = int(sys.argv[5])

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    print("[STARTING ENGINE] Servidor inicializándose...")
    start(SERVER_KAFKA, PORT_KAFKA, SERVER_STE, PORT_STE, MAX_CONEXIONES)
else:
    print ("Oops!. Parece que algo falló.\nNecesito estos argumentos:<ServerIP_FAKFA> <Puerto_FAKFA> <SERVERIP_STE> <PUERTO_STE> <Nº MAX VISITANTES>")
