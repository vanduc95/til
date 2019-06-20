from prometheus_client import start_http_server, REGISTRY
from prometheus_client.core import GaugeMetricFamily
import subprocess
import time
import os

FILE_PATHS = ['/var/log/syslog', '/var/log/auth.log']


class FileCollector(object):
    def __init__(self):
        pass

    def collect(self):
        file_size_bytes = GaugeMetricFamily('file_size_bytes', 'Size of file',
                                            labels=['path_file'])
        for path in FILE_PATHS:
            file_size_bytes.add_metric([path],
                                       float(get_file_size_bytes(path)))
        yield file_size_bytes

        last_modified_file = GaugeMetricFamily('last_modified_file_second',
                                               'Last modified time of file',
                                               labels=['path_file'])
        for path in FILE_PATHS:
            last_modified_file.add_metric([path],
                                          float(get_last_modified_file(path)))
        yield last_modified_file


def get_output(command):
    try:
        output = subprocess.check_output(command, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        return None
    return output.decode("utf-8")


def get_file_size_bytes(path_file):
    command = ['du', '-b', path_file]
    pipeline = ['cut', '-f1']
    try:
        p1 = subprocess.Popen(command, stdout=subprocess.PIPE)
        p2 = subprocess.Popen(pipeline, stdin=p1.stdout,
                              stdout=subprocess.PIPE)
        p1.stdout.close()
    except subprocess.CalledProcessError as e:
        print(e)
    return p2.communicate()[0].decode("utf-8")


def get_last_modified_file(path_file):
    command = ['stat', '-c', '%Y', path_file]
    return get_output(command)


def read_config():
    pass


def main():
    REGISTRY.register(FileCollector())
    start_http_server(8888)
    while True:
        time.sleep(5)


if __name__ == '__main__':
    main()
