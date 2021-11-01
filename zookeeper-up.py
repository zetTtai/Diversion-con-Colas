import subprocess
import os

Target_dir = "C:/kafka"
Zookeeper_Command_Path  = Target_dir + "/bin/windows/zookeeper-server-start.bat"
Zookeeper_Config_File   = Target_dir + "/config/zookeeper.properties"

def main():
    os.chdir(Target_dir)
    subprocess.run([Zookeeper_Command_Path, Zookeeper_Config_File])

if __name__ == "__main__":
    main()