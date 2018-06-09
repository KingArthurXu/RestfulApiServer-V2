#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur Xu'

import logging


import os
import platform
import subprocess

log = logging.getLogger(__name__)

# is_win = True if platform.system() == 'Windows' else False
# bin_admin_path = r'C:\Program Files\Veritas\NetBackup\bin\admincmd' if is_win else r'/usr/openv/netbackup/bin/admincmd'
# BPDBJOBS = r'bpgetconfig.exe' if is_win else r'bpgetconfig'
#
# bpdbjobs_path = os.path.join(os.path.join(bin_admin_path, BPDBJOBS))


# comm1="hdfs dfs -cat test.log.lzo"
# comm2="lzop -d"
# comm3="head -n 2"
# p1=subprocess.Popen(comm1,shell=True,stdout=subprocess.PIPE)
# p2=subprocess.Popen(comm2,shell=True,stdoin=p1.stdout,stdout=subprocess.PIPE)
# p3=subprocess.Popen(comm3,shell=True,stdoin=p2.stdout,stdout=subprocess.PIPE)


def exec_command(*params):
    out = ''
    with open(os.devnull, 'w') as FNULL:
        try:
            logging.info("Start execute command")
            # out = subprocess.Popen(params,stdout=subprocess.PIPE, stderr=FNULL).communicate()[0].strip()
            out = subprocess.Popen(params, cwd='C:\Users\Qingyu.Xu\PycharmProjects\RestfulApiServer\App\static\uploads',
                                   stdout=subprocess.PIPE, stderr=FNULL).communicate()[0].strip()
        except subprocess.CalledProcessError:
            # logging.warn("Can't reach host {0}".format(host))
            logging.warn("Failed to execute {0}".format(command))
        if len(out) != 0:
            return out

if __name__ == "__main__":
    # out = exec_command('C:\\Users\\Qingyu.Xu\\PycharmProjects\\RestfulApiServer\\App\\static\\uploads\\bp.bat')
    out = exec_command('hostname')
    print out

