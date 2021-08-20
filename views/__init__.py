from flask import Flask
import os
from flask_bootstrap import Bootstrap
from Utils.errorhandlers import page_not_found, unauthorized

dir_path = os.path.dirname(os.path.realpath(__file__))
project_path = os.path.dirname(dir_path)
app = Flask(__name__)
app.config.from_pyfile('{}/config/config.cfg'.format(project_path))
app.register_error_handler(404, page_not_found)
app.register_error_handler(401, unauthorized)
Bootstrap(app)

from views import apiviews, vmviews, webviewcommon
