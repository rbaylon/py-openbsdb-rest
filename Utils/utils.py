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
import re, os, netifaces, json
from socket import gethostname

AF = {
    netifaces.AF_INET : 'inet',
    netifaces.AF_INET6 : 'inet6',
    netifaces.AF_LINK : 'mac'
}

class Validator(object):
    def is_username_valid(self, username):
        """
           Validate username based on OpenBSD's passwd(5) username specs.
        """
        if re.search('^[a-z]+[0-9|\-|_|a-z]+$', username) and len(username) <= 31:
            return True
        else:
            return False

    def is_password_valid(self, password):
        """
           Validate password based on OpenBSD's passwd(1) password specs.
        """
        if len(password) >= 6 and len(password) <= 128:
            return True
        else:
            return False

class CfgManager(object):
    def __init__(self, cfg):
        if os.path.isfile(cfg):
            with open(cfg, "r") as rfile:
                self.cfg = json.load(rfile)

        else:
            newcfg = {}
            ifaces = {}
            for i in netifaces.interfaces():
                ifaces[i] = netifaces.ifaddresses(i)

            newcfg['interfaces'] = ifaces
            newcfg['hostname'] = gethostname()
            with open(cfg, "w") as wfile:
                json.dump(newcfg, wfile)

            with open(cfg, "r") as rfile:
                self.cfg = json.load(rfile)

    def gethostname(self):
        return self.cfg['hostname']

    def getinterfaces(self):
        return self.cfg['interfaces']

