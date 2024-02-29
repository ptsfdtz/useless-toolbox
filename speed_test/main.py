import speedtest
import tkinter as tk
from tkinter import Label, Button

def run_speed_test():
    print("准备测试ing...")

    # 创建实例对象
    test = speedtest.Speedtest()
    # 获取可用于测试的服务器列表
    test.get_servers()
    # 筛选出最佳服务器
    best = test.get_best_server()

    print("正在测试ing...")

    # 下载速度
    download_speed = int(test.download() / 1024 / 1024)
    upload_speed = int(test.upload() / 1024 / 1024)

    # 更新界面显示
    download_label.config(text="下载速度:" + str(download_speed) + " Mbits")
    upload_label.config(text="上传速度:" + str(upload_speed) + " Mbits")

# 创建主窗口
window = tk.Tk()
window.title("Speed Test GUI")

# 设置窗口大小
window.geometry("400x200")  # You can change the width and height as needed

# 添加标签和按钮
status_label = Label(window, text="点击开始")
download_label = Label(window, text="")
upload_label = Label(window, text="")
test_button = Button(window, text="运行速度测试", command=run_speed_test)

# 布局管理
status_label.pack(pady=10)
test_button.pack(pady=10)
download_label.pack()
upload_label.pack()

# No mainloop() here

# The window will stay open until explicitly closed
window.mainloop()
