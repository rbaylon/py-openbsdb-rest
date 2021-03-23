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
from views import app
from flask import request, redirect, url_for, jsonify, make_response
import jwt
import datetime
from functools import wraps
from bsdauth.bsdauth import UserOkay
from Utils.variables import AF, IP
from Utils.validators import AccountValidator, IpValidator
import netifaces
from controllers import InterfaceController, OsController
from ipaddress import IPv4Interface

av = AccountValidator()
ipv = IpValidator()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message' : 'Token is missing!'}), 401

        else:
            return jsonify({'message' : 'Authorization required!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['username']
        except Exception as e:
            return jsonify({'message' : 'Token failed {}'.format(str(e))}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/api/login')
def apilogin():
    auth = request.authorization
    if not auth or not auth.username:
        return make_response('Username required!', 401, {'WWW-Authenticate' : 'Basic realm="Username required!"'})

    if not auth.password:
        return make_response('Password required!', 401, {'WWW-Authenticate' : 'Basic realm="Password required!"'})

    if av.is_username_valid(auth.username) and av.is_password_valid(auth.password):
        credential = UserOkay(auth.username, auth.password)
        if credential.login():
            token = jwt.encode({'username' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
            return jsonify({ 'token' : token })

    return make_response('Invalid user or password!', 401, {'WWW-Authenticate' : 'Basic realm="Invalid user!"'})


@app.route('/api', methods=['GET'])
@token_required
def home(current_user):
    osc = OsController()
    return jsonify({'Hostname' : osc.gethostname()})

@app.route('/api/interfaces', methods=['GET'])
@token_required
def interfaces(current_user):
    ic = InterfaceController()
    return jsonify({'interfaces' : ic.getinterfaces()})

@app.route('/api/interfaces/<iface>', defaults={'af': 'all', 'index': '0'}, methods=['GET'])
@app.route('/api/interfaces/<iface>/<af>', defaults={'index': 'all'}, methods=['GET', 'POST'])
@app.route('/api/interfaces/<iface>/<af>/<string:index>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def iface_addr(current_user, iface, af, index):
    if af != 'all':
        oldaf = af
        if af == 'inet':
            af = netifaces.AF_INET
        elif af == 'inet6':
            af = netifaces.AF_INET6
        elif af == 'mac':
            af = netifaces.AF_LINK
        else:
            return jsonify({
                'Error' : 'Invalid AF {}'.format(af),
                'Valid Options' : 'inet, inet6, mac'
            }), 400

    ic = InterfaceController()

    if request.method == 'GET':
        if af == 'all':
            cfgdata = ic.getifaddresses(iface)
        else:
            if index:
                cfgdata = ic.getifaddresses(iface, af, index)
            else:
                cfgdata = ic.getifaddresses(iface, af)

        return jsonify(cfgdata)

    if request.method == 'POST':
        """
            JSON input format:
            {"addr": "192.168.254.100", "netmask": "255.255.255.0"}
        """
        cfgdata = ic.getinterface(iface)
        if 'Failed' in cfgdata:
            return jsonify(cfgdata), 400

        if request.is_json:
            data = request.get_json()
            for key in data:
                if key not in IP['interface_keys']:
                    return jsonify({'Error' : 'invalid paramter {}'.format(key)}), 400
        else:
            return jsonify({'Error' : 'Request must be application/json'}), 400

        if oldaf in AF.values():
            inetaddr = ic.getifaddresses(iface, af)
            if AF[af] == 'inet' or AF[af] == 'inet6':
                if 'Failed' in inetaddr:
                    # assume interface has no ip
                    iip = ipv.isIpInterface(data['addr'], data['netmask'])
                    if iip['status']:
                        ret = ic.addifaf(iface, data, af)
                        if type(ret) != 'str':
                            return redirect(url_for('iface_addr', iface=iface, af=AF[af]))
                        else:
                            return jsonify({'Error' : 'Failed to add address: {}'.format(ret)}), 400
                    else:
                        return jsonify({'Error' : '{}'.format(iip['interface'])}), 400
                else:
                    # assume vip addition
                    for i in inetaddr:
                        if i['netmask'] != '255.255.255.255' or i['netmask'] != '32':
                            interface = IPv4Interface('{}/{}'.format(i['addr'],i['netmask']))
                            break

                    iip = ipv.isIpInterface(data['addr'], '255.255.255.255')
                    if iip['status']:
                        if ipv.isIpInNetwork(iip['interface'].ip, interface.network):
                            data['netmask'] = '255.255.255.255'
                            ret = ic.addifaddr(iface, data, af)
                            if type(ret) != 'str':
                                return redirect(url_for('iface_addr', iface=iface, af=AF[af]))
                            else:
                                return jsonify({'Error' : 'Failed to add address: {}'.format(ret)}), 400
                        else:
                            return jsonify({'Error' : 'Failed to add address: {}. Outside of subnet {}'.format(iip['interface'].ip, interface.network)}), 400
                    else:
                        return jsonify({'Error' : '{}'.format(iip['interface'])}), 400

            elif AF[af] == 'inet6':
                    pass
            elif AF[af] == 'mac':
                    pass


    if request.method == 'DELETE':
        """
            Valid input { 'confirm_delete': 'yes' }
        """
        if request.is_json:
            data = request.get_json()
        else:
            return jsonify({'Error' : 'Request must be application/json'}), 400

        for key in data:
            if key not in IP['delete_keys']:
                return jsonify({'Error' : 'Invalid delete key: {}'.format(key)}), 400

        ret = ic.delifaddr(iface, data, af, index)
        if type(ret) != 'str':
            return redirect(url_for('iface_addr', iface=iface, af=AF[af]))
        else:
            return jsonify({'Error' : 'Failed to add address: {}'.format(ret)}), 400

    if request.method == 'PUT':
        """
            Valid input {"addr": "192.168.254.100", "netmask": "255.255.255.0"}
        """
        if request.is_json:
            data = request.get_json()
        else:
            return jsonify({'Error' : 'Request must be application/json'}), 400

        for key in data:
            if key not in IP['interface_keys']:
                return jsonify({'Error' : 'Invalid update key: {}'.format(key)}), 400

        iip = ipv.isIpInterface(data['addr'], data['netmask'])
        if iip['status']:
            if ic.isifipindex(iface, af, index):
                inetaddr = ic.getifaddresses(iface, af, index)
                interface = IPv4Interface('{}/{}'.format(inetaddr['addr'],inetaddr['netmask']))
                if ipv.isIpInNetwork(iip['interface'].ip, interface.network):
                    ret = ic.modifaddr(iface, data, af, index)
                    if type(ret) != 'str':
                        return redirect(url_for('iface_addr', iface=iface, af=AF[af]))
                    else:
                        return jsonify({'Error' : 'Failed to add address {}'.format(ret)}), 400
                else:
                    return jsonify({'Error' : 'Failed to update address: {}. Outside of subnet {}'.format(data['addr'], interface.network)}), 400
            else:
                return jsonify({'Error' : 'Invalid index {}'.format(index)}), 400
        else:
            return jsonify({'Error' : '{}'.format(iip['interface'])}), 400


