let processCount = 1;

function switchModule(moduleNum) {
    document.getElementById('module1').style.display = moduleNum === 1 ? 'block' : 'none';
    document.getElementById('module2').style.display = moduleNum === 2 ? 'block' : 'none';
    document.getElementById('btnModule1').classList.toggle('active', moduleNum === 1);
    document.getElementById('btnModule2').classList.toggle('active', moduleNum === 2);
}

function addRow() {
    processCount++;
    const tableBody = document.querySelector('#processTable tbody');
    const newRow = document.createElement('tr');
    newRow.innerHTML = `
        <td>P${processCount}</td>
        <td><input type="number" class="arrival" value="0" min="0"></td>
        <td><input type="number" class="burst" value="5" min="1"></td>
        <td><input type="number" class="priority" value="1" min="0"></td>
        <td><button class="remove-btn" onclick="removeRow(this)">Delete</button></td>
    `;
    tableBody.appendChild(newRow);
}

function removeRow(btn) {
    const row = btn.parentNode.parentNode;
    row.parentNode.removeChild(row);
}

function getProcessData() {
    const rows = document.querySelectorAll('#processTable tbody tr');
    const processes = [];
    rows.forEach(row => {
        const id = row.cells[0].innerText;
        const arrival = parseInt(row.querySelector('.arrival').value) || 0;
        const burst = parseInt(row.querySelector('.burst').value) || 1;
        const priority = parseInt(row.querySelector('.priority').value) || 0;
        processes.push({ id, arrival, burst, priority });
    });
    return processes;
}

function runSimulation() {
    const processes = getProcessData();
    const algorithm = document.getElementById('algorithm').value;

    fetch('/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ algorithm, processes })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('results1').style.display = 'block';

        // 1. Render Gantt Chart
        const ganttChart = document.getElementById('ganttChart');
        ganttChart.innerHTML = '';
        if (data.gantt_chart) {
            data.gantt_chart.forEach(block => {
                const div = document.createElement('div');
                div.className = 'gantt-block';
                div.innerText = `${block.id} (${block.start}-${block.end})`;
                ganttChart.appendChild(div);
            });
        }

        // 2. Render Process Result Table
        const tbody = document.querySelector('#resultTable tbody');
        tbody.innerHTML = '';
        if (data.processes) {
            data.processes.forEach(p => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${p.id}</td>
                    <td>${p.arrival}</td>
                    <td>${p.burst}</td>
                    <td>${p.ct ?? p.completion ?? '-'}</td>
                    <td>${p.tat ?? p.turnaround ?? '-'}</td>
                    <td>${p.wt ?? p.waiting ?? '-'}</td>
                `;
                tbody.appendChild(tr);
            });
        }

        // 3. Render Overall Metrics (Handling various response key names)
        const avgWT = data.avg_wt ?? data.avg_waiting_time ?? data.avg_waiting ?? 0;
        const avgTAT = data.avg_tat ?? data.avg_turnaround_time ?? data.avg_turnaround ?? 0;
        const totalIdle = data.total_idle ?? data.total_idle_time ?? data.idle_time ?? 0;

        document.getElementById('avgWaiting').innerText = Number(avgWT).toFixed(2);
        document.getElementById('avgTurnaround').innerText = Number(avgTAT).toFixed(2);
        document.getElementById('totalIdle').innerText = totalIdle;
    })
    .catch(err => console.error('Error running simulation:', err));
}

function runComparison() {
    const processes = getProcessData();
    const checkedBoxes = document.querySelectorAll('#module2 .checkbox-group input:checked');
    const algorithms = Array.from(checkedBoxes).map(cb => cb.value);

    if (algorithms.length === 0) {
        alert('Please select at least one algorithm for comparison.');
        return;
    }

    fetch('/compare', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ algorithms, processes })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('results2').style.display = 'block';

        const ganttContainer = document.getElementById('comparisonGantt');
        ganttContainer.innerHTML = '';

        const tbody = document.querySelector('#comparisonTable tbody');
        tbody.innerHTML = '';

        data.forEach(res => {
            // Gantt Charts
            const algoHeader = document.createElement('h3');
            algoHeader.innerText = res.algorithm;
            ganttContainer.appendChild(algoHeader);

            const ganttDiv = document.createElement('div');
            ganttDiv.className = 'gantt-chart';
            if (res.gantt_chart) {
                res.gantt_chart.forEach(block => {
                    const div = document.createElement('div');
                    div.className = 'gantt-block';
                    div.innerText = `${block.id} (${block.start}-${block.end})`;
                    ganttDiv.appendChild(div);
                });
            }
            ganttContainer.appendChild(ganttDiv);

            // Comparison Table
            const avgWT = res.avg_wt ?? res.avg_waiting_time ?? res.avg_waiting ?? 0;
            const avgTAT = res.avg_tat ?? res.avg_turnaround_time ?? res.avg_turnaround ?? 0;
            const totalIdle = res.total_idle ?? res.total_idle_time ?? res.idle_time ?? 0;

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${res.algorithm}</td>
                <td>${Number(avgWT).toFixed(2)}</td>
                <td>${Number(avgTAT).toFixed(2)}</td>
                <td>${totalIdle}</td>
            `;
            tbody.appendChild(tr);
        });
    })
    .catch(err => console.error('Error running comparison:', err));
}