#!/usr/bin/python
# coding=utf-8

import sys
import re
import time
from subprocess import call, check_output

mapping = {'guigu':['sudo route -n add -net 172.xx.xx.xx/16 192.xx.xx.0',
        'sudo route -n add -net 173.xx.xx.xx/16 192.xx.xx.0'],
    '硅谷内网':['sudo route -n add -net 172.xx.xx.xx/16 192.xx.xx.xx',
        'sudo route -n add -net 173.xx.xx.xx/16 192.xx.xx.x'],
}

def List():
    vpns_string = check_output(["scutil", "--nc", "list"])
    vpns = re.findall('"(.+)"', vpns_string)
    for vpn in vpns:
        print "\t%s" % vpn

def ListAll():
    vpns_string = check_output(["scutil", "--nc", "list"])
    print vpns_string

def Check(vpn_name):
    vpns_string = check_output(["scutil", "--nc", "list"])
    vpns = re.findall('"(.+)"', vpns_string)
    if vpn_name in vpns:
        return True
    else:
        return False

def Status(vpn_name):
    check_r = Check(vpn_name)
    if check_r:
        call(['scutil','--nc','status',vpn_name])
    else:
        print "Invalid vpn name %s!" % vpn_name


def Start(vpn_name):
    check_r = Check(vpn_name)
    if check_r:
        call(["scutil", "--nc", "start", vpn_name])
        if vpn_name in mapping.keys():
            time.sleep(5)
            for command in mapping[vpn_name]:
                call(command.split())
        else:
            print "未添加静态路由!"
    else:
        print "Invalid vpn name %s!" % vpn_name

def Stop(vpn_name):
    check_r = Check(vpn_name)
    if check_r:
        call(["scutil", "--nc", "stop", sys.argv[2]])
    else:
        print "Invalid vpn name %s!" % vpn_name

OPTIONS = {
    'list': List,
    'listall': ListAll,
    'start': Start,
    'stop': Stop,
    'status': Status
}

def main():
    if len(sys.argv) == 2 and sys.argv[1] in ['list','listall']:
        OPTIONS[sys.argv[1]]()
    elif len(sys.argv) == 3 and sys.argv[1] in ['start','stop','status']:
        vpn_name = sys.argv[2]
        OPTIONS[sys.argv[1]](vpn_name)
    else:
        print "Available options:"
        for item in OPTIONS.keys():
            print "\t%s" % item
        sys.exit(0)

if __name__ == "__main__":
    main()
