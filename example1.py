from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
import collections
from pathlib import Path
import re

window = Tk()
window.title("Rename Files by GE")
lbl = Label(window, text="Directory:", font=("Arial Bold", 12))
lbl.grid(column=0, row=0)
window.geometry('1200x600')
txt1 = Entry(window, width=20)
txt1.insert(0, "From")
txt1.grid(column=0, row=1)
txt2 = Entry(window, width=20)
txt2.insert(0, "To")
txt2.grid(column=0, row=2)
directory1 = ''
listPreview = []
listFiles = []
txtArea1 = scrolledtext.ScrolledText(window, width=50, height=80)
txtArea1.grid(column=0, row=4)
txtArea2 = scrolledtext.ScrolledText(window, width=50, height=80)
txtArea2.grid(column=1, row=4)
txtArea3 = scrolledtext.ScrolledText(window, width=50, height=80)
txtArea3.grid(column=2, row=4)


def openFileDialog():
    global directory1
    directory1 = filedialog.askdirectory()  # returns string
    txtArea1.delete("1.0", END)
    lbl.configure(text=directory1)
    listFiles = [p.name for p in Path(directory1).iterdir()]
    for file in listFiles:
        txtArea1.insert('end', file)
        txtArea1.insert('end', '\n')


def renamePreview():
    global directory1
    txtArea2.delete("1.0", END)
    pattern = txt1.get()
    pattern2 = txt2.get()
    result = ''
    listPreview = []
    for file in [p.name for p in Path(directory1).iterdir()]:
        if re.search(pattern, file, flags=re.I):
            result = re.sub(pattern, pattern2,
                            file, flags=re.I)
            listPreview.append(result)
    for file in listPreview:
        txtArea2.insert('end', file)
        txtArea2.insert('end', '\n')


def rename():
    global directory1
    txtArea3.delete("1.0", END)
    pattern = txt1.get()
    pattern2 = txt2.get()
    listOutput = []
    result = ''
    for file in [p for p in Path(directory1).iterdir()]:
        if re.search(pattern, file.name, flags=re.I):
            result = re.sub(pattern, pattern2,
                            file.name, flags=re.I)
            listOutput.append(result)
            # file.rename(result)
    for file in listOutput:
        txtArea3.insert('end', file)
        txtArea3.insert('end', '\n')


btnFileDialog = Button(
    window, text="Select File Directory", command=openFileDialog)
btnRenamePreview = Button(
    window, text="Rename Files Preview", command=renamePreview)
btnRename = Button(
    window, text="Rename Files", command=rename)
btnFileDialog.grid(column=0, row=3)
btnRenamePreview.grid(column=1, row=3)
btnRename.grid(column=2, row=3)
window.mainloop()
