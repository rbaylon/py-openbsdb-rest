from flask import Flask
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
project_path = os.path.dirname(dir_path)
app = Flask(__name__)
app.config.from_pyfile('{}/config/config.cfg'.format(project_path))

from views import apiviews, vmviews
