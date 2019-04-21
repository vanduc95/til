#! /usr/bin/env python
from oslo_config import cfg
import sys
import service
import con

opt_simple_group = cfg.OptGroup(name='simple',
                                title='A Simple Example')

opt_moredata_group = cfg.OptGroup(name='moredata',
                                  title='A More Complex Example')
simple_opts = [
    cfg.BoolOpt('enable', default=False,
                help=('True enables, False disables'))
]

moredata_opts = [
    cfg.StrOpt('message', default='duc',
               choices=['duc', 'mai', 'linh'],
               help=('A message')),
    cfg.ListOpt('usernames', default=None,
                help=('A list of usernames')),
    cfg.DictOpt('jobtitles', default=None,
                help=('A dictionary of usernames and job titles')),
    cfg.IntOpt('payday', default=30,
               help=('Default payday monthly date')),
    cfg.FloatOpt('pi', default=0.0,
                 help=('The value of Pi')),
    cfg.HostAddressOpt('host', default='ub',
                       sample_default='example.domain',
                       help='Hostname')
]

CONF = cfg.CONF

CONF.register_group(opt_simple_group)
CONF.register_opts(simple_opts, opt_simple_group)

CONF.register_group(opt_moredata_group)
CONF.register_opts(moredata_opts, opt_moredata_group)

if __name__ == "__main__":
    CONF(sys.argv[1:], project='app')
    # service.prepare_service()
    print CONF.simple.enable
    print CONF.moredata.usernames
    print CONF.moredata.message
    print CONF.moredata.host
    con.alm()
