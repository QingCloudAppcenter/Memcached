import subprocess
import sys
import json

CONFIG_FILE = '/etc/memcached.conf'

def run_cmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, error = p.communicate()
    return out.decode('utf-8')

def get_port():
    # default
    port = '11211'
    
    with open(CONFIG_FILE) as f:
        lines = f.readlines()
        for line in lines:
            if len(line) == 0:
                continue
            config = line.rstrip().split(' ')
            if config[0] == '-p':
                port = config[1]
                break
    return port

def collect_data():

    data = {}
    
    cmd = "/bin/echo -e 'stats\nquit' | /bin/nc 127.0.0.1 %s" % get_port()
    out = run_cmd(cmd)
    ori_data = {}
    for item in out.split('\r\n'):
        item = item.split()
        if len(item) == 3:
            if item[2].isdigit():
                ori_data[item[1]] = int(item[2])

    data['get_count'] = ori_data['cmd_get']
    data['set_count'] = ori_data['cmd_set']
    data['delete_count'] = ori_data['delete_misses'] + ori_data['delete_hits']
    data['incr_count'] = ori_data['incr_misses'] + ori_data['incr_hits']
    data['decr_count'] = ori_data['decr_misses'] + ori_data['decr_hits']
    data['touch_count'] = ori_data['cmd_touch']
    data['cas_count'] = ori_data['cas_misses'] + ori_data['cas_hits']
    data['flush_count'] = ori_data['cmd_flush']

    hit_count = ori_data['get_hits']+ori_data['delete_hits']+ori_data['incr_hits']+ori_data['decr_hits']+ori_data['cas_hits']+ori_data['touch_hits']
    miss_count = ori_data['get_misses']+ori_data['delete_misses']+ori_data['incr_misses']+ori_data['decr_misses']+ori_data['cas_misses']+ori_data['touch_misses']
    data['his_rate'] = float(hit_count)/(hit_count+miss_count) if (hit_count+miss_count != 0) else 0
    data['get_hits'] = ori_data['get_hits']
    data['get_misses'] = ori_data['get_misses']

    data['evictions_count'] = ori_data['evictions']
    data['reclaimed_count'] = ori_data['reclaimed']

    data['cur_connections'] = ori_data['curr_connections']
    data['total_connections'] = ori_data['total_connections']

    return data


if __name__ == '__main__':
    
    d = json.dumps(collect_data())
    print(d)