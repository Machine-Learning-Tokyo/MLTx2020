from flask import redirect, url_for, request, render_template, flash
from app.main import bp
from flask import current_app as app

@bp.route('/', methods=['GET'])
def index():
    return "Hello"



