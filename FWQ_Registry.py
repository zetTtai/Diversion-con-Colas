import socket 
import threading
import sys
import sqlite3
import traceback
import json

HEADER = 64
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
    visitante= (msg["alias"], msg["nombre"], msg["password"])
    # TODO: Comprobar si salta excepción al crear un visitante con una id existente
    try:
        cursor.execute('INSERT INTO visitante(id, name, password) VALUES(?, ?, ?)', visitante)
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
    # Los atributos que no se editan se declaran como "-" en el mensaje
    if msg["nombre"] != "-": # Actualizar nombre
        try:
            cursor.execute(f'UPDATE visitantes SET name = "{msg["nombre"]}" where id = {msg["id"]}')
            conn.commit()
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            conn.close()
            return False

    if msg["password"] != "-": # Actualizar contraseña
        try:
            cursor.execute(f'UPDATE visitantes SET password = "{msg["password"]}" where id = {msg["id"]}')
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
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        # msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
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
        #     conn.send(f"ERROR: Formato del mensaje incorrecto.\n[OPCION(create/edit)] [ID/ALIAS] [NOMBRE] [PASSWORD]".encode(FORMAT))
    print("Finalizando conexión con Registry.")
    conn.close()
        
def start():
    server.listen()
    print(f"[LISTENING] Servidor a la escucha en {SERVER}")
    while True:
        conn, addr = server.accept()
        CONEX_ACTIVAS = threading.active_count()
        # if (CONEX_ACTIVAS <= MAX_CONEXIONES): 
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[CONEXIONES ACTIVAS] {CONEX_ACTIVAS}")
        # else:
        #     print("OOppsss... DEMASIADAS CONEXIONES. ESPERANDO A QUE ALGUIEN SE VAYA")
        #     conn.send("OOppsss... DEMASIADAS CONEXIONES. Tendrás que esperar a que alguien se vaya".encode(FORMAT))
        #     conn.close()
        #     CONEX_ACTUALES = threading.active_count()-1
        

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

