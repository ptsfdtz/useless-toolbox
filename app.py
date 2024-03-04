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

        for idx, module_info in enumerate(self.modules, start=1):
            button = Button(self.window, text=f"{idx}. {module_info['name']}", command=lambda mod=module_info: mod['function'](), font=("Helvetica", 14))
            button.pack(pady=10)

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

# select = int(input("请选择你要执行的功能：\n1.JPG转PDF\n2.网速测试\n"))
# if select == 1:
#     jpgToPdf.main()
#     print("JPG转PDF已执行")
# elif select == 2:
#     speedTest.main()
#     print("网速测试已执行")