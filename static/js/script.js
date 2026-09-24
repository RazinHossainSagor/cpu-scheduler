let processCount = 1;

// Function to Add Process Row
function addRow() {
    processCount++;
    const tableBody = document.querySelector("#processTable tbody");
    const row = document.createElement("tr");

    row.innerHTML = `
        <td>P${processCount}</td>
        <td><input type="number" class="arrival" value="0" min="0"></td>
        <td><input type="number" class="burst" value="5" min="1"></td>
        <td><input type="number" class="priority" value="1" min="0"></td>
        <td><button class="btn-delete" onclick="removeRow(this)">Delete</button></td>
    `;
    tableBody.appendChild(row);
}

// Function to Remove Process Row
function removeRow(btn) {
    const row = btn.parentElement.parentElement;
    const tbody = row.parentElement;
    if (tbody.children.length > 1) {
        row.remove();
        reindexProcesses();
    } else {
        alert("At least one process is required!");
    }
}

// Re-index process IDs after deletion
function reindexProcesses() {
    const rows = document.querySelectorAll("#processTable tbody tr");
    processCount = rows.length;
    rows.forEach((row, index) => {
        row.children[0].innerText = `P${index + 1}`;
    });
}

// Switch between Module 1 and Module 2
function switchModule(moduleNum) {
    const mod1 = document.getElementById("module1");
    const mod2 = document.getElementById("module2");
    const btn1 = document.getElementById("btnModule1");
    const btn2 = document.getElementById("btnModule2");

    if (moduleNum === 1) {
        mod1.style.display = "block";
        mod2.style.display = "none";
        btn1.classList.add("active");
        btn2.classList.remove("active");
    } else {
        mod1.style.display = "none";
        mod2.style.display = "block";
        btn2.classList.add("active");
        btn1.classList.remove("active");
    }
}

// Helper function to extract input processes
function getProcessData() {
    const rows = document.querySelectorAll("#processTable tbody tr");
    const processes = [];

    rows.forEach((row) => {
        const id = row.children[0].innerText;
        const arrival = parseInt(row.querySelector(".arrival").value) || 0;
        const burst = parseInt(row.querySelector(".burst").value) || 1;
        const priority = parseInt(row.querySelector(".priority").value) || 0;

        processes.push({
            id: id,
            arrival: arrival,
            burst: burst,
            priority: priority
        });
    });

    return processes;
}

// Run Module 1 Simulation
function runSimulation() {
    const processes = getProcessData();
    const algorithm = document.getElementById("algorithm").value;

    fetch("/simulate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            algorithm: algorithm,
            processes: processes
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }

        document.getElementById("results1").style.display = "block";

        // Render Gantt Chart
        renderGanttChart("ganttChart", data.gantt);

        // Render Process Details Table
        const resultTableBody = document.querySelector("#resultTable tbody");
        resultTableBody.innerHTML = "";

        data.processes.forEach(p => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${p.id}</td>
                <td>${p.arrival}</td>
                <td>${p.burst}</td>
                <td>${p.completion}</td>
                <td>${p.turnaround}</td>
                <td>${p.waiting}</td>
            `;
            resultTableBody.appendChild(tr);
        });

        // Metrics Summary
        document.getElementById("avgWaiting").innerText = data.avg_waiting.toFixed(2);
        document.getElementById("avgTurnaround").innerText = data.avg_turnaround.toFixed(2);
        document.getElementById("totalIdle").innerText = data.total_idle;
    })
    .catch(error => {
        console.error("Error running simulation:", error);
        alert("An error occurred while running the simulation.");
    });
}

// Run Module 2 Comparison
function runComparison() {
    const processes = getProcessData();
    const checkedBoxes = document.querySelectorAll(".checkbox-group input[type='checkbox']:checked");
    const selectedAlgos = Array.from(checkedBoxes).map(cb => cb.value);

    if (selectedAlgos.length === 0) {
        alert("Please select at least one algorithm to compare!");
        return;
    }

    fetch("/compare", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            algorithms: selectedAlgos,
            processes: processes
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }

        document.getElementById("results2").style.display = "block";

        // Render Gantt Charts for each algorithm
        const comparisonGanttDiv = document.getElementById("comparisonGantt");
        comparisonGanttDiv.innerHTML = "";

        const comparisonTableBody = document.querySelector("#comparisonTable tbody");
        comparisonTableBody.innerHTML = "";

        data.results.forEach(res => {
            // Title for Gantt
            const title = document.createElement("h3");
            title.innerText = res.algorithm;
            title.style.color = "#38bdf8";
            title.style.margin = "15px 0 8px 0";
            comparisonGanttDiv.appendChild(title);

            // Container for Gantt Chart
            const ganttContainer = document.createElement("div");
            ganttContainer.className = "gantt-chart-container";
            comparisonGanttDiv.appendChild(ganttContainer);

            renderGanttChart(ganttContainer, res.gantt);

            // Table Row
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${res.algorithm}</td>
                <td>${res.avg_waiting.toFixed(2)}</td>
                <td>${res.avg_turnaround.toFixed(2)}</td>
                <td>${res.total_idle}</td>
            `;
            comparisonTableBody.appendChild(tr);
        });
    })
    .catch(error => {
        console.error("Error running comparison:", error);
        alert("An error occurred while running the comparison.");
    });
}

// Function to render Gantt Chart HTML
function renderGanttChart(containerOrId, ganttData) {
    const container = typeof containerOrId === "string" ? document.getElementById(containerOrId) : containerOrId;
    container.innerHTML = "";

    ganttData.forEach(item => {
        const block = document.createElement("div");
        block.className = "gantt-block";
        block.innerText = `${item.process} (${item.start}-${item.end})`;
        
        if (item.process === "Idle") {
            block.style.backgroundColor = "#475569";
        }
        
        container.appendChild(block);
    });
}