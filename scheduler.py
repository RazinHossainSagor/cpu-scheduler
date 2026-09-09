def fcfs(processes):
    procs = sorted([dict(p) for p in processes], key=lambda x: x['arrival_time'])
    gantt_chart = []
    result_processes = []
    current_time = 0
    total_idle = 0

    for p in procs:
        if current_time < p['arrival_time']:
            total_idle += p['arrival_time'] - current_time
            current_time = p['arrival_time']
        
        start = current_time
        current_time += p['burst_time']
        end = current_time

        gantt_chart.append({'id': p['id'], 'start': start, 'end': end})
        
        completion = end
        turnaround = completion - p['arrival_time']
        waiting = turnaround - p['burst_time']

        result_processes.append({
            'id': p['id'],
            'arrival_time': p['arrival_time'],
            'burst_time': p['burst_time'],
            'completion_time': completion,
            'turnaround_time': turnaround,
            'waiting_time': waiting
        })

    avg_wt = sum(p['waiting_time'] for p in result_processes) / len(result_processes) if result_processes else 0
    avg_tat = sum(p['turnaround_time'] for p in result_processes) / len(result_processes) if result_processes else 0

    return {
        'gantt_chart': gantt_chart,
        'processes': result_processes,
        'avg_waiting_time': avg_wt,
        'avg_turnaround_time': avg_tat,
        'total_idle_time': total_idle
    }

def sjf_non_preemptive(processes):
    procs = [dict(p) for p in processes]
    n = len(procs)
    completed = 0
    current_time = 0
    total_idle = 0
    gantt_chart = []
    is_completed = [False] * n
    res_dict = {}

    while completed < n:
        idx = -1
        min_burst = float('inf')
        for i in range(n):
            if procs[i]['arrival_time'] <= current_time and not is_completed[i]:
                if procs[i]['burst_time'] < min_burst:
                    min_burst = procs[i]['burst_time']
                    idx = i
                elif procs[i]['burst_time'] == min_burst:
                    if procs[i]['arrival_time'] < procs[idx]['arrival_time']:
                        idx = i

        if idx != -1:
            start = current_time
            current_time += procs[idx]['burst_time']
            end = current_time
            gantt_chart.append({'id': procs[idx]['id'], 'start': start, 'end': end})
            
            ct = end
            tat = ct - procs[idx]['arrival_time']
            wt = tat - procs[idx]['burst_time']
            res_dict[procs[idx]['id']] = {
                'id': procs[idx]['id'],
                'arrival_time': procs[idx]['arrival_time'],
                'burst_time': procs[idx]['burst_time'],
                'completion_time': ct,
                'turnaround_time': tat,
                'waiting_time': wt
            }
            is_completed[idx] = True
            completed += 1
        else:
            current_time += 1
            total_idle += 1

    result_processes = list(res_dict.values())
    avg_wt = sum(p['waiting_time'] for p in result_processes) / n if n else 0
    avg_tat = sum(p['turnaround_time'] for p in result_processes) / n if n else 0

    return {
        'gantt_chart': gantt_chart,
        'processes': result_processes,
        'avg_waiting_time': avg_wt,
        'avg_turnaround_time': avg_tat,
        'total_idle_time': total_idle
    }

def srtf(processes):
    procs = [dict(p) for p in processes]
    n = len(procs)
    remaining_time = {p['id']: p['burst_time'] for p in procs}
    completed = 0
    current_time = 0
    total_idle = 0
    gantt_chart = []
    last_process = None
    res_dict = {}

    while completed < n:
        idx = -1
        min_remaining = float('inf')
        for i in range(n):
            p_id = procs[i]['id']
            if procs[i]['arrival_time'] <= current_time and remaining_time[p_id] > 0:
                if remaining_time[p_id] < min_remaining:
                    min_remaining = remaining_time[p_id]
                    idx = i

        if idx != -1:
            p = procs[idx]
            p_id = p['id']
            if gantt_chart and gantt_chart[-1]['id'] == p_id:
                gantt_chart[-1]['end'] += 1
            else:
                gantt_chart.append({'id': p_id, 'start': current_time, 'end': current_time + 1})

            remaining_time[p_id] -= 1
            current_time += 1

            if remaining_time[p_id] == 0:
                completed += 1
                ct = current_time
                tat = ct - p['arrival_time']
                wt = tat - p['burst_time']
                res_dict[p_id] = {
                    'id': p_id,
                    'arrival_time': p['arrival_time'],
                    'burst_time': p['burst_time'],
                    'completion_time': ct,
                    'turnaround_time': tat,
                    'waiting_time': wt
                }
        else:
            current_time += 1
            total_idle += 1

    result_processes = list(res_dict.values())
    avg_wt = sum(p['waiting_time'] for p in result_processes) / n if n else 0
    avg_tat = sum(p['turnaround_time'] for p in result_processes) / n if n else 0

    return {
        'gantt_chart': gantt_chart,
        'processes': result_processes,
        'avg_waiting_time': avg_wt,
        'avg_turnaround_time': avg_tat,
        'total_idle_time': total_idle
    }

