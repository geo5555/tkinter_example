from tkinter import *
import tkinter.scrolledtext as tkst
from tkinter import filedialog
from pathlib import Path
import re

window = Tk()
frame1 = Frame(window)
window.title("Rename Files by GE")
# window.geometry('1200x600')

var_recButton = IntVar()
recButton = Checkbutton(frame1, variable=var_recButton, text="Recursive")
recButton.grid(row=1, column=5)

var_escButton = IntVar()
escButton = Checkbutton(frame1, variable=var_escButton,
                        text="Escape Special Characters")
escButton.grid(row=1, column=6)

var_fullButton = IntVar()
escButton = Checkbutton(frame1, variable=var_fullButton,
                        text="Show Full Path")
escButton.grid(row=1, column=7)

Label(frame1, text="From").grid(row=1, column=0)
Label(frame1, text="To").grid(row=1, column=2)
txt1 = Entry(frame1, width=20)
txt1.grid(column=1, row=1)
txt2 = Entry(frame1, width=20)
txt2.grid(column=4, row=1)
frame1.grid(column=0, row=1, columnspan=3)
directory1 = ''
listPreview = []
listFiles = []
txtArea1 = tkst.ScrolledText(window, width=50, height=30)
txtArea1.grid(column=0, row=6)
txtArea2 = tkst.ScrolledText(window, width=50, height=30)
txtArea2.grid(column=1, row=6)
txtArea3 = tkst.ScrolledText(window, width=50, height=30)
txtArea3.grid(column=2, row=6)
frame2 = Frame(window)
frame2.grid(column=0, row=4)
lblDirectory = Label(frame2, text="", font=("Arial Bold", 12))
lblDirectory.grid(column=1, row=0)
lblCountFiles = Label(window, text="#", font=("Arial Bold", 12))
lblCountFiles.grid(column=0, row=5)
lblCountPreview = Label(window, text="#", font=("Arial Bold", 12))
lblCountPreview.grid(column=1, row=5)
lblCountRenamed = Label(window, text="#", font=("Arial Bold", 12))
lblCountRenamed.grid(column=2, row=5)
listFiles = []


def openFileDialog():
    global directory1
    global recursive
    directory1 = filedialog.askdirectory()  # returns string
    lblDirectory.configure(text=directory1)
    populateTextArea1()


def populateTextArea1():
    global listFiles
    global directory1
    recursive = var_recButton.get()
    full_path = var_fullButton.get()
    txtArea1.delete("1.0", END)
    txtArea2.delete("1.0", END)
    txtArea3.delete("1.0", END)
    lblCountPreview.configure(text="#")
    lblCountRenamed.configure(text="#")
    if not recursive:
        listFiles = [file for file in Path(
            directory1).iterdir() if file.is_file()]
    else:
        listFiles = [file for file in Path(
            directory1).glob("**/*") if file.is_file()]
    for file in listFiles:
        if full_path:
            txtArea1.insert('end', file)
        else:
            txtArea1.insert('end', file.name)
        txtArea1.insert('end', '\n')
    countFiles = len(listFiles)
    lblCountFiles.configure(text=str(countFiles))


def renamePreview():
    global directory1
    global listFiles
    txtArea2.delete("1.0", END)
    escape = var_escButton.get()
    if escape:
        pattern = re.escape(txt1.get())
    else:
        pattern = txt1.get()
    pattern2 = txt2.get()
    result = ''
    countPreview = 0
    for file in listFiles:
        if re.search(pattern, file.name, flags=re.I):
            countPreview += 1
            result = re.sub(pattern, pattern2,
                            file.name, flags=re.I)
            txtArea2.insert('end', result)
            txtArea2.insert('end', '\n')
    lblCountPreview.configure(text=str(countPreview))


def rename():
    global directory1
    global listFiles
    txtArea3.delete("1.0", END)
    escape = var_escButton.get()
    if escape:
        pattern = re.escape(txt1.get())
    else:
        pattern = txt1.get()
    pattern = re.escape(txt1.get())
    pattern2 = txt2.get()
    result = ''
    countRenamed = 0
    for file in listFiles:
        if re.search(pattern, file.name, flags=re.I):
            result = re.sub(pattern, pattern2,
                            file.name, flags=re.I)
            print(file.parent.joinpath(result))
            file.rename(file.parent.joinpath(result))
            countRenamed += 1
            # file.rename(result) will move file to another dir
            txtArea3.insert('end', result)
            txtArea3.insert('end', '\n')
    lblCountRenamed.configure(text=str(countRenamed))


def refresh():
    populateTextArea1()


btnFileDialog = Button(
    frame2, text="Select File Directory", command=openFileDialog)
btnRenamePreview = Button(
    window, text="Rename Files Preview", command=renamePreview)
btnRename = Button(
    window, text="Rename Files", command=rename)
btnRefresh = Button(
    window, text="Refresh Directory", command=refresh)
btnRefresh.grid(column=0, row=3)


btnFileDialog.grid(column=0, row=0)
btnRenamePreview.grid(column=1, row=4)
btnRename.grid(column=2, row=4)
window.mainloop()
