import speedtest
import tkinter as tk
from tkinter import Label, Button
from tkinter import ttk

class SpeedTestApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Speed Test")
        self.master.geometry("300x250")

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure("RoundedButton.TButton", borderwidth=5, relief="ridge", padding=10, background="lightgray")

        self.status_label = Label(self.master, text="网速测试,单位为Mbps")
        self.download_label = Label(self.master, text="")
        self.upload_label = Label(self.master, text="")

        self.progress_bar = ttk.Progressbar(self.master, orient=tk.HORIZONTAL, length=200, mode='determinate')

        self.test_button = ttk.Button(self.master, text="运行速度测试", command=self.run_speed_test,
                                      compound=tk.LEFT, style="RoundedButton.TButton")

        self.status_label.pack(pady=10)
        self.download_label.pack(pady=5)
        self.upload_label.pack(pady=5)
        self.progress_bar.pack(pady=10)
        self.test_button.pack(pady=10)

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
        self.progress_bar.stop()
        self.progress_bar["value"] = 100  # Set progress to 100% after completion

def main():
    root = tk.Tk()
    app = SpeedTestApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
