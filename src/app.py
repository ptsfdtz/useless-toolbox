import tkinter as tk
from tkinter import ttk
from jpg_to_pdf import jpgToPdf
from speed_test import speedTest
from drawing import drawing
from send_message import sendMessage
from sign_in import signIn
class Module:
    def __init__(self, name, function, *args, **kwargs):
        self.name = name
        self.function = function
        self.args = args
        self.kwargs = kwargs

class ToolBoxUI:
    def __init__(self, window, modules):
        self.window = window
        self.modules = modules
        self.create_ui()

    def create_ui(self):
        self.window.configure(bg='#f0f0f0')  # Set background color

        canvas = tk.Canvas(self.window, width=800, height=400, bg='#f0f0f0')
        canvas.pack()

        title_label = ttk.Label(self.window, text="选择你需要使用的工具", font=("Helvetica", 20, "bold"), background='#f0f0f0')
        title_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        frame = tk.Frame(self.window, bg='#f0f0f0')  
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.create_buttons(frame)

    def create_buttons(self, frame):
        buttons_per_row = 3  # Number of buttons per row
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
            self.window.destroy()
            module_info.function(*module_info.args, **module_info.kwargs)
        except Exception as e:
            print(f"Error running module {module_info.name}: {e}")

class ToolBox:
    def __init__(self, title, modules):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry("800x400")
        self.ui = ToolBoxUI(self.window, modules)

    def run(self):
        self.window.mainloop()

if __name__ == '__main__':
    modules = [
        Module("图片转PDF", jpgToPdf.main),
        Module("网速测试", speedTest.main),
        Module("随机抽签", drawing.main),
        Module("发送邮件", sendMessage.main),
        Module("签到", signIn.main),
        # Add more modules in the future
    ]

    toolbox = ToolBox("欢迎来到秃子的工具箱", modules)
    toolbox.run()
