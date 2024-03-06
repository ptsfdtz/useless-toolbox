import tkinter as tk
from tkinter import ttk, PhotoImage
from jpg_to_pdf import jpgToPdf
from speed_test import speedTest
from drawing import drawing

class Module:
    def __init__(self, name, function, *args, **kwargs):
        self.name = name
        self.function = function
        self.args = args
        self.kwargs = kwargs

class ToolBox:
    def __init__(self, title, modules):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry("800x400")
        self.modules = modules
        self.create_ui()

    def create_ui(self):
        canvas = tk.Canvas(self.window, width=800, height=400)
        canvas.pack()

        # # Load the background image
        # bg_image = PhotoImage(file="src/background_image.png")  # Provide the correct path
        # canvas.create_image(0, 0, anchor=tk.NW, image=bg_image)

        title_label = ttk.Label(self.window, text="选择你需要使用的工具", font=("Helvetica", 20, "bold"))
        title_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        frame = tk.Frame(self.window)  
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        for idx, module_info in enumerate(self.modules, start=1):
            button = ttk.Button(frame, text=f"{idx}. {module_info.name}", command=lambda mod=module_info: self.run_module(mod), style='Toolbutton.TButton', width=20)
            button.pack(side=tk.LEFT, padx=10, pady=10)

    def run_module(self, module_info):
        try:
            self.window.destroy()
            module_info.function(*module_info.args, **module_info.kwargs)
        except Exception as e:
            print(f"Error running module {module_info.name}: {e}")

    def run(self):
        self.window.mainloop()

if __name__ == '__main__':
    modules = [
        Module("图片转PDF", jpgToPdf.main),
        Module("网速测试", speedTest.main),
        Module("随机抽签", drawing.main)
        # Add more modules in the future
    ]

    toolbox = ToolBox("欢迎来到秃子的工具箱", modules)
    toolbox.run()
