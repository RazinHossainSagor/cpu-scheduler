from flask import Flask, render_template, request, jsonify
import scheduler

app = Flask(__name__)

def parse_processes(data):
    processes = []
    for p in data:
        processes.append({
            'id': str(p.get('id', '')),
            'arrival_time': int(p.get('arrival', p.get('arrival_time', 0))),
            'burst_time': int(p.get('burst', p.get('burst_time', 1))),
            'priority': int(p.get('priority', 0)),
            'arrival': int(p.get('arrival', p.get('arrival_time', 0))),
            'burst': int(p.get('burst', p.get('burst_time', 1)))
        })
    return processes

def get_scheduler_func(func_name):
    return getattr(scheduler, func_name, None)

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

        algo_map = {
            'FCFS': ['fcfs', 'first_come_first_serve', 'fcfs_scheduling'],
            'SJF': ['sjf', 'sjf_non_preemptive', 'shortest_job_first'],
            'SRTF': ['srtf', 'sjf_preemptive', 'shortest_remaining_time_first'],
            'Priority': ['priority', 'priority_non_preemptive', 'priority_scheduling'],
            'Priority_Preemptive': ['priority_preemptive', 'preemptive_priority'],
            'RR': ['rr', 'round_robin', 'round_robin_scheduling'],
            'LJF': ['ljf', 'ljf_non_preemptive', 'longest_job_first'],
            'LRTF': ['lrtf', 'ljf_preemptive', 'longest_remaining_time_first']
        }

        func_names = algo_map.get(algo, [])
        target_func = None

        for name in func_names:
            target_func = get_scheduler_func(name)
            if target_func:
                break

        if not target_func:
            return jsonify({'error': f'Algorithm function for {algo} not found'}), 400

        if algo == 'RR':
            try:
                result = target_func(processes, 2)
            except TypeError:
                result = target_func(processes)
        else:
            result = target_func(processes)

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

        algo_map = {
            'FCFS': ['fcfs', 'first_come_first_serve', 'fcfs_scheduling'],
            'SJF': ['sjf', 'sjf_non_preemptive', 'shortest_job_first'],
            'SRTF': ['srtf', 'sjf_preemptive', 'shortest_remaining_time_first'],
            'Priority': ['priority', 'priority_non_preemptive', 'priority_scheduling'],
            'Priority_Preemptive': ['priority_preemptive', 'preemptive_priority'],
            'RR': ['rr', 'round_robin', 'round_robin_scheduling'],
            'LJF': ['ljf', 'ljf_non_preemptive', 'longest_job_first'],
            'LRTF': ['lrtf', 'ljf_preemptive', 'longest_remaining_time_first']
        }

        comparison_results = []
        for algo in algorithms:
            func_names = algo_map.get(algo, [])
            target_func = None
            for name in func_names:
                target_func = get_scheduler_func(name)
                if target_func:
                    break

            if target_func:
                if algo == 'RR':
                    try:
                        res = target_func(processes, 2)
                    except TypeError:
                        res = target_func(processes)
                else:
                    res = target_func(processes)

                if res:
                    res['algorithm'] = algo
                    comparison_results.append(res)

        return jsonify({'results': comparison_results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)