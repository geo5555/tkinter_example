from tkinter import Button, Label, Entry, Tk, END, filedialog, scrolledtext
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
txtArea1.grid(column=0, row=5)
txtArea2 = scrolledtext.ScrolledText(window, width=50, height=80)
txtArea2.grid(column=1, row=5)
txtArea3 = scrolledtext.ScrolledText(window, width=50, height=80)
txtArea3.grid(column=2, row=5)


def openFileDialog():
    global directory1
    directory1 = filedialog.askdirectory()  # returns string
    txtArea1.delete("1.0", END)
    txtArea2.delete("1.0", END)
    txtArea3.delete("1.0", END)
    lbl.configure(text=directory1)
    for file in Path(directory1).iterdir():
        txtArea1.insert('end', file.name)
        txtArea1.insert('end', '\n')


def renamePreview():
    global directory1
    txtArea2.delete("1.0", END)
    pattern = txt1.get()
    pattern2 = txt2.get()
    result = ''
    for file in Path(directory1).iterdir():
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
        txtArea1.insert('end', file.name)
        txtArea1.insert('end', '\n')


btnFileDialog = Button(
    window, text="Select File Directory", command=openFileDialog)
btnRenamePreview = Button(
    window, text="Rename Files Preview", command=renamePreview)
btnRename = Button(
    window, text="Rename Files", command=rename)
btnRefresh = Button(
    window, text="Refresh Directory", command=refresh)
btnRefresh.grid(column=0, row=3)
btnFileDialog.grid(column=0, row=4)
btnRenamePreview.grid(column=1, row=4)
btnRename.grid(column=2, row=4)
window.mainloop()
