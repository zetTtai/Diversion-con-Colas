import sys
import time
from kafka import KafkaProducer #pip install kafka-python

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
XSEC= 3
FIN = "FIN"
    
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
            
            # TODO: Cómo obtener el número de personas en la ID_Atracción? => Te lo inventas

            print(f'SENSOR[{ID}]: Seleccione opción:')
            print("1. Escribe '+' para aumentar en 10 el número de visitantes.")
            print("2. Escribe '-' para aumentar en 10 el número de visitantes.")
            print("3. ")

            producer = KafkaProducer(bootstrap_servers=f'{SERVER}:{PORT}')
            
            print('Finalizando conexión...')
            start = time.time() # Reseteamos el timer
else:
    print ("Oops!. Parece que algo falló. Necesito estos argumentos: <ServerIP_FAKFA> <Puerto_FAKFA> <ID_Atracción>")
