from kafka import KafkaConsumer
from kafka import KafkaProducer
from pyowm import OWM
import traceback
import threading
import hashlib
import sqlite3
import socket
import time
import json
import sys
import os

HEADER = 2048
FORMAT = 'utf-8'
# Variable global que controla cada cuantos X segundos se conecta a STE
XSEC = 10
# Variable global para controlar el tamaño del mapa
MAXSIZE = 19
# Variable global que contiene la dirección del backup del mapa del parque de atracciones
BACKUP = "mapa.json"
# Variable global que contiene la dirección de la configuración inicial del programa
CONFIG_FILE = "config.json"
CONFIG = {}
# Variable global que contiene el mapa del parque de atracciones
MAPA = {
    "atracciones" : [],
    "visitantes" : [],
    "weather" : ""
}

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
        "message" : "Ya estas fuera del parque."
    },

    "5": {
        "status" : "5",
        "message" : "Aforo maximo alcanzado, vuelva en otro momento"
    }
}

#### OPENWEATHERMAP #####
def WeatherOn(ciudad, api_key) -> int:
    owm = OWM(api_key)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(ciudad)
    w = observation.weather
    return w.temperature('celsius')['temp']  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}

def OWMCalculate():
    fichero = open(CONFIG_FILE, 'r')
    WEATHER = json.load(fichero)['weather']
    fichero.close()
    ciudades_json = {
        "ciudad1" : {
            "nombre" : WEATHER['ciudad1'],
            "temp" : WeatherOn(WEATHER['ciudad1'], WEATHER['api_key'])
        },
        "ciudad2" : {
            "nombre" : WEATHER['ciudad2'],
            "temp" : WeatherOn(WEATHER['ciudad2'], WEATHER['api_key'])
        },
        "ciudad3" : {
            "nombre" : WEATHER['ciudad3'],
            "temp" : WeatherOn(WEATHER['ciudad3'], WEATHER['api_key'])
        },
        "ciudad4" : {
            "nombre" : WEATHER['ciudad4'],
            "temp" : WeatherOn(WEATHER['ciudad4'], WEATHER['api_key'])
        },
    }
    return ciudades_json

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
    for visitante in MAPA["visitantes"]:
        if visitante["id"] == id:
            return True
    return False

def check_password(cursor, id, key):
    # Comprobamos que sea el usuario y la contraesña coincidan con lo guardado en la base de datos
    cursor.execute(f'SELECT password FROM visitantes WHERE id = "{id}"')
    row = cursor.fetchone()
    # Si existe el visitante
    if row:
        password, salt = row[0].split(':')
        # Comprobamos la contraseña pasada por parámetros (visitante[1]) con la almacenada en la base de datos (row[0])
        return password == hashlib.sha256(salt.encode() + key.encode()).hexdigest()
    print("Ese usuario no existe")
    return False

def validateUser(id, password):
    conn = sqlite3.connect('db/database.db')
    print(f"Establecida conexión con la base de datos")
    cursor = conn.cursor()
    try:
        if check_password(cursor, id, password):
            return True
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

def actualizarAtracciones():
    atracciones = []
    conn = sqlite3.connect('db/database.db')
    # print(f"Establecida conexión con la base de datos")
    cursor = conn.cursor()
    try:
        cursor.execute(f'SELECT * FROM atracciones WHERE wait_time IS NOT 0')
        rows = cursor.fetchall()
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
        conn.close()
        return atracciones #Vacio
    conn.close()
    data = {}
    for row in rows:
        position = row[2].split(' ')
        data = {
            "id": row[0],
            "tiempo" : row[1],
            "X" : position[0],
            "Y" : position[1]
        }
    atracciones.append(data)
    return atracciones # Con tiempo de espera != 0

