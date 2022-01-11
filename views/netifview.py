from views import app
from flask_login import login_required
from flask import render_template, request, redirect, url_for, abort
from controllers import InterfaceController
import netifaces


@app.route('/system/interfaces/<iface>', methods=['GET'])
@login_required
def netif(iface):
    ic = InterfaceController()
    addrs = ic.getifaddresses(iface)
    app.logger.info(addrs)
    if 'Failed' in addrs:
        iface = "{} not found".format(iface)

    try:
        ipv4s = addrs[str(netifaces.AF_INET)]
    except:
        ipv4s = []

    try:
        ipv6s = addrs[str(netifaces.AF_INET6)]
    except:
        ipv6s = []

    ips = []
    for ip in ipv4s:
        ips.append(ip)

    for ip6 in ipv6s:
        ips.append(ip6)

    return render_template('netif.html', iface=iface, ips=ips)
