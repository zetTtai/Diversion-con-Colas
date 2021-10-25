import socket 
import threading
import sys
import sqlite3
import traceback

HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
FIN = "FIN"
# MAX_CONEXIONES = 5

def createVisitor(msg):
    conn = sqlite3.connect('db/database.db')
    print(f"Establecida conexión con la base de datos")
    cursor = conn.cursor()
    visitante= (msg[1], msg[2], msg[3], 0) # Posicion inicial de todos los visitantes y '0' para indicar que todavía no está dentro del parque
    # TODO: Comprobar si salta excepción al crear un visitante con una id existente
    try:
        cursor.execute('INSERT INTO visitante(id, name, password, position) VALUES(?, ?, ?, ?)', visitante)
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
    if(msg[2] != "-"): # Actualizar nombre
        try:
            cursor.execute(f'UPDATE visitantes SET name = "{msg[2]}" where id = {msg[1]}')
            conn.commit()
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            conn.close()
            return False

    if(msg[3] != "-"): # Actualizar contraseña
        try:
            cursor.execute(f'UPDATE visitantes SET password = "{msg[3]}" where id = {msg[1]}')
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
    while True:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f" He recibido del cliente [{addr}] el mensaje: {msg}")
            
            msg = msg.split(" ")
            if(msg.len() == 4):
                if(msg[0] == "create"): # msg= "create ID/Alias Nombre Password"
                    print("Creando perfil de visitante...")
                    if(createVisitor(msg)):
                        print("¡Hecho!") 
                        conn.send("Perfil creado correctamente".encode(FORMAT))
                    else:
                        conn.send("No se ha podido crear el perfil, pruebe con otro ID/Alias".encode(FORMAT))
                elif(msg[0] == "edit"): # msg= "edit ID/Alias Nombre Password"
                    print("Editando perfil de visitante...")
                    if(editVisitor(msg)):
                        print("¡Hecho!")
                        conn.send("Perfil editado correctamente".encode(FORMAT))
                    else:
                        conn.send("No se ha podido editar el perfil.".encode(FORMAT))
                else:
                    conn.send(f"ERROR: La opción '{msg[0]}' no es válida.\nOPCIONES: [create | edit]".encode(FORMAT))
            else:
                conn.send(f"ERROR: Formato del mensaje incorrecto.\n[OPCION(create/edit)] [ID/ALIAS] [NOMBRE] [PASSWORD]".encode(FORMAT))
            break;
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

