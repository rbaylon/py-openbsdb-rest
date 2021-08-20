from flask_login import UserMixin

class Users(UserMixin):
    def __init__(self, user=None):
        if not user:
            return None

        self.username = user['user']
        self.password = user['password']
        self.group = user['group']
        self.id = user['uid']
