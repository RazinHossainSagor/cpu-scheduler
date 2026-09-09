from flask import Flask, render_template, request, jsonify
from scheduler import (
    fcfs, sjf_non_preemptive, srtf, 
    priority_non_preemptive, priority_preemptive, 
    round_robin, ljf_non_preemptive
)

app = Flask(__name__)

def parse_processes(data):
    processes = []
    for p in data:
        processes.append({
            'id': str(p.get('id', '')),
            'arrival_time': int(p.get('arrival', p.get('arrival_time', 0))),
            'burst_time': int(p.get('burst', p.get('burst_time', 1))),
            'priority': int(p.get('priority', 0))
        })
    return processes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        req_data = request.get_json()
        algo = req_data.get('algorithm')
        raw_processes = req_data.get('processes', [])
        processes = parse_processes(raw_processes)

        if algo == 'FCFS':
            result = fcfs(processes)
        elif algo == 'SJF':
            result = sjf_non_preemptive(processes)
        elif algo == 'SRTF':
            result = srtf(processes)
        elif algo == 'Priority':
            result = priority_non_preemptive(processes)
        elif algo == 'Priority_Preemptive':
            result = priority_preemptive(processes)
        elif algo == 'RR':
            time_quantum = int(req_data.get('time_quantum', 2))
            result = round_robin(processes, time_quantum)
        elif algo == 'LJF':
            result = ljf_non_preemptive(processes)
        else:
            return jsonify({'error': 'Invalid Algorithm'}), 400

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/compare', methods=['POST'])
def compare():
    try:
        req_data = request.get_json()
        algorithms = req_data.get('algorithms', [])
        raw_processes = req_data.get('processes', [])
        processes = parse_processes(raw_processes)

        comparison_results = []
        for algo in algorithms:
            res = None
            if algo == 'FCFS':
                res = fcfs(processes)
            elif algo == 'SJF':
                res = sjf_non_preemptive(processes)
            elif algo == 'SRTF':
                res = srtf(processes)
            elif algo == 'Priority':
                res = priority_non_preemptive(processes)
            elif algo == 'Priority_Preemptive':
                res = priority_preemptive(processes)
            elif algo == 'RR':
                res = round_robin(processes, 2)
            elif algo == 'LJF':
                res = ljf_non_preemptive(processes)

            if res:
                res['algorithm'] = algo
                comparison_results.append(res)

        return jsonify(comparison_results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)