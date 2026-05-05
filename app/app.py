from flask import Flask, jsonify, render_template
import psutil
import datetime
import psycopg2
import os

app = Flask(__name__)


def get_db():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'db'),
        database=os.environ.get('DB_NAME', 'healthdb'),
        user=os.environ.get('DB_USER', 'admin'),
        password=os.environ.get('DB_PASSWORD', 'password')
    )

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS health_logs (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP,
            cpu_percent FLOAT,
            memory_percent FLOAT,
            disk_percent FLOAT
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/ping')
def ping():
    return 'ok', 200

@app.route('/api/health')
def health():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    timestamp = datetime.datetime.now()

    # Save to database
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO health_logs (timestamp, cpu_percent, memory_percent, disk_percent) VALUES (%s, %s, %s, %s)',
        (timestamp, cpu, memory, disk)
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        'timestamp': str(timestamp),
        'cpu_percent': cpu,
        'memory': {'percent': memory},
        'disk': {'percent': disk}
    })

@app.route('/api/history')
def history():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT timestamp, cpu_percent, memory_percent, disk_percent FROM health_logs ORDER BY timestamp DESC LIMIT 10')
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([{
        'timestamp': str(r[0]),
        'cpu': r[1],
        'memory': r[2],
        'disk': r[3]
    } for r in rows])

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000) 
