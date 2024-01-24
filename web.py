from flask import Flask
from nad_ch.config import WEB_PORT


app = Flask(__name__)


@app.route('/')
def home():
    return 'Welcome to the NAD Collaboration Hub'


def main():
    app.run(host='0.0.0.0', port=int(WEB_PORT))


if __name__ == '__main__':
    main()
