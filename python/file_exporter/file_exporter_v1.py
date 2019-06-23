import argparse
import logging
import os
import time

import yaml
from prometheus_client import CollectorRegistry
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily

logging.basicConfig(level=logging.DEBUG)


class FileSizeCollector(object):
    def __init__(self, config):
        self.config = config

    def collect(self):
        file_size_metric = GaugeMetricFamily(
            'file_size_bytes',
            'Size of file',
            labels=['path_file'])

        for path in self.config['file_paths']:
            value = self.get_file_size_bytes(path)
            if value is not None:
                file_size_metric.add_metric(
                    labels=[path], value=value
                )

        yield file_size_metric

    def get_file_size_bytes(self, file_path):
        try:
            file_size = os.path.getsize(file_path)
            return file_size
        except Exception as exc:
            logging.error(exc)


class LastModifiedCollector(object):
    def __init__(self, config):
        self.config = config

    def collect(self):
        last_modified_metric = GaugeMetricFamily(
            'last_modified_file_seconds',
            'Last modified time of file',
            labels=['path_file'])

        for path in self.config['file_paths']:
            value = self.get_last_modified_file(path)
            if value is not None:
                last_modified_metric.add_metric(
                    labels=[path], value=value
                )

        yield last_modified_metric

    def get_last_modified_file(self, file_path):
        try:
            mod_time_since_epoch = os.path.getmtime(file_path)
            return mod_time_since_epoch
        except Exception as exc:
            logging.error(exc)


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
            logging.error(exc)


def main():
    try:
        args = parse_args()
        port = int(args.port)
        config_path = args.config_path

        config = parse_yml(config_path)

        registry = CollectorRegistry()
        registry.register(FileSizeCollector(config))
        registry.register(LastModifiedCollector(config))
        start_http_server(port, registry=registry)

        # REGISTRY.register(FileSizeCollector(config))
        # REGISTRY.register(LastModifiedCollector(config))
        # start_http_server(port)

        print("Listening on :{}".format(port))
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        logging.info("Interrupted")
        exit(0)


if __name__ == '__main__':
    main()
