#!/usr/bin/env python
# encoding: utf-8

"""
MongoDB backup and restore utility script.
"""

import subprocess
import shlex
import os


def restore():
    backup_name = os.getenv('BACKUP_NAME')
    s3_bucket = os.getenv('S3_BUCKET')
    s3_path = os.getenv('S3_PATH')
    if backup_name and s3_bucket and s3_path:
        commands = ['aws s3 cp s3://%s/%s/%s.tgz %s.tgz' % (s3_bucket, s3_path, backup_name, backup_name),
                    'tar xzf %s.tgz' % backup_name]
        for cmd in commands:
            print(cmd)
            subprocess.call(shlex.split(cmd))
            print('')

        # os.chdir(os.path.join('backup', backup_name))
        cmd = "mongorestore "
        args = [('--host=', 'MONGODB_BACKUP_HOST'),
                ('--port=', 'MONGODB_BACKUP_PORT'),
                ('--username=', 'MONGODB_BACKUP_USER'),
                ('--password=', 'MONGODB_BACKUP_PASS'),
                ('--db=', 'production')]
        for arg in args:
            if os.getenv(arg[1]):
                cmd += '%s%s ' % (arg[0], os.getenv(arg[1]))
        cmd += ' backup/%s' % os.getenv('MONGODB_BACKUP_DB')
        print(cmd)
        subprocess.call(shlex.split(cmd))
        print()


if __name__ == "__main__":
    restore()
