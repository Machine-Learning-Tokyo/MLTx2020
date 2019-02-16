from flask import Flask, request, current_app
from flask_bootstrap import Bootstrap
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, \
     patch_request_class
from flask_wtf.csrf import CSRFProtect
from config import Config

bootstrap = Bootstrap()
dropzone = Dropzone()
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    bootstrap.init_app(app)
    dropzone.init_app(app)
    csrf.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.detect import bp as detect_bp
    app.register_blueprint(detect_bp)

    return app
