from flask import Blueprint

bp = Blueprint('detect', __name__)

from app.detect import routes
from app.detect import run_model_server
run_model_server = run_model_server.pre_load_model()
