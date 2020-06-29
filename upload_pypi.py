"""
whatprovides upload_pypi.py

This script runs 'twine upload dist/whatprovides-{VERSION}.tar.gz dist/whatprovides-{VERSION}-*.whl'
"""
import os
import subprocess
from typing import List
from whatprovides.version import VERSION

SCRIPT_DIR: str = os.path.dirname(os.path.abspath(__file__))


def get_pip_config():
    process: subprocess.Popen = subprocess.Popen(
        ['pip', 'config', 'list', ], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    process.wait()
    if not process.returncode:
        if process.stdout.readable():
            return list(map(lambda x: x.decode().rstrip(), process.stdout.readlines()))
        else:
            return []  # pip configuration is empty
    else:
        if process.stdout.readable():
            print(process.stdout.read().decode())
        if process.stderr.readable():
            print(process.stderr.read().decode())
        exit(1)


def run_upload():
    pip_certs: List[str] = list(filter(lambda x: str(x).startswith('global.cert='), get_pip_config()))
    if pip_certs:
        pip_cert_arg: str = '--cert %s ' % (pip_certs[0].split('=')[1])
    else:
        pip_cert_arg: str = ''
    print(pip_cert_arg)
    dist_dir: str = os.path.join(SCRIPT_DIR, 'dist')
    dist_file: str = os.path.join(dist_dir, 'whatprovides-%s.tar.gz' % (VERSION, ))
    dist_whls: str = os.path.join(dist_dir, 'whatprovides-%s-*.whl' % (VERSION, ))
    os.system('twine upload "%s" "%s" %s --verbose' % (dist_file, dist_whls, pip_cert_arg))
    print('__end__')


if __name__ == '__main__':
    run_upload()
