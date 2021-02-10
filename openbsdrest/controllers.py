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
from Utils.utils import CfgManager, AF
from openbsdrest import app

cfg = CfgManager(app.config['OPENBSD_CONFIG'])

def _build_error(e):
    error = {}
    error['Error'] = e
    return error

class InterfaceController(object):
    def __init__(self):
        self.ifaces = cfg.cfg['interfaces']

    def getinterfaces(self):
        return self.ifaces

    def getifaddresses(self, iface, af=None):
        if af:
            try:
                return self.ifaces[iface][str(af)]
            except:
                return _build_error('AF {} or interface {} not found.'.format(AF[af], iface))
        else:
            try:
                return self.ifaces[iface]
            except:
                return _build_error('Interface {} not found.'.format(iface))

    def addifaddr(self, iface, data, af):
        cfg.cfg['interfaces'][iface][str(af)].append(data)
        if not cfg.is_lock():
            cfg.lock()
            return cfg.save()
        else:
            return 'CONFIG LOCK'

    def delifaddr(self, iface, data, af):
        cfg.cfg['interfaces'][iface][str(af)].pop(data['index'])
        if not cfg.is_lock():
            cfg.lock()
            return cfg.save()
        else:
            return 'CONFIG LOCK'

    def modifaddr(self, iface, data, af):
        cfg.cfg['interfaces'][iface][str(af)][data['index']] = data['value']
        if not cfg.is_lock():
            cfg.lock()
            return cfg.save()
        else:
            return 'CONFIG LOCK'

class OsController(object):
    def __init__(self):
        self.hostname = cfg.cfg['hostname']

    def gethostname(self):
        return self.hostname

    def sethostname(self):
        pass
