from flask import Flask, render_template
import redis
import time
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.logger.info("Flask App Started")
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return render_template('index.html', count=count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
