# 1. FCFS (First Come First Serve)
def run_fcfs(processes):
    procs = [p.copy() for p in processes]
    procs.sort(key=lambda x: int(x.get('arrival_time', 0)))
    current_time = 0
    gantt_chart = []
    
    for p in procs:
        at = int(p.get('arrival_time', 0))
        bt = int(p.get('burst_time', 0))
        
        if current_time < at:
            gantt_chart.append({'process_id': 'Idle', 'start': current_time, 'end': at})
            current_time = at
            
        start = current_time
        current_time += bt
        p['completion_time'] = current_time
        p['turnaround_time'] = p['completion_time'] - at
        p['waiting_time'] = p['turnaround_time'] - bt
        gantt_chart.append({'process_id': p.get('id', p.get('process_id')), 'start': start, 'end': current_time})
        
    return calculate_metrics(procs, gantt_chart)

# 2. SJF (Shortest Job First Non-Preemptive)
def run_sjf(processes):
    procs = [p.copy() for p in processes]
    n = len(procs)
    completed = 0
    current_time = 0
    gantt_chart = []
    is_completed = [False] * n

    while completed < n:
        idx = -1
        min_bt = float('inf')
        for i in range(n):
            at = int(procs[i].get('arrival_time', 0))
            bt = int(procs[i].get('burst_time', 0))
            if at <= current_time and not is_completed[i]:
                if bt < min_bt:
                    min_bt = bt
                    idx = i

        if idx != -1:
            at = int(procs[idx].get('arrival_time', 0))
            bt = int(procs[idx].get('burst_time', 0))
            start = current_time
            current_time += bt
            procs[idx]['completion_time'] = current_time
            procs[idx]['turnaround_time'] = procs[idx]['completion_time'] - at
            procs[idx]['waiting_time'] = procs[idx]['turnaround_time'] - bt
            
            gantt_chart.append({'process_id': procs[idx].get('id', procs[idx].get('process_id')), 'start': start, 'end': current_time})
            is_completed[idx] = True
            completed += 1
        else:
            gantt_chart.append({'process_id': 'Idle', 'start': current_time, 'end': current_time + 1})
            current_time += 1

    return calculate_metrics(procs, gantt_chart)

# 3. Priority Non-Preemptive
def run_priority(processes):
    procs = [p.copy() for p in processes]
    n = len(procs)
    completed = 0
    current_time = 0
    gantt_chart = []
    is_completed = [False] * n

    while completed < n:
        idx = -1
        highest_priority = float('inf')
        for i in range(n):
            at = int(procs[i].get('arrival_time', 0))
            prio = int(procs[i].get('priority', 0))
            if at <= current_time and not is_completed[i]:
                if prio < highest_priority:
                    highest_priority = prio
                    idx = i

        if idx != -1:
            at = int(procs[idx].get('arrival_time', 0))
            bt = int(procs[idx].get('burst_time', 0))
            start = current_time
            current_time += bt
            procs[idx]['completion_time'] = current_time
            procs[idx]['turnaround_time'] = procs[idx]['completion_time'] - at
            procs[idx]['waiting_time'] = procs[idx]['turnaround_time'] - bt
            
            gantt_chart.append({'process_id': procs[idx].get('id', procs[idx].get('process_id')), 'start': start, 'end': current_time})
            is_completed[idx] = True
            completed += 1
        else:
            gantt_chart.append({'process_id': 'Idle', 'start': current_time, 'end': current_time + 1})
            current_time += 1

    return calculate_metrics(procs, gantt_chart)

