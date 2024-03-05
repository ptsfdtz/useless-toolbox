import tkinter as tk
from tkinter import Button, Label
from jpg_to_pdf import jpgToPdf
from speed_test import speedTest  

class ToolBox:
    def __init__(self, title, modules):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry("800x400")
        self.window.configure(bg='gray')  # Set background color to gray

        self.modules = modules
        self.create_ui()

    def create_ui(self):
        label = Label(self.window, text="请选择一个执行:", font=("Helvetica", 16), bg='gray')  # Set label background color
        label.pack(pady=20)

        frame = tk.Frame(self.window, bg='gray')  # Create a frame to contain the buttons
        frame.pack()

        for idx, module_info in enumerate(self.modules, start=1):
            button = Button(frame, text=f"{idx}. {module_info['name']}", command=lambda mod=module_info: self.run_module(mod), font=("Helvetica", 14), width=15)
            button.pack(side=tk.LEFT, padx=10, pady=10)  # Use pack inside the frame


    def run_module(self, module_info):
        self.window.destroy()  # Close the main window
        module_info['function']()

    def run(self):
        self.window.mainloop()

if __name__ == '__main__':
    modules = [
        {"name": "JPG转PDF", "function": jpgToPdf.main},
        {"name": "网速测试", "function": speedTest.main},
        # Add more modules in the future
    ]

    toolbox = ToolBox("欢迎来到秃子的工具箱", modules)
    toolbox.run()
