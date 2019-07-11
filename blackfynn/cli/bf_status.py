'''
usage:
  bf status [options]

global options:
  -h --help                 Show help
  --dataset=<dataset>       Use specified dataset (instead of your current working dataset)
  --profile=<name>          Use specified profile (instead of default)
'''
from __future__ import absolute_import, division, print_function

from docopt import docopt

from .working_dataset import working_dataset_id


def main(bf):
    args = docopt(__doc__)
    print('Active profile:\n  \033[32m{}\033[0m\n'.format(bf.settings.active_profile))

    if len(bf.settings.env.keys()) > 0:
        key_len = 0
        value_len = 0
        for key,value in bf.settings.env.items():
            valstr = '{}'.format(value)
            key_len = max(key_len,len(key))
            value_len = max(value_len,len(valstr))

        print('Environment variables:')
        print('  \033[4m{:{key_len}}    {:{value_len}}    {}'.format('Key','Value','Environment Variable\033[0m',key_len=key_len,value_len=value_len))
        for value,evar in sorted(bf.settings.env.items()):
           valstr = '{}'.format(value)
           # get internal variable
           ivar=''
           for k,v in bf.settings.__dict__.items():
                if str(v) == str(evar):
                    ivar = k
           print('  {:{key_len}}    {:{value_len}}    {}'.format(ivar,evar,valstr,key_len=key_len,value_len=value_len))
        print()

    working_dataset_status = 'Not set.'
    ds = working_dataset_id()
    if ds:
        try:
            working_dataset = bf.get_dataset(ds)
            working_dataset_status = "{} (id: {})".format(working_dataset.name, working_dataset.id)
        except:
            pass

    print("Blackfynn environment:")
    print("  User               : {}".format(bf.profile.email))
    print("  Organization       : {} (id: {})".format(bf.context.name, bf.context.id))
    print("  Dataset            : {}".format(working_dataset_status))
    print("  API Location       : {}".format(bf.settings.api_host))
    print("  Streaming API      : {}".format(bf.settings.streaming_api_host))
