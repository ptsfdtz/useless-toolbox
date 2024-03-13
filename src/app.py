import tkinter as tk
from tkinter import ttk
from jpg_to_pdf import jpgToPdf
from drawing import drawing
from send_message import sendMessage
from sign_in import signIn
import logging

class Module:
    def __init__(self, name, function, *args, **kwargs):
        self.name = name
        self.function = function
        self.args = args
        self.kwargs = kwargs

class ToolBoxUI:
    def __init__(self, root, modules):
        self.root = root
        self.modules = modules
        self.create_ui()

    def create_ui(self):
        self.root.configure(bg='#f0f0f0') 

        canvas = tk.Canvas(self.root, width=400, height=400, bg='#f0f0f0')
        canvas.pack()

        title_label = ttk.Label(self.root, text="选择你需要使用的工具", font=("Helvetica", 20, "bold"), background='#f0f0f0')
        title_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        frame = tk.Frame(self.root, bg='#f0f0f0')  
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.create_buttons(frame)

    def create_buttons(self, frame):
        buttons_per_row = 4  #定义每一行显示几个按钮
        row = 0
        col = 0

        for idx, module_info in enumerate(self.modules, start=1):
            button = ttk.Button(frame, text=f"{idx}. {module_info.name}", command=lambda mod=module_info: self.run_module(mod), style='Toolbutton.TButton', width=20)
            button.grid(row=row, column=col, padx=10, pady=10)

            col += 1
            if col == buttons_per_row:
                col = 0
                row += 1

    def run_module(self, module_info):
        try:
            module_info.function(*module_info.args, **module_info.kwargs)
        except Exception as e:
            print(f"Error running module {module_info.name}: {e}")

class ToolBox:
    def __init__(self, title, modules):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("800x400")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x_position = int((screen_width - 800) / 2)
        y_position = int((screen_height - 400) / 2)

        self.root.geometry(f"800x400+{x_position}+{y_position}")

        self.ui = ToolBoxUI(self.root, modules)

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    modules = [
        Module("图片转PDF", jpgToPdf.main),
        Module("随机抽签", drawing.main),
        Module("发送邮件", sendMessage.main),
        Module("签到", signIn.main),
    ]

    toolbox = ToolBox("欢迎来到秃子的工具箱", modules)
    toolbox.run()