from flask import Flask, render_template, request, jsonify
from scheduler import run_fcfs, run_sjf, run_priority

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/simulate', methods=['POST'])
def simulate():
    data = request.json
    algorithm = data.get('algorithm')
    processes = data.get('processes', [])

    if algorithm == 'FCFS':
        result = run_fcfs(processes)
    elif algorithm == 'SJF':
        result = run_sjf(processes)
    elif algorithm == 'Priority':
        result = run_priority(processes)
    else:
        result = run_fcfs(processes)

    return jsonify(result)

@app.route('/api/compare', methods=['POST'])
def compare():
    data = request.json
    algorithms = data.get('algorithms', [])
    processes = data.get('processes', [])

    results = {}
    for algo in algorithms:
        if algo == 'FCFS':
            results['FCFS'] = run_fcfs(processes)
        elif algo == 'SJF':
            results['SJF'] = run_sjf(processes)
        elif algo == 'Priority':
            results['Priority'] = run_priority(processes)

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)