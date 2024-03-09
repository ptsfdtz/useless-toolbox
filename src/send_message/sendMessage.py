import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QProgressBar, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from threading import Thread
from email.message import EmailMessage
import smtplib
import pandas as pd
from PyQt5.QtWidgets import QDesktopWidget


class EmailSenderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("邮件发送器")
        self.resize(500, 300)

        font_style = ('Helvetica', 14)
        font = QFont(*font_style)

        self.email_label = QLabel("邮箱:", self)
        self.email_label.setFont(font)

        self.email_entry = QLineEdit(self)
        self.email_entry.setFont(font)

        self.password_label = QLabel("密码:", self)
        self.password_label.setFont(font)

        self.password_entry = QLineEdit(self)
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setFont(font)

        self.file_label = QLabel("选择名单文件:", self)
        self.file_label.setFont(font)

        self.file_entry = QLineEdit(self)
        self.file_entry.setFont(font)

        self.file_button = QPushButton("选择名单文件", self)
        self.file_button.clicked.connect(self.on_file_button_click)
        self.file_button.setFont(font)

        self.send_button = QPushButton("发送邮件", self)
        self.send_button.clicked.connect(self.on_send_button_click)
        self.send_button.setFont(font)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setFixedHeight(30) 
        self.progress_bar.setAlignment(Qt.AlignCenter) 

        layout = QVBoxLayout(self)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_entry)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_entry)
        layout.addWidget(self.file_label)
        layout.addWidget(self.file_entry)
        layout.addWidget(self.file_button)
        layout.addWidget(self.send_button)
        layout.addWidget(self.progress_bar)

        self.center_on_screen()  

    def center_on_screen(self):
        screen_geo = QDesktopWidget().screenGeometry()
        window_geo = self.frameGeometry()
        self.move((screen_geo.width() - window_geo.width()) // 2, (screen_geo.height() - window_geo.height()) // 2)

    def on_file_button_click(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "选择名单文件", "", "Excel Files (*.xlsx);;All Files (*)")
        if file_path:
            self.file_entry.setText(file_path)

    def on_send_button_click(self):
        email_address = self.email_entry.text()
        email_password = self.password_entry.text()
        file_path = self.file_entry.text()

        if not file_path:
            return  

        recipient_data = self.read_recipient_list(file_path)

        if not recipient_data:
            return 

        self.progress_bar.setValue(0)

        send_thread = Thread(target=self.send_emails, args=(email_address, email_password, recipient_data))
        send_thread.start()

    def send_emails(self, email_address, email_password, recipient_data):
        for i, (recipient_name, recipient_email) in enumerate(recipient_data.items(), 1):
            self.send_email(email_address, email_password, recipient_name, recipient_email)
            progress_value = int((i / len(recipient_data)) * 100)
            self.progress_bar.setValue(progress_value)

        self.progress_bar.setValue(100)

    def send_email(self, email_address, email_password, recipient_name, recipient_email):
        smtp_host, smtp_port = self.get_smtp_settings(email_address)
        smtp = smtplib.SMTP_SSL(smtp_host, smtp_port)

        subject = "Python邮件主题"
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = email_address
        msg['To'] = recipient_email

        msg.set_content(f"尊敬的 {recipient_name},你好")

        smtp.login(email_address, email_password)
        smtp.send_message(msg)

        smtp.quit()

    def get_smtp_settings(self, email_address):
        domain = email_address.split('@')[1].lower()

        if domain == '163.com':
            return 'smtp.163.com', 465
        elif domain == 'gmail.com':
            return 'smtp.gmail.com', 465
        elif domain == 'qq.com':
            return 'smtp.qq.com', 465
        else:
            raise ValueError(f"不支持的电子邮件域名: {domain}")

    def read_recipient_list(self, file_path):
        try:
            data = pd.read_excel(file_path)
            result_dict = data.set_index('姓名')['邮箱'].to_dict()
            return result_dict
        except FileNotFoundError:
            print(f"文件未找到：{file_path}")
        except Exception as e:
            print(f"读取文件时出错：{e}")
            return None


def main():
    app = QApplication(sys.argv)
    window = EmailSenderApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
