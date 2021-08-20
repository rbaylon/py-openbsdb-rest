"""
Copyright (c) 2021 Ricardo Baylon rbaylon@outlook.com

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""
import os, netifaces, json, subprocess
from socket import gethostname
from Utils.variables import SIFS
from werkzeug.security import generate_password_hash


class CfgManager(object):
    def __init__(self, cfg):
        self.cfgfile = cfg
        self.lockfile = '{}.lock'.format(cfg)
        if os.path.isfile(cfg):
            with open(cfg, "r") as rfile:
                self.cfg = json.load(rfile)

        else:
            #get working dir so that we can execute our shell script
            wdir = os.path.dirname(__file__)
            newcfg = {}
            ifaces = {}
            for i in netifaces.interfaces():
                if i in SIFS:
                    continue

                ifaces[i] = netifaces.ifaddresses(i)
                try:
                    j=0
                    for ip in ifaces[i][netifaces.AF_INET]:
                        addr = ip['addr']
                        out = subprocess.Popen(
                            ['Utils/sh/getNetmask.sh', i, addr],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT
                        )
                        stdout,stderr = out.communicate()
                        netmask = stdout.decode()
                        ifaces[i][netifaces.AF_INET][j]['netmask'] = netmask
                        ifaces[i][netifaces.AF_INET][j]['broadcast'] = ''
                        j+=1

                except Exception as e:
                    print(e)

            newcfg['interfaces'] = ifaces
            newcfg['hostname'] = gethostname()
            default_password = generate_password_hash('123*45',
                                                      method='pbkdf2:sha256:260000',
                                                      salt_length=16
                                                     )
            newcfg['users'] = [
                {'user': 'admin',
                 'password': default_password,
                 'group': 'admin',
                 'uid': 1},
            ]
            with open(cfg, "w") as wfile:
                json.dump(newcfg, wfile, indent=4,sort_keys=True)

            with open(cfg, "r") as rfile:
                self.cfg = json.load(rfile)

    def save(self):
        try:
            with open(self.lockfile, "r") as lockfile:
                self.cfg = json.load(lockfile)

            os.rename(self.cfgfile,'{}.old'.format(self.cfgfile))
            os.rename(self.lockfile, self.cfgfile)
            return True
        except Exception as e:
            return str(e)

    def lock(self):
        with open(self.lockfile, "w") as lockfile:
            json.dump(self.cfg, lockfile, indent=4, sort_keys=True)

    def unlock(self):
        if os.path.isfile(self.lockfile):
            os.remove(self.lockfile)
            return True

        return False

    def is_lock(self):
        if os.path.isfile(self.lockfile):
            return True
        else:
            return False
