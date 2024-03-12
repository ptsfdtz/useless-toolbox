import tkinter as tk
from tkinter import ttk
from jpg_to_pdf import jpgToPdf
from speed_test import speedTest
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
    def __init__(self, modules):
        self.modules = modules
        self.root = tk.Tk()
        self.root.title('欢迎来到秃子的工具箱')
        self.root.geometry('800x400')
        self.create_ui()

    def create_ui(self):
        title_label = ttk.Label(self.root, text="选择你需要使用的工具", font=("Helvetica", 20, "bold"))
        title_label.pack(pady=20)

        frame = ttk.Frame(self.root)
        frame.pack(expand=True, fill=tk.BOTH)

        self.create_buttons(frame)

    def create_buttons(self, frame):
        buttons_per_row = 3  # Number of buttons per row
        row = 0
        col = 0

        for idx, module_info in enumerate(self.modules, start=1):
            button = ttk.Button(frame, text=f"{idx}. {module_info.name}", command=lambda mod=module_info: self.run_module(mod), width=20)
            button.grid(row=row, column=col, padx=10, pady=10)

            col += 1
            if col == buttons_per_row:
                col = 0
                row += 1

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(row, weight=1)


    def run_module(self, module_info):
        try:
            module_info.function(*module_info.args, **module_info.kwargs)
        except Exception as e:
            logging.exception(f"Error running module {module_info.name}: {e}")

    def run(self):
        self.root.mainloop()

def main():
    modules = [
        Module("图片转PDF", jpgToPdf.main),
        Module("网速测试", speedTest.main),
        Module("随机抽签", drawing.main),
        Module("发送邮件", sendMessage.main),
        Module("签到", signIn.main),
        # Add more modules in the future
    ]

    toolbox_ui = ToolBoxUI(modules)
    toolbox_ui.run()

if __name__ == '__main__':
    main()
