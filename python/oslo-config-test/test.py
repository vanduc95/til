from oslo_config import cfg

new_conf = cfg.ConfigOpts()
project_args = ['--config-file', 'app.conf']
new_conf(project_args)

print new_conf._parse_config_files()