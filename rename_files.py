from tkinter import *
import tkinter.scrolledtext as tkst
from tkinter import filedialog
from pathlib import Path
import re

window = Tk()
frame1 = Frame(window)
window.title("Rename Files by GE")
# window.geometry('1200x600')

Label(frame1, text="From").grid(row=1, column=0)
Label(frame1, text="To").grid(row=1, column=2)
txt1 = Entry(frame1, width=20)
txt1.grid(column=1, row=1)
txt2 = Entry(frame1, width=20)
txt2.grid(column=4, row=1)
frame1.grid(column=0, row=1)
directory1 = ''
listPreview = []
listFiles = []
txtArea1 = tkst.ScrolledText(window, width=50, height=30)
txtArea1.grid(column=0, row=5)
txtArea2 = tkst.ScrolledText(window, width=50, height=30)
txtArea2.grid(column=1, row=5)
txtArea3 = tkst.ScrolledText(window, width=50, height=30)
txtArea3.grid(column=2, row=5)
frame2 = Frame(window)
frame2.grid(column=0, row=4)
lbl = Label(frame2, text="", font=("Arial Bold", 12))
lbl.grid(column=1, row=0)


def openFileDialog():
    global directory1
    global recursive
    directory1 = filedialog.askdirectory()  # returns string
    txtArea1.delete("1.0", END)
    txtArea2.delete("1.0", END)
    txtArea3.delete("1.0", END)
    lbl.configure(text=directory1)
    for file in Path(directory1).iterdir():
        if file.is_file():
            txtArea1.insert('end', file.name)
            txtArea1.insert('end', '\n')


def renamePreview():
    global directory1
    txtArea2.delete("1.0", END)
    pattern = txt1.get()
    pattern2 = txt2.get()
    result = ''
    for file in Path(directory1).iterdir():
        if file.is_file():
            if re.search(pattern, file.name, flags=re.I):
                result = re.sub(pattern, pattern2,
                                file.name, flags=re.I)
                txtArea2.insert('end', result)
                txtArea2.insert('end', '\n')


def rename():
    global directory1
    txtArea3.delete("1.0", END)
    pattern = re.escape(txt1.get())
    pattern2 = re.escape(txt2.get())
    result = ''
    for file in Path(directory1).iterdir():
        if file.is_file():
            if re.search(pattern, file.name, flags=re.I):
                result = re.sub(pattern, pattern2,
                                file.name, flags=re.I)
                file.rename(file.parent.joinpath(result))
                txtArea3.insert('end', result)
                txtArea3.insert('end', '\n')


def refresh():
    global directory1
    txtArea1.delete("1.0", END)
    txtArea2.delete("1.0", END)
    txtArea3.delete("1.0", END)
    for file in Path(directory1).iterdir():
        if file.is_file():
            txtArea1.insert('end', file.name)
            txtArea1.insert('end', '\n')


btnFileDialog = Button(
    frame2, text="Select File Directory", command=openFileDialog)
btnRenamePreview = Button(
    window, text="Rename Files Preview", command=renamePreview)
btnRename = Button(
    window, text="Rename Files", command=rename)
btnRefresh = Button(
    window, text="Refresh Directory", command=refresh)
btnRefresh.grid(column=0, row=3)

#frame2.grid(column=0, row=4)
btnFileDialog.grid(column=0, row=0)
#lbl=Label(frame2, text="Directory:", font=("Arial Bold", 12)).grid(column=1, row=0)
btnRenamePreview.grid(column=1, row=4)
btnRename.grid(column=2, row=4)
window.mainloop()
