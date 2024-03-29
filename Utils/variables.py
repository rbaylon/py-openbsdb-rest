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

import netifaces

AF = {
    netifaces.AF_INET : 'inet',
    netifaces.AF_INET6 : 'inet6',
    netifaces.AF_LINK : 'mac'
}

SIFS = [
    'enc0',
    'pflog0'
]

IP = {}
IP['interface_keys'] = ['addr', 'netmask']
IP['delete_keys'] = ['confirm_delete']
IP['update_keys'] = ['index','value']

groups = [
    ('admin', 'Admin'),
    ('viewer', 'Viewer')
]


pf = {
    'action': [
        ('pass', 'pass'),
        ('block', 'block'),
        ('match', 'match')
    ],
    'direction': [
        ('in', 'inbound'),
        ('out', 'outbound'),
        ('any', 'any')
    ],
    'log': False,
    'quick': False,
    'on': ["replace with an array of combined interface and rdomain numbers"],
    'af':[
        ('any', 'any'),
        ('inet', 'ipv4'),
        ('inet6', 'ipv6')
    ],
    'protospec': ["replace with protocols in /etc/services"],
    'hosts': {
        'from': {
            'host': 'input field',
            'port': 'input field'
        },
        'to':{
            'host': 'input field',
            'port': 'input field'
        }
    }
}
