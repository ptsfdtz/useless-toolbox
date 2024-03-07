import smtplib
from getpass import getpass
from email.message import EmailMessage

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

EMAIL_ADDRESS = input('Enter your email address: ')
EMAIL_PASSWORD = getpass('Enter your email password: ')
TO_EMAIL_ADDRESS = input('Enter the recipient email address: ')
smtp_host, smtp_port = get_smtp_settings(EMAIL_ADDRESS)
smtp = smtplib.SMTP_SSL(smtp_host, smtp_port)

subject = "Python email subject"
msg = EmailMessage()
msg['Subject'] = subject
msg['From'] = EMAIL_ADDRESS
msg['To'] = TO_EMAIL_ADDRESS

filename = r"src\send_message\test.txt"

with open(filename, 'r', encoding='utf-8') as f:
    file_content = f.read()

msg.set_content(file_content)

smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
smtp.send_message(msg)
smtp.quit()
