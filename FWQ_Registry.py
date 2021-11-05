import socket 
import threading
import sys
import sqlite3
import traceback
import json

HEADER = 2048
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
FIN = "FIN"

RESPUESTA = {
    "0": {
        "status" : "0",
        "message" : "OK"
    },

    "1": {
        "status" : "1",
        "message" : "Opción es incorrecta [create | edit]"
    },

    "2": {
        "status" : "2",
        "message" : "Fallo al crear el perfil"
    }, 

    "3": {
        "status" : "3",
        "message" : "Fallo al editar el perfil"
    }
}

def createVisitor(msg):
    conn = sqlite3.connect('db/database.db')
    print(f"Establecida conexión con la base de datos")
    cursor = conn.cursor()
    visitante= (msg["alias"], msg["name"], msg["password"])
    # TODO: Comprobar si salta excepción al crear un visitante con una id existente
    try:
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
        cursor.execute('UPDATE visitantes SET name = ?, password = ? WHERE"where id = ?', (msg["name"], msg["password"], msg["alias"]))
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
        else:   
            print("Opción incorrecta")
            respuesta = RESPUESTA["1"]

        respuesta = json.dumps(respuesta)
        print("Enviando respuesta...")
        conn.send(respuesta.encode(FORMAT))
    print("Finalizando conexión con Registry.")
    conn.close()
        
def start():
    server.listen()
    print(f"[LISTENING] Servidor a la escucha en {SERVER}")
    while True:
        conn, addr = server.accept()
        CONEX_ACTIVAS = threading.active_count()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[CONEXIONES ACTIVAS] {CONEX_ACTIVAS}")
        

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
