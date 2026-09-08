from flask import Flask, render_template, request, jsonify
from scheduler import (
    run_fcfs, run_sjf, run_priority, 
    run_srtf, run_priority_preemptive, 
    run_round_robin, run_ljf_non_preemptive, run_ljf_preemptive
)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def execute_algorithm(algo, processes):
    if algo == 'FCFS':
        return run_fcfs(processes)
    elif algo == 'SJF':
        return run_sjf(processes)
    elif algo == 'Priority':
        return run_priority(processes)
    elif algo in ['SRTF', 'srtf']:
        return run_srtf(processes)
    elif algo in ['Priority_Preemptive', 'priority_preemptive']:
        return run_priority_preemptive(processes)
    elif algo in ['RR', 'rr', 'Round_Robin']:
        return run_round_robin(processes)
    elif algo in ['LJF', 'ljf_non_preemptive']:
        return run_ljf_non_preemptive(processes)
    elif algo in ['LRTF', 'ljf_preemptive']:
        return run_ljf_preemptive(processes)
    else:
        return run_fcfs(processes)

@app.route('/api/simulate', methods=['POST'])
def simulate():
    data = request.json
    algorithm = data.get('algorithm')
    processes = data.get('processes', [])

    result = execute_algorithm(algorithm, processes)
    return jsonify(result)

@app.route('/api/compare', methods=['POST'])
def compare():
    data = request.json
    algorithms = data.get('algorithms', [])
    processes = data.get('processes', [])

    results = {}
    for algo in algorithms:
        results[algo] = execute_algorithm(algo, processes)

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)