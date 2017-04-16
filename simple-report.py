# -*- coding=UTF-8 -*-
from time import strftime, localtime

from collectors import *
from config import load_properties
from mailer import *

SUBJECT_TEMPLATE = "Raport Serwera Raspberry %s - %s"

MESSAGE_TEMPLATE = """
Raport działania serwera Raspberry:

Uptime: %s
Cups on-line: %s
IP zewnętrzne: %s

Wygenerowano: %s
"""


def create_message_body(uptime_report, cups_report, ip_report):
    return MESSAGE_TEMPLATE % (
        uptime_report.data,
        boolean_to_string(cups_report.success),
        ip_report.data, get_time_string_shorter())


def create_subject(uptime_report, cups_report, ip_report):
    is_ok = uptime_report.success and cups_report.success and ip_report.success
    return SUBJECT_TEMPLATE % (get_time_string(), boolean_to_status(is_ok))


def boolean_to_status(bool):
    if bool:
        return "OK"
    else:
        return "BŁĄD"


def boolean_to_string(bool):
    if bool:
        return "tak"
    else:
        return "nie"


def get_time_string():
    return strftime("%Y-%m-%d %H:%M:%S", localtime())


def get_time_string_shorter():
    return strftime("%Y-%m-%d %H:%M", localtime())


if __name__ == '__main__':
    configuration = load_properties('config.properties')
    uptime_report = UptimeCollector().collect()
    ip_report = IPCollector.by_config(configuration).collect()
    cups_report = CupsCollector.by_config(configuration).collect()

    smtp_connection = get_smtp_ssl_connection_from_properties(configuration)

    send_mail_with_fields_from_properties(smtp_connection=smtp_connection,
                                          properties=configuration,
                                          subject=create_subject(uptime_report, cups_report, ip_report),
                                          message_body=create_message_body(uptime_report, cups_report, ip_report),
                                          cups_data=cups_report.data)
