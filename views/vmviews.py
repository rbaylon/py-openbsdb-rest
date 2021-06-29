from views import app
from views.apiviews import token_required
from flask import request, redirect, url_for, jsonify, make_response


@app.route('/api/vm', methods=['GET'])
@token_required
def vms(current_user):
    return jsonify({'Virtual Machines' : ['vm1', 'vm2']})