def updateMap(userID, id, movX, movY):

    # Actualizamos a QUIEN va enviado el mapa
    MAPA["usuario"] = userID

    # Actualizamos tiempo de espera de las atracciones
    MAPA["atracciones"] = actualizarAtracciones()

    # Actualizamos la lista de posiciones
    if id == 0 and movX == 0 and movY == 0: # Nuevo visitante
        visitantes = []
        if MAPA["visitantes"] is not None:
            for visitante in MAPA["visitantes"]:
                data = {
                    "id": visitante["id"],
                    "X" : visitante["X"],
                    "Y" : visitante["Y"]
                }
                visitantes.append(data)
            # Volvemos a montar el mapa pero esta vez añadiendo el nuevo visitante
        MAPA["visitantes"] = visitantes
    else:
        print("Actualizando posición")
        for visitante in MAPA['visitantes']:
            if visitante["id"] == id:
                visitante["X"] = movement(visitante["X"], movX)
                visitante["Y"] = movement(visitante["Y"], movY)
    print("ACTUALIZAR")
    print(MAPA["visitantes"])
    weather = OWMCalculate()
    MAPA['weather'] = weather

def sendResponse(userID, code, timestamp):
    respuesta = json.dumps(RESPUESTA[code])
    respuesta = json.loads(respuesta)

    respuesta = {
        "id" : userID,
        "status" : respuesta["status"],
        "message" : respuesta["message"],
        "timestamp_request" : timestamp
    }

    respuesta = json.dumps(respuesta)
    return respuesta

def procesarEntrada(producer, message, CONEX_ACTIVAS):
    print(f"El visitante[{message['id']}] quiere entrar")
    if not visitorInsidePark(message["id"]):
        #Validamos que esté registrado en la base de datos
        if validateUser(message["id"], message["password"]) == True:
            visitante = {
                "id" : message["id"],
                "X"  : 0,
                "Y"  : 0
            }
            MAPA["visitantes"].append(visitante)
            print("AÑADIR")
            print(MAPA["visitantes"])
            CONEX_ACTIVAS += 1
            updateMap(message["id"], 0, 0, 0)
            # El topic mapa será el que contenga toda la información del mapa que luego los visitantes CONSUMIRAN
            producer.send('mapa', json.dumps(MAPA).encode(FORMAT))
            producer.send('visitantes', sendResponse(message["id"], "0", message['timestamp']).encode(FORMAT))
            print("CONEXIONES RESTANTES PARA CERRAR EL SERVICIO", CONFIG['max_connections']-CONEX_ACTIVAS)
        else:
            producer.send('visitantes', sendResponse(message["id"], "2", message['timestamp']).encode(FORMAT))
            print(f"El visitante[{message['id']}] NO está registrado")
    else:
        print("No puede entrar si ya está dentro")
        producer.send('visitantes', sendResponse(message["id"], "3", message['timestamp']).encode(FORMAT))

def procesarSalida(producer, message, CONEX_ACTIVAS):
    print(f"El visitante[{message['id']}] quiere salir")
    # Comprobar que el visitante está dentro del parque
    if visitorInsidePark(message["id"]) == True:
        #Validamos que esté registrado en la base de datos
        if validateUser(message["id"], message["password"]) == True:
            # Eliminamos visitante
            for visitante in MAPA["visitantes"]:
                if visitante["id"] == message["id"]:
                    MAPA["visitantes"].remove(visitante)
            print("ELIMINAR")
            print(MAPA["visitantes"])
            CONEX_ACTIVAS -= 1
            producer.send('visitantes', sendResponse(message["id"], "0", message['timestamp']).encode(FORMAT))
            print("CONEXIONES RESTANTES PARA CERRAR EL SERVICIO", CONFIG['max_connections']-CONEX_ACTIVAS)
        else:
            producer.send('visitantes', sendResponse(message["id"], "2", message['timestamp']).encode(FORMAT))
            print(f"El visitante[{message['id']}] NO está registrado")
    else:
        print("No puede salir si ya esta fuera")
        # producer.send('mapa',"Ya estás fuera del parque.".encode(FORMAT))
        producer.send('visitantes', sendResponse(message["id"], "4", message['timestamp']).encode(FORMAT))

def procesarMovimiento(producer, message):
    print(f"El visitante[{message['id']}] ha enviado un movimiento")
    # Comprobar que el visitante no está dentro del parque
    if visitorInsidePark(message["id"]) == True:
        #Validamos que esté registrado en la base de datos
        if validateUser(message["id"], message["password"]) == True:
            updateMap(message["id"], message["id"], message["X"], message["Y"])
            # Enviamos el mapa actualizado
            producer.send('mapa',json.dumps(MAPA).encode(FORMAT))
            producer.send('visitantes', sendResponse(message["id"], "0", message['timestamp']).encode(FORMAT))
        else:
            producer.send('visitantes', sendResponse(message["id"], "2", message['timestamp']).encode(FORMAT))
            print(f"El visitante[{message['id']}] NO está registrado")
    else:
        print("No puede realizar movimientos porque no está dentro del parque")
        producer.send('visitantes', sendResponse(message["id"], "4", message['timestamp']).encode(FORMAT))

