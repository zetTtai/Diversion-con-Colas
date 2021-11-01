import os
import zipfile
import shutil

Target_dir = "C:/kafka"


def main():
    Directory()
    Unzip()

def Directory():
    if os.path.isdir(Target_dir):
        shutil.rmtree(Target_dir)
    os.mkdir(Target_dir)

def Unzip():
    with zipfile.ZipFile("kafka.zip","r") as zip_ref:
        zip_ref.extractall(Target_dir)

if __name__ == "__main__":
    main()
