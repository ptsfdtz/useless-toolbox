import smtplib
from getpass import getpass
from email.message import EmailMessage
import pandas as pd
import tkinter as tk
from tkinter import ttk
from threading import Thread

def get_smtp_settings(email_address):
    domain = email_address.split('@')[1].lower()

    if domain == '163.com':
        return 'smtp.163.com', 465
    elif domain == 'gmail.com':
        return 'smtp.gmail.com', 465
    elif domain == 'qq.com':
        return 'smtp.qq.com', 465
    else:
        raise ValueError(f"不支持的电子邮件域名: {domain}")

def send_email(email_address, email_password, filename, recipient_name, recipient_email, progress_var):
    smtp_host, smtp_port = get_smtp_settings(email_address)
    smtp = smtplib.SMTP_SSL(smtp_host, smtp_port)

    subject = "Python邮件主题"
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = recipient_email

    with open(filename, 'r', encoding='utf-8') as f:
        file_content = f.read()

    # 在文件内容开头添加个人姓名
    modified_content = f"{recipient_name}, {file_content}"

    msg.set_content(modified_content)

    smtp.login(email_address, email_password)
    smtp.send_message(msg)

    for i in range(100):
        progress_var.set(i)

    smtp.quit()

def read_message_data():
    file_path = 'src/send_message/index.xlsx'
    data = pd.read_excel(file_path)
    result_dict = data.set_index('姓名')['邮箱'].to_dict()
    return result_dict

def main():
    def on_send_button_click():
        email_address = email_entry.get()
        email_password = password_entry.get()
        recipient_data = read_message_data()

        progress_var.set(0)

        send_thread = Thread(target=send_emails, args=(email_address, email_password, recipient_data))
        send_thread.start()

    def send_emails(email_address, email_password, recipient_data):
        for i, (recipient_name, recipient_email) in enumerate(recipient_data.items(), 1):
            filename = r"src\send_message\test.txt"
            send_email(email_address, email_password, filename, recipient_name, recipient_email, progress_var)

        progress_var.set(100)

    root = tk.Tk()
    root.title("邮件发送器")

    style = ttk.Style()
    style.theme_use("clam")

    font_style = ('Helvetica', 14)

    email_label = ttk.Label(root, text="邮箱:", font=font_style)
    email_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
    email_entry = ttk.Entry(root, font=font_style)
    email_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

    password_label = ttk.Label(root, text="密码:", font=font_style)
    password_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
    password_entry = ttk.Entry(root, show="*", font=font_style)
    password_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

    send_button = ttk.Button(root, text="发送邮件", command=on_send_button_click, style="TButton")
    send_button.grid(row=2, column=0, columnspan=2, pady=20)

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(root, variable=progress_var, mode='determinate', length=200)
    progress_bar.grid(row=3, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == '__main__':
    main()
