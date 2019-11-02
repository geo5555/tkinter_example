from tkinter import *
from tkinter import ttk

root = Tk()
btn1 = ttk.Button(root, text="Hello George from ttk")
btn1.pack()
btn2 = ttk.Button(root, text="Hello 2 from ttk")
btn2.pack()
style = ttk.Style()
style.theme_use('vista')
#style.theme_names()
#('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
print(style.theme_use())
style.configure('TButton', foreground='blue')
#btn1.configure(style='MyStyle')
root.mainloop()
