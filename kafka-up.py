import subprocess
import os

Target_dir = "C:/kafka"
Kafka_Command_Path      = Target_dir + "/bin/windows/kafka-server-start.bat"
Kafka_Config_File       = Target_dir + "/config/server.properties"

def main():
    os.chdir(Target_dir)
    subprocess.run([Kafka_Command_Path, Kafka_Config_File])

if __name__ == "__main__":
    main()