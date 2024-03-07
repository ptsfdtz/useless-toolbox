import pandas as pd
import random
from collections import Counter
import tkinter as tk
from tkinter import ttk, messagebox

class DrawingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("抽签程序")
        self.master.geometry("400x250")
        self.master.configure(bg='#f0f0f0')
        #添加一个背景图
        # self.master.background()

        self.label = ttk.Label(master, text="点击按钮进行抽签", font=("Arial", 18))
        self.label.pack(pady=20)

        style = ttk.Style()
        style.configure('TButton', font=('Arial', 14))

        self.button = ttk.Button(master, text="抽签", command=self.draw)
        self.button.pack()

    def drawing(self):
        data = pd.read_excel('index.xlsx')

        output_dict = {}

        for index, row in data.iterrows():
            name = row['姓名']
            output_dict[str(index)] = name
    
        return output_dict

    def draw(self):
        iterations = 1 
        result_dict = self.drawing()

        selected_list = [random.choice(list(result_dict.values())) for _ in range(iterations)]

        most_common_person, _ = Counter(selected_list).most_common(1)[0]

        message = f"恭喜你 {most_common_person} 被抽中了！"
        self.label.config(text=message)

        self.label.after(2000, self.fade_out)

        messagebox.showinfo("恭喜", message)

    def fade_out(self):
        current_color = self.label.cget("foreground")
        new_color = self.master.winfo_rgb(current_color)
        new_color = "#{:02x}{:02x}{:02x}".format(*new_color)

        self.label.config(foreground=new_color)

def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
