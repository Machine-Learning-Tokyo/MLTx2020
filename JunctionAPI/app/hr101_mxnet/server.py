from flask import Flask
from constant import Constant
from controller.face_features import api_face_features

# initialize Flask app
app = Flask(__name__)

app.register_blueprint(api_face_features, url_prefix='/face_features')


if __name__ == '__main__':
    # app.run(host=Constant.API_HOST, port=Constant.API_PORT, debug=False, use_reloader=False)
    # app.run(host='0.0.0.0', port=80, debug=False, use_reloader=False)
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
