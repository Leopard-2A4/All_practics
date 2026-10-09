from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)
logs = []


@app.route('/logs', methods=['POST'])
def receive_logs():
    """Принимает ЛЮБЫЙ формат от HTTPHandler"""
    if request.is_json:
        log_data = request.json
    else:
        log_data = request.form.to_dict()
        if 'json' in log_data:
            import json
            log_data = json.loads(log_data['json'])

    logs.append({
        'timestamp': datetime.now().isoformat(),
        'data': log_data,
        'source': request.remote_addr
    })

    print(f"Получен лог: {log_data.get('name', 'unknown')} - {log_data.get('message', '')[:50]}")
    return jsonify({'status': 'received', 'count': len(logs)}), 200


@app.route('/logs', methods=['GET'])
def get_logs():
    return jsonify({'logs': logs[-20:], 'total': len(logs)})


if __name__ == '__main__':
    print("Log Collector: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
