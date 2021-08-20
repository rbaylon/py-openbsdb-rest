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
import re, ipaddress
from wtforms.validators import ValidationError


class AccountValidator(object):
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

class FormAccountValidator(object):
    def __init__(self, opt=None):
        self.umessage = """
            The login name may be 4 to 31 characters long. Login name
            should start with a letter and consist solely of letters,
            numbers, dashes and underscores.  The login name must
            never begin with a dash (‘-’); also, it is strongly suggested that
            neither uppercase characters nor dots (‘.’) be part of the name.
            No field may contain a colon.
        """
        self.pwmessage = """
        Password must be greater than or equal to 6 characters
        long but not morethan 128 characters
        """
        self.opt = opt

    def __call__(self, form, field):
        av = AccountValidator()
        if self.opt == 'password':
            if not av.is_password_valid(field.data):
                raise ValidationError(self.pwmessage)
        elif self.opt == 'user':
            if not av.is_username_valid(field.data):
                 raise ValidationError(self.umessage)

class IpValidator(object):
    def isIpInterface(self, ip, netmask):
        """ 
            both ip and network must be string
        """
        ret = {}
        try:
           ifaceaddr = ipaddress.IPv4Interface("{}/{}".format(ip,netmask))
           ret['status'] = True
           ret['interface'] = ifaceaddr
           return ret
        except Exception as e:
           ret['status'] = False
           ret['interface'] = str(e)
           return ret

    def isIpInNetwork(self, ip, network):
        """ 
            ip must be an IPv4Address object
            network must be an IPv4Network object
        """
        return ip in network.hosts()