# 4. SRTF (SJF Preemptive)
def run_srtf(processes):
    procs = [p.copy() for p in processes]
    n = len(procs)
    remaining_time = [int(p.get('burst_time', 0)) for p in procs]
    completed = 0
    current_time = 0
    gantt_chart = []
    prev_proc = None

    while completed < n:
        idx = -1
        min_bt = float('inf')
        for i in range(n):
            at = int(procs[i].get('arrival_time', 0))
            if at <= current_time and remaining_time[i] > 0:
                if remaining_time[i] < min_bt:
                    min_bt = remaining_time[i]
                    idx = i

        if idx != -1:
            pid = procs[idx].get('id', procs[idx].get('process_id'))
            if prev_proc == pid and gantt_chart:
                gantt_chart[-1]['end'] += 1
            else:
                gantt_chart.append({'process_id': pid, 'start': current_time, 'end': current_time + 1})
            
            remaining_time[idx] -= 1
            prev_proc = pid
            current_time += 1
            
            if remaining_time[idx] == 0:
                completed += 1
                at = int(procs[idx].get('arrival_time', 0))
                bt = int(procs[idx].get('burst_time', 0))
                procs[idx]['completion_time'] = current_time
                procs[idx]['turnaround_time'] = current_time - at
                procs[idx]['waiting_time'] = procs[idx]['turnaround_time'] - bt
        else:
            if prev_proc == 'Idle' and gantt_chart:
                gantt_chart[-1]['end'] += 1
            else:
                gantt_chart.append({'process_id': 'Idle', 'start': current_time, 'end': current_time + 1})
            prev_proc = 'Idle'
            current_time += 1

    return calculate_metrics(procs, gantt_chart)

# 5. Priority Preemptive
def run_priority_preemptive(processes):
    procs = [p.copy() for p in processes]
    n = len(procs)
    remaining_time = [int(p.get('burst_time', 0)) for p in procs]
    completed = 0
    current_time = 0
    gantt_chart = []
    prev_proc = None

    while completed < n:
        idx = -1
        highest_priority = float('inf')
        for i in range(n):
            at = int(procs[i].get('arrival_time', 0))
            prio = int(procs[i].get('priority', 0))
            if at <= current_time and remaining_time[i] > 0:
                if prio < highest_priority:
                    highest_priority = prio
                    idx = i

        if idx != -1:
            pid = procs[idx].get('id', procs[idx].get('process_id'))
            if prev_proc == pid and gantt_chart:
                gantt_chart[-1]['end'] += 1
            else:
                gantt_chart.append({'process_id': pid, 'start': current_time, 'end': current_time + 1})
            
            remaining_time[idx] -= 1
            prev_proc = pid
            current_time += 1
            
            if remaining_time[idx] == 0:
                completed += 1
                at = int(procs[idx].get('arrival_time', 0))
                bt = int(procs[idx].get('burst_time', 0))
                procs[idx]['completion_time'] = current_time
                procs[idx]['turnaround_time'] = current_time - at
                procs[idx]['waiting_time'] = procs[idx]['turnaround_time'] - bt
        else:
            if prev_proc == 'Idle' and gantt_chart:
                gantt_chart[-1]['end'] += 1
            else:
                gantt_chart.append({'process_id': 'Idle', 'start': current_time, 'end': current_time + 1})
            prev_proc = 'Idle'
            current_time += 1

    return calculate_metrics(procs, gantt_chart)

# 6. Round Robin (RR)
def run_round_robin(processes, time_quantum=2):
    procs = [p.copy() for p in processes]
    n = len(procs)
    remaining_time = [int(p.get('burst_time', 0)) for p in procs]
    current_time = 0
    gantt_chart = []
    queue = []
    visited = [False] * n
    completed = 0

    sorted_indices = sorted(range(n), key=lambda i: int(procs[i].get('arrival_time', 0)))
    
    first_at = int(procs[sorted_indices[0]].get('arrival_time', 0))
    if first_at > 0:
        gantt_chart.append({'process_id': 'Idle', 'start': 0, 'end': first_at})
        current_time = first_at

    queue.append(sorted_indices[0])
    visited[sorted_indices[0]] = True

    while completed < n:
        if not queue:
            for i in sorted_indices:
                if remaining_time[i] > 0:
                    at = int(procs[i].get('arrival_time', 0))
                    if current_time < at:
                        gantt_chart.append({'process_id': 'Idle', 'start': current_time, 'end': at})
                        current_time = at
                    queue.append(i)
                    visited[i] = True
                    break

        idx = queue.pop(0)
        exec_time = min(time_quantum, remaining_time[idx])
        pid = procs[idx].get('id', procs[idx].get('process_id'))
        
        gantt_chart.append({'process_id': pid, 'start': current_time, 'end': current_time + exec_time})

        current_time += exec_time
        remaining_time[idx] -= exec_time

        for i in sorted_indices:
            at = int(procs[i].get('arrival_time', 0))
            if not visited[i] and at <= current_time and remaining_time[i] > 0:
                queue.append(i)
                visited[i] = True

        if remaining_time[idx] > 0:
            queue.append(idx)
        else:
            completed += 1
            at = int(procs[idx].get('arrival_time', 0))
            bt = int(procs[idx].get('burst_time', 0))
            procs[idx]['completion_time'] = current_time
            procs[idx]['turnaround_time'] = current_time - at
            procs[idx]['waiting_time'] = procs[idx]['turnaround_time'] - bt

    return calculate_metrics(procs, gantt_chart)

