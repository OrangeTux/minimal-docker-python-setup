from flask import Flask, request, jsonify
from flask.ext.redis import FlaskRedis

app = Flask(__name__)
app.config.update(
    REDIS_URL="redis://redis:6379/0"
)

redis_store = FlaskRedis(app)


@app.route('/')
def index():
    addr = request.remote_addr
    redis_store.incr(addr)
    visits = redis_store.get(addr)

    return jsonify({
        'ip': addr,
        'visits': visits,
    })
