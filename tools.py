import tkinter as tk
from tkinter import filedialog

def selectFile():
    root = tk.Tk()
    root.withdraw()

    directory_path = filedialog.askopenfilename()
    return directory_path
