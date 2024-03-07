import smtplib
from getpass import getpass
from email.message import EmailMessage
import readMessage

def get_smtp_settings(email_address):
    domain = email_address.split('@')[1].lower()

    if domain == '163.com':
        return 'smtp.163.com', 465
    elif domain == 'gmail.com':
        return 'smtp.gmail.com', 465
    elif domain == 'qq.com':
        return 'smtp.qq.com', 465
    else:
        raise ValueError(f"Unsupported email domain: {domain}")

def send_email(email_address, email_password, filename, recipient_name):
    smtp_host, smtp_port = get_smtp_settings(email_address)
    smtp = smtplib.SMTP_SSL(smtp_host, smtp_port)

    subject = "Python email subject"
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = email_address

    with open(filename, 'r', encoding='utf-8') as f:
        file_content = f.read()

    # 在文件内容开头添加个人姓名
    modified_content = f"{recipient_name}, {file_content}"

    msg.set_content(modified_content)

    smtp.login(email_address, email_password)
    smtp.send_message(msg)
    smtp.quit()

def main():
    EMAIL_ADDRESS = input('Enter your email address: ')
    EMAIL_PASSWORD = getpass('Enter your email password: ')
    
    recipient_data = readMessage.main()

    for recipient_name, recipient_email in recipient_data.items():
        filename = r"src\send_message\test.txt"
        send_email(EMAIL_ADDRESS, EMAIL_PASSWORD, filename, recipient_name)

if __name__ == '__main__':
    main()
