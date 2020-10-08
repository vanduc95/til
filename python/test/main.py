from pathlib import Path

import openpyxl
import yaml


class Module:
    def __init__(self, host, container_name, container_id):
        self.host = host
        self.container_name = container_name
        self.container_id = container_id
        self.name = container_name.replace('_', '-')
        self.port = -1


class Service:
    def __init__(self, service_name, module_group):
        self.service_name = service_name
        self.module_group = module_group
        self.modules = []
        self.hosts = []

    def set_modules(self, modules):
        for m in modules:
            if m.name in self.module_group:
                self.modules.append(m)

    def set_hosts(self):
        hosts = []
        for module in self.modules:
            hosts.append(module.host)
        self.hosts = list(dict.fromkeys(hosts))


if __name__ == '__main__':
    xlsx_file = Path('/home/ducnv/test/docker_infor.xlsx')
    wb_obj = openpyxl.load_workbook(xlsx_file)
    sheet = wb_obj.active
    modules = []
    for i, row in enumerate(sheet.iter_rows(values_only=True)):
        if i == 0:
            continue
        else:
            module = Module(host=row[0], container_id=row[1], container_name=row[2])
            modules.append(module)

    cloud_service = []
    with open("cloud.yaml", 'r') as stream:
        try:
            cloud_service = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    services = []
    for cs in cloud_service:
        service = Service(service_name=cs['service'], module_group=cs['modules'])
        service.set_modules(modules)
        service.set_hosts()
        services.append(service)

    print(services)
