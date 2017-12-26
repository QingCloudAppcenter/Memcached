import subprocess
import sys


def run_cmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, error = p.communicate()
    return out.decode('utf-8')


if __name__ == '__main__':
    cmd = 'pidof memcached'
    ret = run_cmd(cmd).rstrip()
    
    if ret == '':
        sys.exit(-1)
    else:
        sys.exit(0)