import argparse
import itertools
import logging
import os
import time

import yaml
from prometheus_client import start_http_server, REGISTRY
from prometheus_client.core import GaugeMetricFamily

logging.basicConfig(level=logging.DEBUG)


class FileCollector(object):
    def __init__(self, config):
        self.config = config

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

        for path in self.config['file_paths']:
            metrics['file_size_bytes'].add_metric(
                labels=[path], value=get_file_size_bytes(path)
            )
            metrics['last_modified_file_seconds'].add_metric(
                labels=[path], value=get_last_modified_file(path)
            )
        return itertools.chain(metrics.values())


def get_file_size_bytes(path_file):
    try:
        file_size = os.path.getsize(path_file)
        return file_size
    except Exception as exc:
        # logging.exception(exc)
        pass

def get_last_modified_file(path_file):
    try:
        mod_time_since_epoch = os.path.getmtime(path_file)
        return mod_time_since_epoch
    except Exception as exc:
        # logging.exception(exc)
        pass

def parse_args():
    parser = argparse.ArgumentParser(
        description='File collector that collects and expose metrics'
    )
    parser.add_argument(
        '--config_path',
        metavar='config_path',
        required=False,
        help='Path to configuration file',
        default='config.yml',
    )
    parser.add_argument(
        '--port',
        metavar='port',
        required=False,
        type=int,
        help='Listen to this port',
        default=9999
    )

    return parser.parse_args()


def parse_yml(config_path):
    # Load configuration
    with open(config_path, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logging.exception(exc)


def main():
    try:
        args = parse_args()
        port = int(args.port)
        config_path = args.config_path

        config = parse_yml(config_path)

        REGISTRY.register(FileCollector(config))
        start_http_server(port)
        print("Listening on :{}".format(port))
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        print("Interrupted")
        exit(0)


if __name__ == '__main__':
    main()

