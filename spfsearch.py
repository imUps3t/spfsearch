#!/usr/bin/python3
import requests
import sys
import socket
import json
import os

from pip._vendor.distlib.compat import raw_input

ascii_art =  " __                 _____                                  .__      __   \n" +  "  / /   _____________/ ____\\______ ____ _____ _______   ____ |  |__   \\ \\  \n" +   " / /   /  ___/\\____ \\   __\\/  ___// __ \\\\__  \\\\_  __ \\_/ ___\\|  |  \\   \\ \\ \n" +   " \\ \\   \\___ \\ |  |_> >  |  \\___ \\\\  ___/ / __ \\|  | \\/\\  \\___|   Y  \\  / / \n" +  "  \\_\\ /____  >|   __/|__| /____  >\\___  >____  /__|    \\___  >___|  / /_/  \n" +     "           \\/ |__|             \\/     \\/     \\/            \\/     \\/"

loads = ''

scriptname = os.path.basename(sys.argv[0])

def query_yes_no(question, default="yes"):
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n]: "
    elif default == "yes":
        prompt = " [Y/n]: "
    elif default == "no":
        prompt = " [y/N]: "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("[SPFsearch] You must enter \"y\" (yes) or \"n\" (no)! \n")


def search(domain):
    spf = requests.get('https://dmarcly.com/server/spf_check.php?domain=' + domain)
    loads = json.loads(spf.content)

    if loads['code'] == 'success':
        txt = json.loads(json.dumps(loads['record']))['txt']

        print("[SPFsearch] This website/domain is secure with SPF! [" + json.loads(spf.content)['code'] + "]")
        check = query_yes_no('[SPFsearch] Would you like to check the TXT record?', default='no')

        if check:
            print('[SPFsearch] SPF TXT Records: ')
            print(txt)
        if not check:
            exit(0)
    else:
        print("[SPFsearch] This website/domain is insecure (No SPF!) [" + json.loads(spf.content)['code'] + "]")


print(ascii_art)

print('\n - by ups3t <3')

try:
    socket.gethostbyname('dmarcly.com')
except socket.gaierror:
    print("[SPFsearch] Error > https://dmarcly.com is currently not available :(")
    exit(1)

arg_count = len(sys.argv)

if arg_count != 2:
    print("[SPFsearch] Error > Type " + scriptname + " <domain> to check for an SPF record.")
else:
    print("[SPFsearch] Searching for SPF record at " + sys.argv[1] + "..")
    search(sys.argv[1])