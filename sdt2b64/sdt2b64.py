"""
Convert .sdt files to .b64 file that can be opened with SimFCS software.

To execute the script simply run this python code through IDE or by "python sdt2b64.py" in terminal/command prompt.
It will pop-up a window asking if a file or folder will be processed and then another window to select the file/folder to be processed.
After finishing convertion it will print "Finished converting". To process another file/folder, the script should be executed again. 

Author: Bruno Pannunzio. Advanced Bioimagenology Unit, Institut Pasteur de Montevideo (2023-2024)
"""

import numpy
import subprocess
import sys
packages = ['sdtfile','lfdfiles']
for package in packages:
	subprocess.check_call([sys.executable, '-m', 'pip','install', package])
from sdtfile import SdtFile
from lfdfiles import simfcsb64_write
import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'
import tkinter as tk
from tkinter import filedialog

class CustomDialog:
    def __init__(self, parent):
        self.parent = parent
        self.result = None
        self.create_widgets()

    def create_widgets(self):
        self.win = tk.Toplevel(self.parent)
        self.win.title('Select Option')
        message = "Do you want to process a file or a folder?"
        tk.Label(self.win, text=message).pack()

        tk.Button(self.win, text='File', command=self.process_file).pack()
        tk.Button(self.win, text='Folder', command=self.process_folder).pack()

    def process_file(self):
        self.result = 'file'
        self.win.destroy()

    def process_folder(self):
        self.result = 'folder'
        self.win.destroy()

def process_file(filename):
    print('Converting file: ', filename)
    with SdtFile(filename) as sdt:
        for i, data in enumerate(sdt.data):
            assert data.shape == (512, 512, 1024)
            data = numpy.moveaxis(data, -1, 0)
            # export to B64
            simfcsb64_write(filename + f'.{i}.B64', data.astype(numpy.int16))

def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".sdt"):
            file_path = os.path.join(folder_path, filename)
            process_file(file_path)

def select_file_or_folder():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Create a custom dialog
    dialog = CustomDialog(root)

    # Wait for the dialog to be closed
    root.wait_window(dialog.win)

    # Process based on user input
    if dialog.result and dialog.result.lower() == 'file':
        # Process a file
        file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("SDT files", "*.sdt")])
        if file_path:
            process_file(file_path)
    elif dialog.result and dialog.result.lower() == 'folder':
        # Process a folder
        folder_path = filedialog.askdirectory(title="Select a folder")
        if folder_path:
            process_folder(folder_path)
    print('Finished converting')

if __name__ == "__main__":
    select_file_or_folder()
