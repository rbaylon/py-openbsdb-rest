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
from openbsdrest import app
from flask import request, redirect, url_for, jsonify, make_response
import jwt
import datetime
from functools import wraps
from bsdauth.bsdauth import UserOkay
from Utils.utils import Validator

v = Validator()

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
            return jsonify({'message' : str(e)}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/api/login')
def apilogin():
    auth = request.authorization
    if not auth or not auth.username:
        return make_response('Username required!', 401, {'WWW-Authenticate' : 'Basic realm="Username required!"'})

    if not auth.password:
        return make_response('Password required!', 401, {'WWW-Authenticate' : 'Basic realm="Password required!"'})

    if v.is_username_valid(auth.username) and v.is_password_valid(auth.password):
        credential = UserOkay(auth.username, auth.password)
        if credential.login():
            token = jwt.encode({'username' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
            return jsonify({ 'token' : token })

    return make_response('Invalid user or password!', 401, {'WWW-Authenticate' : 'Basic realm="Invalid user!"'})


@app.route('/api', methods=['GET'])
@token_required
def home(current_user):
    return jsonify({'Hello' : current_user})
