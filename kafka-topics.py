import subprocess
import os

Target_dir     = "C:/kafka"
Default_Topics = ["visitantes", "mapa", "sensores"]

def CreateAllTopics():
    Command    = [Target_dir + "/bin/windows/kafka-topics.bat", "--create", "--zookeeper", "localhost:2181", "--replication-factor", "1", "--partitions", "1", "--topic"]
    os.chdir(Target_dir)
    for topic in Default_Topics:
        Command.append(topic)
        subprocess.run(Command)
        Command.pop()

def ListAllTopics():
    Command = [Target_dir + "/bin/windows/kafka-topics.bat", "--list", "--zookeeper", "localhost:2181"]
    os.chdir(Target_dir)
    subprocess.run(Command)

def CreateTopic():
    Command    = [Target_dir + "/bin/windows/kafka-topics.bat", "--create", "--zookeeper", "localhost:2181", "--replication-factor", "1", "--partitions", "1", "--topic"]
    os.chdir(Target_dir)
    print("Introduce el nombre del topic: ", end='')
    string = input()
    if not string.isalnum():
        exit(0)
    Command.append(string)
    subprocess.run(Command)
    
def ListMessagesFromTopic():
    Command = [Target_dir + "/bin/windows/kafka-console-consumer.bat", "--bootstrap-server", "localhost:9092", "--topic"]
    os.chdir(Target_dir)
    print("Introduce el nombre del topic: ", end='')
    string = input()
    if not string.isalnum():
        exit(0)
    Command.append(string)
    Command.append("--from-beginning")
    subprocess.run(Command)

def main():
    input = menu()
    if input == 1:
        CreateAllTopics()
    elif input == 2:
        ListAllTopics()
    elif input == 3:
        CreateTopic()
    elif input == 4:
        ListMessagesFromTopic()
    elif input == 5:
        os.system('cls')
    else:
        exit(0)

def menu() -> int:
    print("Introduce el número correspondiente a la acción que desea realizar")
    print("1 - Crea todos los topics necesarios de la aplicación")
    print("2 - Lista todos los topics actuales")
    print("3 - Crea un topic manualmente")
    print("4 - Ver mensajes de un topic concreto")
    print("5 - Limpia la consola")
    print("Otro valor - Salir del programa")
    print("Input:", end='')
    inp = input()
    if inp.isnumeric():
        return int(inp)
    else:
        exit(0)

if __name__ == "__main__":
    os.system('cls')
    while True:
        main()