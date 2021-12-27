import socket 
import threading
import sys
import sqlite3
import traceback
import json
#Práctica 3
from flask import Flask, make_response, request, jsonify
import uuid
import hashlib
import datetime

HEADER = 2048
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
FIRST = True

RESPUESTA = {
    "0": {
        "status" : "0",
        "message" : "OK"
    },

    "1": {
        "status" : "1",
        "message" : "Opción es incorrecta [create | edit | delete]"
    },

    "2": {
        "status" : "2",
        "message" : "Fallo al crear el perfil"
    }, 

    "3": {
        "status" : "3",
        "message" : "Fallo al editar el perfil"
    },

    "4": {
        "status" : "4",
        "message" : "Fallo al borrar el perfil"
    }
}

#############################################################
######################### FUNCIONES #########################
#############################################################

def deleteVisitor(msg, ipVisitante):
    conn = sqlite3.connect('db/database.db')
    print(f"Establecida conexión con la base de datos")
    cursor = conn.cursor()
    params = f'ID: {msg["id"]} | PASSWORD: {hash_password(msg["password"])}'
    try:
        if check_password(cursor, msg["id"], msg["password"]):
            cursor.execute('DELETE FROM visitantes WHERE id = ?', (msg["id"],))
            conn.commit()
        else:
            print("El usuario y la contraseña no coinciden")
            generateRegister(cursor, conn, "Error", ipVisitante, params)
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
    generateRegister(cursor, conn, "Baja", ipVisitante, params)
    conn.close()
    return True

def createVisitor(msg, ipVisitante):
    conn = sqlite3.connect('db/database.db')
    print(f"Establecida conexión con la base de datos")
    cursor = conn.cursor()

    visitante= (msg["id"], msg["name"], hash_password(msg["password"]))
    try:
        # Buscamos si ya existe ese perfil
        cursor.execute(f'SELECT * FROM visitantes WHERE id = "{msg["id"]}"')
        rows = cursor.fetchall()
        params = f'ID: {msg["id"]} | PASSWORD: {hash_password(msg["password"])} | NAME: {msg["name"]}'
        if rows:
            generateRegister(cursor, conn, "Error", ipVisitante, params)
            conn.close()
            return False
        else:
            cursor.execute('INSERT INTO visitantes(id, name, password) VALUES(?, ?, ?)', visitante)
            conn.commit()
            generateRegister(cursor, conn, "Crear", ipVisitante, params)
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
        conn.close()
        return False
    conn.close()
    return True

def editVisitor(msg, ipVisitante): 
    conn = sqlite3.connect('db/database.db')
    print(f"Establecida conexión con la base de datos")
    cursor = conn.cursor()
    # ID no se puede cambiar
    try:
        params = f'ID: {msg["id"]} | PASSWORD: {hash_password(msg["password"])} | NAME: {msg["name"]} | newPASSWORD: {hash_password(msg["new_password"])}'
        if check_password(cursor, msg["id"], msg["password"]):
            cursor.execute('UPDATE visitantes SET name = ?, password = ? WHERE id = ?', (msg["name"], hash_password(msg["new_password"]), msg["id"]))
            conn.commit()
            generateRegister(cursor, conn, "Modificación", ipVisitante, params)
        else:
            print("El usuario y la contraseña no coinciden")
            generateRegister(cursor, conn, "Error", ipVisitante, params)
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

    print(f"Cerrando conexión con la base de datos")
    conn.close()
    return True

def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

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


def generateRegister(cursor, conn, action, ipVisitante, params):
    print(f"Generando registro...")
    # ipVisitante es una tupla
    print(ipVisitante[0])
    print(params)
    print("==============================")
    timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    try:
        cursor.execute('INSERT INTO registros(timestamp, ip, action, params) VALUES(?, ?, ?, ?)', (timestamp, ipVisitante[0], action, params))
        conn.commit()
        print("Registro almacenado")
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))

#######################################################
######################### API #########################
#######################################################

app = Flask(__name__)

@app.route("/profile", methods=["POST"])
def create():
    print("Creando perfil mediante API")
    if createVisitor(request.json, request.remote_addr):
        response = make_response(jsonify(RESPUESTA["0"]), 200)
        response.headers["Content-Type"] = "application/json"
        return response
    response = make_response(jsonify(RESPUESTA["2"]), 403)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route("/profile", methods=["PUT"])
def update():
    print("Actualizando perfil mediante API")
    if editVisitor(request.json, request.remote_addr):
        response = make_response(jsonify(RESPUESTA["0"]), 200)
        response.headers["Content-Type"] = "application/json"
        return response
    response = make_response(jsonify(RESPUESTA["3"]), 403)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route("/profile", methods=["DELETE"])
def remove():
    print("Eliminando perfil mediante API")
    if deleteVisitor(request.json, request.remote_addr):
        response = make_response(jsonify(RESPUESTA["0"]), 200)
        response.headers["Content-Type"] = "application/json"
        return response
    response = make_response(jsonify(RESPUESTA["4"]), 403)
    response.headers["Content-Type"] = "application/json"
    return response

def connectionAPI():
    if __name__ == '__main__':
        app.run(debug=False, port=API_PORT, ssl_context="adhoc")

##########################################################
######################### SOCKET #########################
##########################################################

def handle_client(conn, addr):
    print(f"[NUEVA CONEXION] {addr} connected.")
    msg = conn.recv(HEADER).decode(FORMAT)
    if msg:
        print(f" He recibido del cliente [{addr}] el mensaje: {msg}")
        respuesta = {}
        msg = json.loads(msg)
        if msg["action"] == "create":
            print("Creando perfil de visitante...")
            # IPAddr = socket. gethostbyname(hostname
            if(createVisitor(msg, addr)):
                print("¡Hecho!")
                respuesta = RESPUESTA["0"]
            else:
                respuesta = RESPUESTA["2"]
        elif msg["action"] == "edit":
                print("Editando perfil de visitante...")
                if(editVisitor(msg, addr)):
                    print("¡Hecho!")
                    respuesta = RESPUESTA["0"]
                else:
                    respuesta = RESPUESTA["3"]
        elif msg["action"] == "delete":
            print("Borrando perfil de visitante...")
            if(deleteVisitor(msg, addr)):
                print("¡Hecho!")
                respuesta = RESPUESTA["0"]
            else:
                respuesta = RESPUESTA["4"]
        else:   
            print("Opción incorrecta")
            respuesta = RESPUESTA["1"]
        respuesta = json.dumps(respuesta)
        print("Enviando respuesta...")
        conn.send(respuesta.encode(FORMAT))
    print("Finalizando conexión con Registry.")
    conn.close()
        
def connectionSocket():
    print(f"[LISTENING] Servidor a la escucha en {SERVER}")
    while True:
        conn, addr = server.accept()
        CONEX_ACTIVAS = threading.active_count()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[CONEXIONES ACTIVAS] {CONEX_ACTIVAS}")
    
def start():
    server.listen()
    threadSocket = threading.Thread(target=connectionSocket)
    threadSocket.start()
    threadAPI = threading.Thread(target=connectionAPI)
    threadAPI.start()

#########################################################
######################### MAIN ##########################
#########################################################

if(len(sys.argv) == 3):
    API_PORT = int(sys.argv[2])
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    PORT = int(sys.argv[1])
    ADDR = (SERVER, PORT)
    print(ADDR)
    server.bind(ADDR)
    print("[STARTING] Servidor inicializándose...")
    start()

else:
    print ("Oops!. Parece que algo falló. Necesito estos argumentos: <Puerto_Escucha> <Puerto_Escucha_API>")
