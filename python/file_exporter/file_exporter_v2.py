import argparse
import base64
import json
import logging
import os
import time
import glob

import requests
import urllib3
from prometheus_client import CollectorRegistry
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily

# logging.basicConfig(level=logging.DEBUG)


class FileSizeCollector(object):
    def __init__(self):
        pass

    def collect(self):
        file_size_metric = GaugeMetricFamily(
            'lwe_file_size_bytes',
            'Size of file',
            labels=['service_name', 'module_code', 'path', 'file_name', 'user_manager'])

        for info in config:
            file_path = '{}/{}'.format(info['path'], info['file_name'])
            value = self.get_file_size_bytes(file_path)
            if value is not None:
                file_size_metric.add_metric(
                    labels=[
                        info['services_name'],
                        info['module_code'],
                        info['path'],
                        info['file_name'],
                        info['user_manager']
                    ], value=value)

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
            'lwe_file_last_modified_seconds',
            'Last modified time of file',
            labels=['service_name', 'module_code', 'path', 'file_name', 'user_manager'])

        for info in config:
            file_path = '{}/{}'.format(info['path'], info['file_name'])
            value = self.get_file_last_modified(file_path)
            if value is not None:
                file_last_modified_metric.add_metric(
                    labels=[
                        info['services_name'],
                        info['module_code'],
                        info['path'],
                        info['file_name'],
                        info['user_manager']
                    ], value=value)

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
        directory_number_file_metric = GaugeMetricFamily(
            'lwe_directory_number_file',
            'Number of files in a directory',
            labels=['service_name', 'module_code', 'path', 'user_manager'])

        for info in config:
            directory_path = info['path']
            value = self.get_number_file_directory(directory_path)
            if value is not None:
                directory_number_file_metric.add_metric(
                    labels=[
                        info['services_name'],
                        info['module_code'],
                        info['path'],
                        info['user_manager']
                    ], value=value)

        yield directory_number_file_metric

    def get_number_file_directory(self, path):
        try:
            return len(os.listdir(path))
        except Exception as exc:
            logging.error(exc)


class DirectoryLastModifiedCollector(object):
    def __init__(self):
        pass

    def collect(self):
        directory_last_modified_metric = GaugeMetricFamily(
            'lwe_directory_last_modified_seconds',
            'Last modified time of directory',
            labels=['service_name', 'module_code', 'path', 'user_manager'])

        for info in config:
            directory_path = info['path']
            value = self.get_directory_last_modified(directory_path)
            if value is not None:
                directory_last_modified_metric.add_metric(
                    labels=[
                        info['services_name'],
                        info['module_code'],
                        info['path'],
                        info['user_manager']
                    ], value=value)

        yield directory_last_modified_metric

    def get_directory_last_modified(self, path):
        try:
            mod_time_since_epoch = os.path.getmtime(path)
            logging.debug('OK: Get last modified of directory: {}'.format(path))
            return mod_time_since_epoch
        except Exception as exc:
            logging.error(exc)


class FileLastCreatedCollector(object):
    def __init__(self):
        pass

    def collect(self):
        file_last_modified_metric = GaugeMetricFamily(
            'lwe_file_last_created_seconds',
            'Time of file created last in directory ',
            labels=['service_name', 'module_code', 'path', 'file_name', 'user_manager'])

        for info in config:
            directory_path = info['path']
            lasted_file, value = self.get_lasted_file_created(directory_path)
            if value is not None:
                file_last_modified_metric.add_metric(
                    labels=[
                        info['services_name'],
                        info['module_code'],
                        info['path'],
                        lasted_file,
                        info['user_manager']
                    ], value=value)

        yield file_last_modified_metric

    def get_lasted_file_created(self, path):
        try:
            list_of_files = glob.glob(path + '/*')
            latest_file = max(list_of_files, key=os.path.getctime)
            logging.debug('OK: Get lasted file created in directory: {}'.format(path))
            return latest_file, os.path.getctime(latest_file)
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
        default='config.json',
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


def parse_json(config_path):
    # Load configuration
    with open(config_path) as json_file:
        data = json.load(json_file)

    return data


def get_token():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    url = 'https://10.240.202.144/v1/auth'
    username = 'observer'
    password = 'Wcb9qSWt5uhEqbWVtAk^D#k!hxGi^gAAK2TJPePB3I4B6zLqBh*c&jm7W%j^NyGG'
    payload = "%s:%s" % (username, password)
    # Encode user and pass to BASE64
    b64val = base64.b64encode(payload.encode())

    headers = {
        'Authorization': 'Basic %s' % b64val.decode('ascii')
    }

    response = requests.request(method='GET', url=url, headers=headers, verify=False)

    data = json.loads(response.text)
    return data['token']


def get_config(ip_server):
    url = "https://10.240.202.144/v1/custom-api/get_log_path_by_ip"

    token = get_token()

    headers = {
        "Authorization": "JWT {}".format(token)
    }

    params = {
        'ipserver': ip_server
    }

    response = requests.request(method="GET", url=url, headers=headers, params=params, verify=False)
    config = json.loads(response.text)
    return config


def main():
    try:
        args = parse_args()
        port = int(args.port)
        config_path = args.config_path

        global config
        # config = get_config(ip_server='10.60.101.202')
        config = parse_json(config_path)

        registry = CollectorRegistry()
        registry.register(FileSizeCollector())
        registry.register(FileLastModifiedCollector())
        registry.register(NumberFileDirectoryCollector())
        registry.register(DirectoryLastModifiedCollector())
        registry.register(FileLastCreatedCollector())
        start_http_server(port, registry=registry)

        # REGISTRY.register(FileSizeCollector(config))
        # REGISTRY.register(LastModifiedCollector(config))
        # start_http_server(port)

        logging.info("Listening on :{}".format(port))
        while True:
            time.sleep(30)
            # config = parse_json('config1.yml')
    except KeyboardInterrupt:
        logging.info("Interrupted")
        exit(0)


if __name__ == '__main__':
    main()