def restoreMap():
    global MAPA
    # Comprobamos si hay información en el BACKUP
    if os.stat(BACKUP).st_size != 0:
        print("Recuperando mapa")
        fichero = open(BACKUP, 'r')
        MAPA = json.loads(fichero.read())
        fichero.close()
        # Actualizamos MAPA["visitantes"] con los visitantes del fichero
        # if "visitantes" in MAPA:
        #     for visitante in MAPA["visitantes"]:
        #         MAPA["visitantes"].append({
        #             "id" : visitante["id"],
        #             "X"  : visitante["X"],
        #             "Y"  : visitante["Y"]
        #         })

def backUpMap():
    print("Guardando mapa")
    fichero = open(BACKUP,"w")
    fichero.write(json.dumps(MAPA, indent=4))
    fichero.close()


def connectionEngineKafka(SERVER_KAFKA, PORT_KAFKA, MAX_CONEXIONES):
    CONEX_ACTIVAS = 0
    print(f"{CONEX_ACTIVAS} / {MAX_CONEXIONES}")
    start = time.time()*1000
    restoreMap()
    # Creamos el Productor
    producer= KafkaProducer(bootstrap_servers=f'{SERVER_KAFKA}:{PORT_KAFKA}')
    while True:
        # Recibimos un mensaje de 'visitantes' donde se almacenan los movimientos de los visitantes
        # Y Engine es CONSUMIDOR de este topic
        consumer=KafkaConsumer('visitantes', group_id="engine", bootstrap_servers=f'{SERVER_KAFKA}:{PORT_KAFKA}')
        for message in consumer:
            message = json.loads(message.value) # Convertimos a JSON
            if "timestamp" not in message or message["timestamp"] < (start - 60*1000):
                continue
            if MAX_CONEXIONES-CONEX_ACTIVAS > 0:
                if ("status" in message) == False:
                    print("Leemos el mensaje:")
                    if message["action"] == "Movimiento":
                        procesarMovimiento(producer, message)
                    elif message["action"] == "Entrar":
                        procesarEntrada(producer, message, CONEX_ACTIVAS)
                    elif message["action"] == "Salir":
                        procesarSalida(producer, message, CONEX_ACTIVAS)
                    else:
                        print("Action no controlada")
                        producer.send('mapa', sendResponse(message["id"], "1", message['timestamp']).encode(FORMAT))
                    # Realizamos backup por cada acción que realizan los visitantes
                    backUpMap()
            else:
                if visitorInsidePark(message["id"]) == False:
                    print("AFORO ALCANZADO")
                    producer.send('visitantes', sendResponse(message["id"], "5", message['timestamp']).encode(FORMAT))

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

########## MAIN ##########

def main():
    global CONFIG_FILE
    global CONFIG

    if not os.path.exists(CONFIG_FILE):
        return
    try:
        print("Se ha detectado un fichero de configuración. Se procederá a cargarlo.")
        fichero = open(CONFIG_FILE, "r")
        CONFIG = json.load(fichero)['engine']
        fichero.close()
    except Exception as e:
        print(f"Error al cargar el fichero de configuración: {e}")
        return

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((CONFIG['listen_ip'], CONFIG['listen_port']))
    print("[STARTING ENGINE] Servidor inicializándose...")
    server.listen()
    print(f"[LISTENING] Servidor a la escucha en {CONFIG['listen_ip']}:{CONFIG['listen_port']}")

    threadKafka = threading.Thread(target=connectionEngineKafka, args=(CONFIG['kafka_ip'], CONFIG['kafka_port'], CONFIG['max_connections']))
    threadSTE   = threading.Thread(target=connectionEngineSTE,   args=(CONFIG['ste_ip'],   CONFIG['ste_port']))

    threadKafka.start()
    threadSTE.start()

if __name__ == "__main__":
    main()