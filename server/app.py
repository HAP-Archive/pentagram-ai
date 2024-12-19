from flask import (
    Flask,
    request,
    make_response,
    Response,
    jsonify,
    abort,
)
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
