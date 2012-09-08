import gtk
import glib
import sys
import subprocess
import traceback
import wnck
import re
import psutil
import time

output = sys.stdout

def log(output):
    try:
        window = get_current_window()
        if not window:
            sys.stderr.write('failed to get window\n')
            return True

        format = 'a4'
        output.write("%s %s %s %s %s %s\n" % (
            format, get_ip(), get_ssid(), get_date(),
            get_name(window.get_pid()), window.get_name()))
    except Exception, e:
        traceback.print_exc(file=sys.stderr)

    return True

def get_ssid():
    arg='iwconfig'    
    p = subprocess.Popen(arg, shell=True, stdout=subprocess.PIPE, stderr=None)
    for line in p.communicate():
        if line:
            match = re.search('ESSID:"(.*)"', line)
            if match:
                return match.groups()[0]

    return '-'

def get_name(pid):
    return [ps.name for ps in psutil.get_process_list() if ps.pid == pid][0]

def get_date():
    return time.strftime('%Y/%m/%d-%H:%M', time.localtime())

def get_current_window():
    try:
        return wnck.screen_get_default().get_active_window()
    except AttributeError:
        traceback.print_exc(file=sys.stderr)
        return False

def get_ip():
    #Use ip route list
    try:
        arg = 'ip route list'    
        p = subprocess.Popen(arg, shell=True, stdout=subprocess.PIPE)
        data = p.communicate()
        sdata = data[0].split()
        ipaddr = sdata[ sdata.index('src')+1 ]
        return ipaddr
    except Exception, e:
        traceback.print_exc(file=sys.stderr)
        return '-'

    # netdev = sdata[ sdata.index('dev')+1 ]
    
glib.timeout_add(60 * 1000, log, output) # 60sec
gtk.main()