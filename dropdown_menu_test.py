import tkinter as tk
from api_tool import ApiTool

root = tk.Tk()
root.geometry('500x500')
root.title("main window")

api_tool = ApiTool(root=root)

root.mainloop()