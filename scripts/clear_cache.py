# This file is part of the Prodeimat project
# @Author: Ricel Quispe

import shutil
import os

def clear_pycache(root_dir):
    if root_dir == '/':
        print("Operation not allowed on root directory")
        return
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if '__pycache__' in dirnames:
            shutil.rmtree(os.path.join(dirpath, '__pycache__'))
            print(f"Removed __pycache__ from {dirpath}")


clear_pycache('app/')
