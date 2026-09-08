def run_fcfs(processes):
    procs = [p.copy() for p in processes]
    procs.sort(key=lambda x: x['arrival_time'])
    current_time = 0
    gantt_chart = []
    completed = []

    for p in procs:
        if current_time < p['arrival_time']:
            gantt_chart.append({
                'process_id': 'Idle',
                'start': current_time,
                'end': p['arrival_time']
            })
            current_time = p['arrival_time']

        start_time = current_time
        completion_time = start_time + p['burst_time']
        turnaround_time = completion_time - p['arrival_time']
        waiting_time = turnaround_time - p['burst_time']

        gantt_chart.append({
            'process_id': p['id'],
            'start': start_time,
            'end': completion_time
        })

        completed.append({
            'id': p['id'],
            'arrival_time': p['arrival_time'],
            'burst_time': p['burst_time'],
            'priority': p.get('priority', 0),
            'completion_time': completion_time,
            'turnaround_time': turnaround_time,
            'waiting_time': waiting_time
        })

        current_time = completion_time

    return calculate_metrics(completed, gantt_chart)

def run_sjf(processes):
    procs = [p.copy() for p in processes]
    n = len(procs)
    completed = []
    gantt_chart = []
    current_time = 0
    is_completed = [False] * n

    while len(completed) < n:
        idx = -1
        min_burst = float('inf')
        for i in range(n):
            if procs[i]['arrival_time'] <= current_time and not is_completed[i]:
                if procs[i]['burst_time'] < min_burst:
                    min_burst = procs[i]['burst_time']
                    idx = i

        if idx != -1:
            p = procs[idx]
            start_time = current_time
            completion_time = start_time + p['burst_time']
            turnaround_time = completion_time - p['arrival_time']
            waiting_time = turnaround_time - p['burst_time']

            gantt_chart.append({
                'process_id': p['id'],
                'start': start_time,
                'end': completion_time
            })

            completed.append({
                'id': p['id'],
                'arrival_time': p['arrival_time'],
                'burst_time': p['burst_time'],
                'priority': p.get('priority', 0),
                'completion_time': completion_time,
                'turnaround_time': turnaround_time,
                'waiting_time': waiting_time
            })

            is_completed[idx] = True
            current_time = completion_time
        else:
            gantt_chart.append({
                'process_id': 'Idle',
                'start': current_time,
                'end': current_time + 1
            })
            current_time += 1

    return calculate_metrics(completed, gantt_chart)

def run_priority(processes):
    procs = [p.copy() for p in processes]
    n = len(procs)
    completed = []
    gantt_chart = []
    current_time = 0
    is_completed = [False] * n

    while len(completed) < n:
        idx = -1
        min_priority = float('inf')
        for i in range(n):
            if procs[i]['arrival_time'] <= current_time and not is_completed[i]:
                if procs[i].get('priority', 0) < min_priority:
                    min_priority = procs[i].get('priority', 0)
                    idx = i

        if idx != -1:
            p = procs[idx]
            start_time = current_time
            completion_time = start_time + p['burst_time']
            turnaround_time = completion_time - p['arrival_time']
            waiting_time = turnaround_time - p['burst_time']

            gantt_chart.append({
                'process_id': p['id'],
                'start': start_time,
                'end': completion_time
            })

            completed.append({
                'id': p['id'],
                'arrival_time': p['arrival_time'],
                'burst_time': p['burst_time'],
                'priority': p.get('priority', 0),
                'completion_time': completion_time,
                'turnaround_time': turnaround_time,
                'waiting_time': waiting_time
            })

            is_completed[idx] = True
            current_time = completion_time
        else:
            gantt_chart.append({
                'process_id': 'Idle',
                'start': current_time,
                'end': current_time + 1
            })
            current_time += 1

    return calculate_metrics(completed, gantt_chart)

def calculate_metrics(completed, gantt_chart):
    avg_waiting = sum(p['waiting_time'] for p in completed) / len(completed) if completed else 0
    avg_turnaround = sum(p['turnaround_time'] for p in completed) / len(completed) if completed else 0
    total_idle = sum(item['end'] - item['start'] for item in gantt_chart if item['process_id'] == 'Idle')

    return {
        'processes': completed,
        'gantt_chart': gantt_chart,
        'avg_waiting': round(avg_waiting, 2),
        'avg_turnaround': round(avg_turnaround, 2),
        'total_idle': total_idle
    }