import speedtest
import tkinter as tk
from tkinter import Label, Button

class SpeedTestApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Speed Test")
        self.master.geometry("400x200")

        self.status_label = Label(master, text="点击开始")
        self.download_label = Label(master, text="")
        self.upload_label = Label(master, text="")
        self.test_button = Button(master, text="运行速度测试", command=self.run_speed_test)

        self.status_label.pack(pady=10)
        self.test_button.pack(pady=10)
        self.download_label.pack()
        self.upload_label.pack()

    def run_speed_test(self):
        self.status_label.config(text="正在测试ing...")

        test = speedtest.Speedtest()
        test.get_servers()
        best = test.get_best_server()

        download_speed = int(test.download() / 1024 / 1024)
        upload_speed = int(test.upload() / 1024 / 1024)

        self.download_label.config(text=f"下载速度: {download_speed} Mbits")
        self.upload_label.config(text=f"上传速度: {upload_speed} Mbits")

        self.status_label.config(text="测试完成")
        self.master.update()

def main():
    root = tk.Tk()
    app = SpeedTestApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
