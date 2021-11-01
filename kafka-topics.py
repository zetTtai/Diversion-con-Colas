import subprocess
import os

Target_dir    = "C:/kafka"
Topic_Args    = [Target_dir + "/bin/windows/kafka-topics.bat", "--create", "--zookeeper", "localhost:2181", "--replication-factor", "1", "--partitions", "1", "--topic"]
Topics        = ["visitantes", "mapa", "sensores"]

def main():
    os.chdir(Target_dir)
    for topic in Topics:
        Topic_Args.append(topic)
        subprocess.run(Topic_Args)
        Topic_Args.pop()

if __name__ == "__main__":
    main()