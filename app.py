from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# 初始化数据库
def init_db():
    with sqlite3.connect('warehouse.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS devices (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL UNIQUE,
                     quantity INTEGER NOT NULL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS records (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     device_id INTEGER,
                     operation TEXT NOT NULL,
                     quantity INTEGER NOT NULL,
                     operator TEXT NOT NULL,
                     timestamp TEXT NOT NULL,
                     source_destination TEXT,
                     FOREIGN KEY (device_id) REFERENCES devices(id))''')
        conn.commit()

# API 端点 - 库存概览
@app.route('/api/index')
def api_index():
    with sqlite3.connect('warehouse.db') as conn:
        c = conn.cursor()
        c.execute('SELECT id, name, quantity FROM devices')
        devices = c.fetchall()
    return render_template('index_content.html', devices=devices)

# API 端点 - 添加设备
@app.route('/api/add_device', methods=['GET', 'POST'])
def api_add_device():
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        with sqlite3.connect('warehouse.db') as conn:
            c = conn.cursor()
            try:
                c.execute('INSERT INTO devices (name, quantity) VALUES (?, ?)', (name, quantity))
                conn.commit()
            except sqlite3.IntegrityError:
                return jsonify({'status': 'error', 'message': '设备名称已存在！'}), 400
        return jsonify({'status': 'success', 'message': '添加成功'})
    return render_template('add_device_content.html')

# API 端点 - 出入库操作
@app.route('/api/operation', methods=['GET', 'POST'])
def api_operation():
    with sqlite3.connect('warehouse.db') as conn:
        c = conn.cursor()
        c.execute('SELECT id, name FROM devices')
        devices = c.fetchall()
    if request.method == 'POST':
        device_id = int(request.form['device_id'])
        operation_type = request.form['operation']
        quantity = int(request.form['quantity'])
        operator = request.form['operator']
        source_destination = request.form['source_destination']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with sqlite3.connect('warehouse.db') as conn:
            c = conn.cursor()
            c.execute('SELECT quantity FROM devices WHERE id = ?', (device_id,))
            current_quantity = c.fetchone()[0]
            
            if operation_type == 'out' and current_quantity < quantity:
                return jsonify({'status': 'error', 'message': '库存不足！'}), 400
            
            new_quantity = current_quantity + quantity if operation_type == 'in' else current_quantity - quantity
            c.execute('UPDATE devices SET quantity = ? WHERE id = ?', (new_quantity, device_id))
            c.execute('INSERT INTO records (device_id, operation, quantity, operator, timestamp, source_destination) VALUES (?, ?, ?, ?, ?, ?)',
                      (device_id, operation_type, quantity, operator, timestamp, source_destination))
            conn.commit()
        return jsonify({'status': 'success', 'message': '操作成功'})
    return render_template('operation_content.html', devices=devices)

# API 端点 - 操作历史
@app.route('/api/history')
def api_history():
    with sqlite3.connect('warehouse.db') as conn:
        c = conn.cursor()
        c.execute('''SELECT r.id, d.name, r.operation, r.quantity, r.operator, r.timestamp, r.source_destination 
                     FROM records r JOIN devices d ON r.device_id = d.id 
                     ORDER BY r.timestamp DESC''')
        records = c.fetchall()
    return render_template('history_content.html', records=records)

# 主页面
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001, debug=False, threaded=False)