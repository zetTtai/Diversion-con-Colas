import os
import subprocess

pip_dir = os.path.expandvars(r'%LOCALAPPDATA%/Programs/Python/Python310/Scripts')
pip = os.path.join(pip_dir, 'pip3.exe')
subprocess.run([pip, 'install', '-r', 'requirements.txt'])
