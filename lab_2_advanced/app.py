import time
import redis
from flask import Flask

app = Flask(__name__)
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
    # HTML и CSS для стилизации страницы с бледно-розовым фоном
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome</title>
        <style>
            body {{
                background-color: #ffe4e1; /* бледно-розовый цвет фона */
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                font-family: Arial, sans-serif;
            }}
            .content {{
                text-align: center;
                background-color: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }}
            h1 {{
                font-size: 24px;
                color: #333;
            }}
        </style>
    </head>
    <body>
        <div class="content">
            <h1>Обновляя эту страницу, ты тапаешь хомяка 🐹</h1>
            <h2>Твоих тапов: {count}</h2>
        </div>
    </body>
    </html>
    """

if name == '__main__':
    app.run(host='0.0.0.0')
