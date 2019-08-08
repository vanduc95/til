import argparse
import logging
import os
import time
import json

import yaml
from prometheus_client import CollectorRegistry
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily

logging.basicConfig(level=logging.DEBUG)


class FileSizeCollector(object):
    def __init__(self):
        pass

    def collect(self):
        file_size_metric = GaugeMetricFamily(
            'file_size_bytes',
            'Size of file',
            labels=['path'])

        for path in config['file_paths']:
            value = self.get_file_size_bytes(path)
            if value is not None:
                file_size_metric.add_metric(
                    labels=[path], value=value)

        yield file_size_metric

    def get_file_size_bytes(self, path):

        if os.path.isfile(path):
            try:
                file_size = os.path.getsize(path)
                logging.debug('OK: Get file size at {}'.format(path))
                return file_size
            except Exception as exc:
                logging.error(exc)
        elif os.path.isdir(path):
            try:
                file_size = 0
                for dirpath, dirnames, filenames in os.walk(path):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        # skip if it is symbolic link
                        if not os.path.islink(fp):
                            file_size += os.path.getsize(fp)
                logging.debug('OK: Get file size: {}'.format(path))
                return file_size
            except Exception as exc:
                logging.error(exc)
        else:
            logging.error("No such file or directory or it is a special file")


class FileLastModifiedCollector(object):
    def __init__(self):
        pass

    def collect(self):
        file_last_modified_metric = GaugeMetricFamily(
            'file_last_modified_seconds',
            'Last modified time of file',
            labels=['path'])

        for path in config['file_paths']:
            value = self.get_file_last_modified(path)
            if value is not None:
                file_last_modified_metric.add_metric(
                    labels=[path], value=value)

        yield file_last_modified_metric

    def get_file_last_modified(self, path):
        try:
            mod_time_since_epoch = os.path.getmtime(path)
            logging.debug('OK: Get last modified of file: {}'.format(path))
            return mod_time_since_epoch
        except Exception as exc:
            logging.error(exc)


class NumberFileDirectoryCollector(object):
    def __init__(self):
        pass

    def collect(self):
        number_file_directory_metric = GaugeMetricFamily(
            'log_number_file_directory_metric',
            'Number of files in a directory', labels=['path'])

        for path in config['file_paths']:
            value = self.get_number_file_directory(path)
            if value is not None:
                number_file_directory_metric.add_metric(
                    labels=[path], value=value)

        yield number_file_directory_metric

    def get_number_file_directory(self, path):
        try:
            return len(os.listdir(path))
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


def parse_json(config_path):
    # Load configuration
    with open(config_path) as json_file:
        data = json.load(json_file)

    return data

def main():
    try:
        args = parse_args()
        port = int(args.port)
        config_path = args.config_path

        global config
        config = parse_yml(config_path)
        # config = parse_json(config_path)

        registry = CollectorRegistry()
        registry.register(FileSizeCollector())
        registry.register(FileLastModifiedCollector())
        registry.register(NumberFileDirectoryCollector())
        start_http_server(port, registry=registry)

        # REGISTRY.register(FileSizeCollector(config))
        # REGISTRY.register(LastModifiedCollector(config))
        # start_http_server(port)

        logging.info("Listening on :{}".format(port))
        while True:
            time.sleep(5)
            config = parse_yml('config1.yml')
    except KeyboardInterrupt:
        logging.info("Interrupted")
        exit(0)


if __name__ == '__main__':
    main()
    # print(type(parse_json('config1.yml')))
