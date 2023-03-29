from pick import pick
import os
from pathlib import Path
from tkinter.filedialog import askopenfilenames

BASE_DIR = Path.home()

def ask_files():
    dialog = askopenfilenames(defaultextension="mp3", title="Select your files",initialdir=BASE_DIR)
    # print(list(dialog))
    return list(dialog)