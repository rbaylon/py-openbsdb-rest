from controllers import cfg
from models import Users

def _getnextid():
    ids = []
    for u in cfg.cfg['users']:
        ids.append(u['uid'])

    ids.sort()
    return ids[-1] + 1

class UserController(object):
    def getusers(self):
        users = []
        for u in cfg.cfg['users']:
            users.append(Users(u))

        return users

    def getuser(self, username=None, uid=None):
        ok = False
        if username:
            for u in cfg.cfg['users']:
                if u['user'] == username:
                    self.user = u
                    ok = True
                    break

        elif uid:
            for u in cfg.cfg['users']:
                if u['uid'] == uid:
                    self.user = u
                    ok = True
                    break

        if ok:
            return Users(self.user)
        else:
            return None

    def adduser(self, data):
        data['uid'] = _getnextid()
        cfg.cfg['users'].append(data)
        if not cfg.is_lock():
            cfg.lock()
            return cfg.save()
        else:
            return None

    def edituser(self, data, updatepw=False):
        i = 0
        for u in cfg.cfg['users']:
            if u['uid'] == data['uid']:
                if updatepw:
                    cfg.cfg['users'][i]['password'] = data['password']
                else:
                    cfg.cfg['users'][i]['user'] = data['username']
                    cfg.cfg['users'][i]['group'] = data['group']

                break
            i += 1

        if not cfg.is_lock():
            cfg.lock()
            return cfg.save()
        else:
            return None

    def deleteuser(self, data):
        i = 0
        for u in cfg.cfg['users']:
            if u['uid'] == data['uid']:
                cfg.cfg['users'].pop(i)
                break
            i += 1

        if not cfg.is_lock():
            cfg.lock()
            return cfg.save()
        else:
            return None

