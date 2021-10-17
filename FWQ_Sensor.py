import sys
import time
from kafka import KafkaConsumer #pip install kafka-python

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
            
            # TODO: Cómo obtener el número de personas en la ID_Atracción?

            consumer = KafkaConsumer('sensor')
            for message in consumer:
                # TODO: Enviar el número de personas que se encuentran en la atracción correspondiente a ID
                print(message)
            print('Finalizando conexión...')
            start = time.time() # Reseteamos el timer
else:
    print ("Oops!. Parece que algo falló. Necesito estos argumentos: <ServerIP_FAKFA> <Puerto_FAKFA> <ID_Atracción>")
