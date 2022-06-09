from views import app
from views.apicommon import token_required
from controllers.pfcontroller import PfController
from controllers import OsController
from flask import request, redirect, url_for, jsonify, make_response
import os

@app.route('/api/v1/pf', methods=['GET'])
@token_required
def pf(current_user):
    pfc = PfController()
    osc = OsController()
    return jsonify({'Hostname' : osc.gethostname()})
