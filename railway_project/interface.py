import tkinter as tk
from tkinter import font
import re
from constants import *
from auth import Authorization
# from loading_screen import ImageLabel

root = tk.Tk()
root.geometry(SCREEN_SIZE)
root.configure(background=BACKGROUND)
root.resizable(width=False, height=False)
# lbl = ImageLabel(root)
# lbl.pack()
# lbl.load('map-icon-train-station.gif')
# try:
#     lbl.destroy()
# except:
#     pass

Authorization(root)
root.mainloop()



