import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from enum import Enum


class EmailType(Enum):
    pass


class Email(object):
    # 设置服务器所需信息
    # 163邮箱服务器地址
    host = 'smtp.qq.com'
    port = 465
    # 163用户名
    user = ''
    # 密码(部分邮箱为授权码)
    password = ''
    # 邮件发送方邮箱地址
    sender = ''
    sender_name = ''

    receivers = []

    def __init__(self, host: str, port: int, user: str, password: str):
        self.port = port
        self.host = host
        self.user = user
        self.password = password

    def set_sender(self, sender: str, sender_name: str):
        self.sender = sender
        self.sender_name = sender_name
        return self

    def set_receiver(self, receivers: list):
        self.receivers = receivers
        return self

    def send(self, subject: str, msg: str):
        try:
            msg = MIMEText(msg, 'plain', 'utf-8')
            msg['From'] = formataddr([self.sender_name, self.sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = ','.join(self.receivers)  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = subject  # 邮件的主题，也可以说是标题

            server = smtplib.SMTP_SSL(self.host, self.port)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(self.user, self.password)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(self.sender, self.receivers, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.close()  # 关闭邮箱
            server.quit()  # 关闭连接
        except smtplib.SMTPException as e:  # 如果 try 中的语句没有执行，则会执行下面的
            print('发送失败:', e)

    def build_end_data(self):
        pass