# 7. LJF (Longest Job First Non-Preemptive)
def run_ljf_non_preemptive(processes):
    procs = [p.copy() for p in processes]
    n = len(procs)
    completed = 0
    current_time = 0
    gantt_chart = []
    is_completed = [False] * n

    while completed < n:
        idx = -1
        max_bt = -1
        for i in range(n):
            at = int(procs[i].get('arrival_time', 0))
            bt = int(procs[i].get('burst_time', 0))
            if at <= current_time and not is_completed[i]:
                if bt > max_bt:
                    max_bt = bt
                    idx = i

        if idx != -1:
            at = int(procs[idx].get('arrival_time', 0))
            bt = int(procs[idx].get('burst_time', 0))
            start = current_time
            current_time += bt
            procs[idx]['completion_time'] = current_time
            procs[idx]['turnaround_time'] = procs[idx]['completion_time'] - at
            procs[idx]['waiting_time'] = procs[idx]['turnaround_time'] - bt
            
            gantt_chart.append({'process_id': procs[idx].get('id', procs[idx].get('process_id')), 'start': start, 'end': current_time})
            is_completed[idx] = True
            completed += 1
        else:
            gantt_chart.append({'process_id': 'Idle', 'start': current_time, 'end': current_time + 1})
            current_time += 1

    return calculate_metrics(procs, gantt_chart)

# 8. LJF Preemptive
def run_ljf_preemptive(processes):
    procs = [p.copy() for p in processes]
    n = len(procs)
    remaining_time = [int(p.get('burst_time', 0)) for p in procs]
    completed = 0
    current_time = 0
    gantt_chart = []
    prev_proc = None

    while completed < n:
        idx = -1
        max_bt = -1
        for i in range(n):
            at = int(procs[i].get('arrival_time', 0))
            if at <= current_time and remaining_time[i] > 0:
                if remaining_time[i] > max_bt:
                    max_bt = remaining_time[i]
                    idx = i

        if idx != -1:
            pid = procs[idx].get('id', procs[idx].get('process_id'))
            if prev_proc == pid and gantt_chart:
                gantt_chart[-1]['end'] += 1
            else:
                gantt_chart.append({'process_id': pid, 'start': current_time, 'end': current_time + 1})
            
            remaining_time[idx] -= 1
            prev_proc = pid
            current_time += 1
            
            if remaining_time[idx] == 0:
                completed += 1
                at = int(procs[idx].get('arrival_time', 0))
                bt = int(procs[idx].get('burst_time', 0))
                procs[idx]['completion_time'] = current_time
                procs[idx]['turnaround_time'] = current_time - at
                procs[idx]['waiting_time'] = procs[idx]['turnaround_time'] - bt
        else:
            if prev_proc == 'Idle' and gantt_chart:
                gantt_chart[-1]['end'] += 1
            else:
                gantt_chart.append({'process_id': 'Idle', 'start': current_time, 'end': current_time + 1})
            prev_proc = 'Idle'
            current_time += 1

    return calculate_metrics(procs, gantt_chart)

# Helper function to format metrics
def calculate_metrics(processes, gantt_chart):
    total_wt = sum(p.get('waiting_time', 0) for p in processes)
    total_tat = sum(p.get('turnaround_time', 0) for p in processes)
    n = len(processes) if len(processes) > 0 else 1
    
    idle_time = sum(g['end'] - g['start'] for g in gantt_chart if g['process_id'] == 'Idle')

    return {
        'processes': processes,
        'gantt_chart': gantt_chart,
        'avg_waiting_time': round(total_wt / n, 2),
        'avg_turnaround_time': round(total_tat / n, 2),
        'total_idle_time': idle_time
    }