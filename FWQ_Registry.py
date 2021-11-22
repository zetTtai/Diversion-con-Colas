import socket 
import threading
import sys
import sqlite3
import traceback
import json
#API
from flask import Flask, make_response, request, jsonify

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

app = Flask(__name__)
######################### API #########################

@app.route("/profile", methods=["POST"])
def create():
    print("Creando perfil mediante API")
    if createVisitor(request.json):
        response = make_response(jsonify(RESPUESTA["0"]), 200)
        response.headers["Content-Type"] = "application/json"
        return response
    response = make_response(jsonify(RESPUESTA["2"]), 403)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route("/profile", methods=["PUT"])
def update():
    print("Actualizando perfil mediante API")
    if editVisitor(request.json):
        response = make_response(jsonify(RESPUESTA["0"]), 200)
        response.headers["Content-Type"] = "application/json"
        return response
    response = make_response(jsonify(RESPUESTA["3"]), 403)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route("/profile", methods=["DELETE"])
def remove():
    print("Eliminando perfil mediante API")
    if deleteVisitor(request.json):
        response = make_response(jsonify(RESPUESTA["0"]), 200)
        response.headers["Content-Type"] = "application/json"
        return response
    response = make_response(jsonify(RESPUESTA["4"]), 403)
    response.headers["Content-Type"] = "application/json"
    return response

def connectionAPI():
    if __name__ == '__main__':
        app.run(debug=False, port=API_PORT)

######################### SOCKET #########################

def deleteVisitor(msg):
    conn = sqlite3.connect('db/database.db')
    print(f"Establecida conexión con la base de datos")
    cursor = conn.cursor()
    # TODO: Encriptar password
    visitante= (msg["id"], msg["password"])
    try:
        # Buscamos si ya existe ese perfil y que la contraseña sea la correcta TODO: Falta encriptar
        cursor.execute(f'SELECT * FROM visitantes WHERE id = "{msg["id"]}" AND password = "{msg["password"]}"')
        rows = cursor.fetchall()
        if rows:
            cursor.execute('DELETE FROM visitantes WHERE id = ? AND password = ?', visitante)
            conn.commit()
        else:
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
    conn.close()
    return True

def createVisitor(msg):
    conn = sqlite3.connect('db/database.db')
    print(f"Establecida conexión con la base de datos")
    cursor = conn.cursor()
    # TODO: Encriptar password
    visitante= (msg["id"], msg["name"], msg["password"])
    try:
        # Buscamos si ya existe ese perfil
        cursor.execute(f'SELECT * FROM visitantes WHERE id = "{msg["id"]}"')
        rows = cursor.fetchall()
        if rows:
            conn.close()
            return False
        else:
            cursor.execute('INSERT INTO visitantes(id, name, password) VALUES(?, ?, ?)', visitante)
            conn.commit()
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

def editVisitor(msg): 
    conn = sqlite3.connect('db/database.db')
    print(f"Establecida conexión con la base de datos")
    cursor = conn.cursor()
    # ID no se puede cambiar
    try:
        cursor.execute('UPDATE visitantes SET name = ?, password = ? WHERE id = ?', (msg["name"], msg["password"], msg["id"]))
        conn.commit()
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

def handle_client(conn, addr):
    print(f"[NUEVA CONEXION] {addr} connected.")
    msg = conn.recv(HEADER).decode(FORMAT)
    if msg:
        print(f" He recibido del cliente [{addr}] el mensaje: {msg}")
        respuesta = {}
        msg = json.loads(msg)
        if msg["action"] == "create":
            print("Creando perfil de visitante...")
            if(createVisitor(msg)):
                print("¡Hecho!")
                respuesta = RESPUESTA["0"]
            else:
                respuesta = RESPUESTA["2"]
        elif msg["action"] == "edit":
                print("Editando perfil de visitante...")
                if(editVisitor(msg)):
                    print("¡Hecho!")
                    respuesta = RESPUESTA["0"]
                else:
                    respuesta = RESPUESTA["3"]
        elif msg["action"] == "delete":
            print("Borrando perfil de visitante...")
            if(editVisitor(msg)):
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

######################### MAIN ##########################

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
