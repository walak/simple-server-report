# -*- coding=UTF-8 -*-
from datetime import timedelta
from http.client import HTTPConnection, HTTPSConnection

ENCODING = "UTF-8"
GET_METHOD = "GET"


class CollectingResult:
    def __init__(self, sucess=True, data=None):
        self.success = sucess
        if data is None:
            self.data = ""
        else:
            self.data = data


class GenericCollector:
    def collect(self):
        raise NotImplementedError()


class UptimeCollector(GenericCollector):
    UPTIME_FILE = '/proc/uptime'

    def collect(self):
        uptime_file = None
        try:
            uptime_file = open(self.UPTIME_FILE)
            uptime_string = uptime_file.readline().split()[0]
            converted_string = str(timedelta(seconds=float(uptime_string)))
            return CollectingResult(data=converted_string)
        except Exception as e:
            return CollectingResult(sucess=False, data=e.args[1])
        finally:
            uptime_file.close()


class CupsCollector(GenericCollector):
    def __init__(self, cups_host, cups_port, cups_url):
        self.cups_host = cups_host
        self.cups_port = cups_port
        self.cups_url = cups_url

    def collect(self):
        connection = HTTPConnection(host=self.cups_host, port=self.cups_port)
        try:
            connection.connect()
            connection.request(GET_METHOD, self.cups_url)
            response = connection.getresponse()
            if response.code == 200:
                response_text = "".join([l.decode(ENCODING) for l in response.readlines()])
                return CollectingResult(data=response_text)
            else:
                return CollectingResult(sucess=False, data=response.msg)
        except Exception as e:
            return CollectingResult(sucess=False, data=e.args[1])
        finally:
            connection.close()

    @staticmethod
    def by_config(config):
        return CupsCollector(cups_host=config['cups_host'],
                             cups_port=config['cups_port'],
                             cups_url=config['cups_url'])


class IPCollector(GenericCollector):
    def __init__(self, ip_api_host, ip_api_url):
        self.ip_api_host = ip_api_host
        self.ip_api_url = ip_api_url

    def collect(self):
        connection = HTTPSConnection(self.ip_api_host)
        try:
            connection.connect()
            connection.request(GET_METHOD, self.ip_api_url)
            response = connection.getresponse()
            if response.code == 200:
                return CollectingResult(data=response.readline().decode(ENCODING))
            else:
                return CollectingResult(sucess=False, data="0.0.0.0")
        except Exception as e:
            return CollectingResult(sucess=False, data=e.args[1])
        finally:
            connection.close()

    @staticmethod
    def by_config(config):
        return IPCollector(ip_api_host=config['ip_api_host'],
                           ip_api_url=config['ip_api_url'])
