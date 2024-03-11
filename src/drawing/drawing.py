import pandas as pd
import random
from collections import Counter
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
class DrawingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("抽签程序")
        self.master.geometry("400x250")
        self.master.configure(bg='#f0f0f0')

        self.label = ttk.Label(master, text="点击按钮选择文件", font=("Arial", 18))
        self.label.pack(pady=10)

        style = ttk.Style()
        style.configure('TButton', font=('Arial', 14))

        self.choose_file_button = ttk.Button(master, text="选择文件", command=self.choose_file)
        self.choose_file_button.pack(pady=10)

        self.draw_button = ttk.Button(master, text="抽签", state=tk.DISABLED, command=self.draw)
        self.draw_button.pack()

        self.selected_file = None

    def choose_file(self):
        self.selected_file = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if self.selected_file:
            self.label.config(text=f"已选择文件：{self.selected_file}")
            self.draw_button.config(state=tk.NORMAL)

    def drawing(self, file_path):
        data = pd.read_excel(file_path)

        output_dict = {}

        for index, row in data.iterrows():
            name = row['姓名']
            output_dict[str(index)] = name
    
        return output_dict

    def draw(self):
        if not self.selected_file:
            messagebox.showwarning("警告", "请选择一个有效的Excel文件。")
            return

        iterations = 1 
        result_dict = {}
        
        result_dict[self.selected_file] = self.drawing(self.selected_file)

        selected_list = [random.choice(list(result_dict[self.selected_file].values())) for _ in range(iterations)]

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