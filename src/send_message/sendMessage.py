import smtplib
from getpass import getpass
from email.message import EmailMessage
import pandas as pd

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

def send_email(email_address, email_password, filename, recipient_name, recipient_email):
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
    smtp.quit()

def read_message_data():
    file_path = 'src/send_message/index.xlsx'
    data = pd.read_excel(file_path)
    result_dict = data.set_index('姓名')['邮箱'].to_dict()
    return result_dict

def main():
    EMAIL_ADDRESS = input('请输入您的电子邮件地址: ')
    EMAIL_PASSWORD = getpass('请输入您的电子邮件密码: ')

    recipient_data = read_message_data()

    for recipient_name, recipient_email in recipient_data.items():
        filename = r"src\send_message\test.txt"
        send_email(EMAIL_ADDRESS, EMAIL_PASSWORD, filename, recipient_name, recipient_email)

if __name__ == '__main__':
    main()
