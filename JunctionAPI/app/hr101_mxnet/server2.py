#!/home/paperspace/anaconda3/bin/python
from flask import Flask
app = Flask(__name__)


@app.route('/', methods=['POST'])

def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)
