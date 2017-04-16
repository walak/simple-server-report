# -*- coding=UTF-8 -*-
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL


def get_smtp_ssl_connection(host, port, user, password):
    smtpConnection = SMTP_SSL(host=host, port=port)
    smtpConnection.login(user=user, password=password)
    return smtpConnection


def get_smtp_ssl_connection_from_properties(properties):
    return get_smtp_ssl_connection(properties['smtp_host'],
                                   properties['smtp_port'],
                                   properties['smtp_user'],
                                   properties['smtp_password'])


def create_message(frm, to, subject):
    message = MIMEMultipart()
    message['From'] = frm
    message['To'] = to
    message['Subject'] = subject
    return message


def create_mime_body(content):
    text_attachment = MIMEText(content)
    return text_attachment


def create_file_attachment(attachment_content, filename='attachment.txt', mimetype='text/html'):
    file_attachment = MIMEApplication(str.encode(attachment_content, "UTF-8"), mimetype, Name=filename)
    file_attachment['Content-Disposition'] = 'attachment; filename="%s"' % filename
    return file_attachment


def send_mail(smtp_connection, frm, to, subject, message_body, cups_data):
    message = create_message(frm, to, subject)
    body = create_mime_body(message_body)
    cups_attachment = create_file_attachment(cups_data, 'cups_report.html')

    message.attach(body)
    message.attach(cups_attachment)

    smtp_connection.send_message(message)


def send_mail_with_fields_from_properties(smtp_connection, properties, subject, message_body, cups_data):
    return send_mail(smtp_connection=smtp_connection,
                     frm=properties['smtp_from'],
                     to=properties['smtp_to'],
                     subject=subject,
                     message_body=message_body,
                     cups_data=cups_data)
