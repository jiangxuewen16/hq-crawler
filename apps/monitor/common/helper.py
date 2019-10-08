from core.lib.emailer import Email
from hq_crawler import settings


def send_email(receivers: list, cc_mail: list, subject: str, msg: str):
    mail_conf = settings.EMAIL_CONF
    Email(mail_conf['host'], mail_conf['port'], mail_conf['user_name'], mail_conf['password']) \
        .set_sender(mail_conf['sender'], mail_conf['sender_name']).set_receiver(receivers, cc_mail) \
        .send(subject, msg)
