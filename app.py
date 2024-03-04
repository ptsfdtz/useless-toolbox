import tkinter as tk
from tkinter import Button, Label
from jpg_to_pdf import jpgToPdf
from speed_test import speedTest 
class ToolBox:
    def __init__(self, title, modules):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry("800x400")

        self.modules = modules
        self.create_ui()

    def create_ui(self):
        label = Label(self.window, text="请选择一个执行:", font=("Helvetica", 16))
        label.pack(pady=20)

        for idx, module in enumerate(self.modules, start=1):
            button = Button(self.window, text=f"{idx}. {module['name']}", command=lambda mod=module: mod['function'](), font=("Helvetica", 14))
            button.pack(pady=10)

    def run(self):
        self.window.mainloop()

if __name__ == '__main__':
    modules = [
        {"name": "JPG转PDF", "function": jpgToPdf},
        {"name": "网速测试", "function": speedTest},
        # Add more modules in the future
    ]

    toolbox = ToolBox("欢迎来到秃子的工具箱", modules)
    toolbox.run()
