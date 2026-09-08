let processCount = 1;

function switchModule(moduleNum) {
    document.getElementById("module1").style.display = moduleNum === 1 ? "block" : "none";
    document.getElementById("module2").style.display = moduleNum === 2 ? "block" : "none";
    document.getElementById("btnModule1").className = moduleNum === 1 ? "active" : "";
    document.getElementById("btnModule2").className = moduleNum === 2 ? "active" : "";
}

function addRow() {
    processCount++;
    const table = document.getElementById("processTable").getElementsByTagName('tbody')[0];
    const row = table.insertRow();
    row.innerHTML = `
        <td>P${processCount}</td>
        <td><input type="number" class="arrival" value="0" min="0"></td>
        <td><input type="number" class="burst" value="1" min="1"></td>
        <td><input type="number" class="priority" value="1" min="0"></td>
        <td><button class="remove-btn" onclick="removeRow(this)">Delete</button></td>
    `;
}

function removeRow(btn) {
    const row = btn.parentNode.parentNode;
    row.parentNode.removeChild(row);
}

function getProcessInputs() {
    const rows = document.querySelectorAll("#processTable tbody tr");
    const processes = [];
    rows.forEach(row => {
        const id = row.cells[0].innerText;
        const arrival = parseInt(row.querySelector(".arrival").value);
        const burst = parseInt(row.querySelector(".burst").value);
        const priority = parseInt(row.querySelector(".priority").value);
        if (!isNaN(arrival) && !isNaN(burst)) {
            processes.push({ id, arrival_time: arrival, burst_time: burst, priority: isNaN(priority) ? 0 : priority });
        }
    });
    return processes;
}

function runSimulation() {
    const algorithm = document.getElementById("algorithm").value;
    const processes = getProcessInputs();

    fetch('/api/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ algorithm, processes })
    })
    .then(res => res.json())
    .then(data => displayModule1Results(data));
}

function displayModule1Results(data) {
    document.getElementById("results1").style.display = "block";
    document.getElementById("avgWaiting").innerText = data.avg_waiting;
    document.getElementById("avgTurnaround").innerText = data.avg_turnaround;
    document.getElementById("totalIdle").innerText = data.total_idle;

    // Gantt Chart
    const gantt = document.getElementById("ganttChart");
    gantt.innerHTML = "";
    data.gantt_chart.forEach(item => {
        const block = document.createElement("div");
        block.className = `gantt-block ${item.process_id === 'Idle' ? 'idle' : ''}`;
        block.style.flex = item.end - item.start;
        block.innerText = `${item.process_id} (${item.start}-${item.end})`;
        gantt.appendChild(block);
    });

    // Result Table
    const tbody = document.getElementById("resultTable").querySelector("tbody");
    tbody.innerHTML = "";
    data.processes.forEach(p => {
        const row = tbody.insertRow();
        row.innerHTML = `
            <td>${p.id}</td>
            <td>${p.arrival_time}</td>
            <td>${p.burst_time}</td>
            <td>${p.completion_time}</td>
            <td>${p.turnaround_time}</td>
            <td>${p.waiting_time}</td>
        `;
    });
}

function runComparison() {
    const checkboxes = document.querySelectorAll("#module2 input[type='checkbox']:checked");
    const algorithms = Array.from(checkboxes).map(cb => cb.value);
    const processes = getProcessInputs();

    fetch('/api/compare', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ algorithms, processes })
    })
    .then(res => res.json())
    .then(data => displayModule2Results(data));
}

function displayModule2Results(data) {
    document.getElementById("results2").style.display = "block";

    const ganttContainer = document.getElementById("comparisonGantt");
    ganttContainer.innerHTML = "";

    const summaryTableBody = document.getElementById("comparisonTable").querySelector("tbody");
    summaryTableBody.innerHTML = "";

    for (const [algo, result] of Object.entries(data)) {
        // Render Gantt Chart
        const algoTitle = document.createElement("h4");
        algoTitle.innerText = algo;
        ganttContainer.appendChild(algoTitle);

        const gantt = document.createElement("div");
        gantt.className = "gantt-chart";
        result.gantt_chart.forEach(item => {
            const block = document.createElement("div");
            block.className = `gantt-block ${item.process_id === 'Idle' ? 'idle' : ''}`;
            block.style.flex = item.end - item.start;
            block.innerText = `${item.process_id} (${item.start}-${item.end})`;
            gantt.appendChild(block);
        });
        ganttContainer.appendChild(gantt);

        // Render Summary Table
        const row = summaryTableBody.insertRow();
        row.innerHTML = `
            <td><b>${algo}</b></td>
            <td>${result.avg_waiting}</td>
            <td>${result.avg_turnaround}</td>
            <td>${result.total_idle}</td>
        `;
    }
}