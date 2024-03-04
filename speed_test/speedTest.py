import speedtest
import tkinter as tk
from tkinter import Label, Button

def run_speed_test():

    status_label.config(text="正在测试ing...")
    
    test = speedtest.Speedtest()

    test.get_servers()

    best = test.get_best_server()

    download_speed = int(test.download() / 1024 / 1024)
    upload_speed = int(test.upload() / 1024 / 1024)

    download_label.config(text="下载速度:" + str(download_speed) + " Mbits")
    upload_label.config(text="上传速度:" + str(upload_speed) + " Mbits")

window = tk.Tk()
window.title("Speed Test GUI")

window.geometry("400x200")  

status_label = Label(window, text="点击开始")
download_label = Label(window, text="")
upload_label = Label(window, text="")
test_button = Button(window, text="运行速度测试", command=run_speed_test)

status_label.pack(pady=10)
test_button.pack(pady=10)
download_label.pack()
upload_label.pack()

def main():
    window.mainloop()

if __name__ == "__main__":
    main()