import argparse
import os
import subprocess
import time
import itertools

from prometheus_client import start_http_server, REGISTRY
from prometheus_client.core import GaugeMetricFamily

FILE_PATHS = ['/var/log/syslog', '/var/log/auth.log']


class FileCollector(object):
    def collect(self):
        metrics = {
            'file_size_bytes': GaugeMetricFamily(
                'file_size_bytes',
                'Size of file',
                labels=['path_file']),
            'last_modified_file_seconds': GaugeMetricFamily(
                'last_modified_file_seconds',
                'Last modified time of file',
                labels=['path_file']),
        }

        for path in FILE_PATHS:
            metrics['file_size_bytes'].add_metric([path],
                                       float(get_file_size_bytes(path)))
            metrics['last_modified_file_seconds'].add_metric([path],
                                          float(get_last_modified_file(path)))
        # yield metrics
        return itertools.chain(metrics.values())

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


def get_output(command):
    try:
        output = subprocess.check_output(command, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        return None
    return output.decode("utf-8")

def parse_args():
    parser = argparse.ArgumentParser(
        description='File collector that collects and expose metrics'
    )

    parser.add_argument(
        '-p', '--port',
        metavar='port',
        required=False,
        type=int,
        help='Listen to this port',
        default=int(os.environ.get('VIRTUAL_PORT', '9999'))
    )

    return parser.parse_args()


def main():
    try:
        args = parse_args()
        port = int(args.port)
        REGISTRY.register(FileCollector())
        start_http_server(port)
        print("Serving at port: {}".format(port))
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(" Interrupted")
        exit(0)


if __name__ == '__main__':
    main()