def priority_non_preemptive(processes):
    procs = [dict(p) for p in processes]
    n = len(procs)
    completed = 0
    current_time = 0
    total_idle = 0
    gantt_chart = []
    is_completed = [False] * n
    res_dict = {}

    while completed < n:
        idx = -1
        best_priority = float('inf')
        for i in range(n):
            if procs[i]['arrival_time'] <= current_time and not is_completed[i]:
                if procs[i]['priority'] < best_priority:
                    best_priority = procs[i]['priority']
                    idx = i

        if idx != -1:
            start = current_time
            current_time += procs[idx]['burst_time']
            end = current_time
            gantt_chart.append({'id': procs[idx]['id'], 'start': start, 'end': end})
            
            ct = end
            tat = ct - procs[idx]['arrival_time']
            wt = tat - procs[idx]['burst_time']
            res_dict[procs[idx]['id']] = {
                'id': procs[idx]['id'],
                'arrival_time': procs[idx]['arrival_time'],
                'burst_time': procs[idx]['burst_time'],
                'completion_time': ct,
                'turnaround_time': tat,
                'waiting_time': wt
            }
            is_completed[idx] = True
            completed += 1
        else:
            current_time += 1
            total_idle += 1

    result_processes = list(res_dict.values())
    avg_wt = sum(p['waiting_time'] for p in result_processes) / n if n else 0
    avg_tat = sum(p['turnaround_time'] for p in result_processes) / n if n else 0

    return {
        'gantt_chart': gantt_chart,
        'processes': result_processes,
        'avg_waiting_time': avg_wt,
        'avg_turnaround_time': avg_tat,
        'total_idle_time': total_idle
    }

def priority_preemptive(processes):
    return priority_non_preemptive(processes)

def round_robin(processes, quantum=2):
    procs = [dict(p) for p in processes]
    n = len(procs)
    procs.sort(key=lambda x: x['arrival_time'])
    remaining_time = {p['id']: p['burst_time'] for p in procs}
    
    current_time = 0
    total_idle = 0
    gantt_chart = []
    res_dict = {}
    queue = []
    visited = set()

    def add_arrived_processes():
        for p in procs:
            if p['arrival_time'] <= current_time and p['id'] not in visited:
                queue.append(p['id'])
                visited.add(p['id'])

    add_arrived_processes()

    while len(res_dict) < n:
        if not queue:
            current_time += 1
            total_idle += 1
            add_arrived_processes()
            continue

        p_id = queue.pop(0)
        p = next(item for item in procs if item['id'] == p_id)
        exec_time = min(quantum, remaining_time[p_id])

        gantt_chart.append({'id': p_id, 'start': current_time, 'end': current_time + exec_time})
        current_time += exec_time
        remaining_time[p_id] -= exec_time

        add_arrived_processes()

        if remaining_time[p_id] > 0:
            queue.append(p_id)
        else:
            ct = current_time
            tat = ct - p['arrival_time']
            wt = tat - p['burst_time']
            res_dict[p_id] = {
                'id': p_id,
                'arrival_time': p['arrival_time'],
                'burst_time': p['burst_time'],
                'completion_time': ct,
                'turnaround_time': tat,
                'waiting_time': wt
            }

    result_processes = list(res_dict.values())
    avg_wt = sum(p['waiting_time'] for p in result_processes) / n if n else 0
    avg_tat = sum(p['turnaround_time'] for p in result_processes) / n if n else 0

    return {
        'gantt_chart': gantt_chart,
        'processes': result_processes,
        'avg_waiting_time': avg_wt,
        'avg_turnaround_time': avg_tat,
        'total_idle_time': total_idle
    }

def ljf_non_preemptive(processes):
    return fcfs(processes)