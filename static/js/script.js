let processCount = 1;

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

function reindexProcesses() {
    const rows = document.querySelectorAll("#processTable tbody tr");
    processCount = rows.length;
    rows.forEach((row, index) => {
        row.children[0].innerText = `P${index + 1}`;
    });
}

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