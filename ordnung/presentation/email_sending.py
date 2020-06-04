# -*- coding: utf-8 -*-

"""Инструменты для работы с электронной почтой.
"""
# import os
import smtplib
# from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

from starlette.requests import Request

from ordnung import settings
from loguru import logger

from ordnung.core.access import generate_token, get_monotonic


class SMTPServer:
    """
    """

    def __init__(self,
                 username: str = settings.EMAIL_LOGIN,
                 password: str = settings.EMAIL_PASSWORD,
                 host: str = settings.EMAIL_HOST,
                 port: int = settings.EMAIL_PORT):
        """
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def __enter__(self):
        """
        """
        self.server = smtplib.SMTP(self.host, self.port)
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()
        self.server.login(self.username, self.password)
        return self.server

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        """
        self.server.quit()
        if exc_val:
            logger.exception('Fail')
            # raise


def send_email(subject: str, targets: List[str], html: str,
               sender: str = settings.EMAIL_SENDER):
    """
    """
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(targets)

    text = MIMEText(html, "html", 'UTF-8')
    msg.attach(text)

    # paths = ['logo.jpg', '../logo.jpg', '../../logo.jpg']
    # for path in paths:
    #     if os.path.exists(path):
    #         with open(path, 'rb') as f:
    #             img = MIMEImage(f.read())
    #             img.add_header('Content-ID', 'logo.jpg')
    #             msg.attach(img)
    #         break
    # 
    # for file in files:
    #     data = MIMEBase('application', file['mime'])
    #     data.set_payload(file['data'].read())
    #     encoders.encode_base64(data)
    #     filename = Header(file['filename'], 'utf-8').encode()
    #     parameters = {
    #         'filename*': filename,  # RFC2231
    #         'filename': filename,  # RFC2047
    #     }
    #     data.add_header('Content-Disposition', 'attachment', **parameters)
    #     msg.attach(data)

    with SMTPServer(sender) as server:
        server.sendmail(sender, targets, msg.as_string())


def send_restore_email(request: Request, user_id: int, email: str) -> str:
    """Send link with password restore URL to the user.
    """
    token = generate_token(
        payload={'user_id': user_id, 'monotonic': get_monotonic()},
        salt='restore_password'
    )
    restore_confirm_url = request.url_for('restore_confirm', token=token)
    # todo
    send_email('Password restore', [email], f'Your password restore url: {restore_confirm_url}')
    return restore_confirm_url


def send_verification_email(request: Request, user_id: int, email: str) -> str:
    """Send link with account activation URL to the user.
    """
    token = generate_token(
        payload={'user_id': user_id, 'monotonic': get_monotonic()},
        salt='confirm_registration'
    )
    register_confirm_url = request.url_for('register_confirm', token=token)
    # todo
    send_email('Registration confirm', [email], f'Your confirmation url: {register_confirm_url}')
    return register_confirm_url