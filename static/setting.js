function addStaff() {
    const id = document.getElementById('staffID').value;
    const name = document.getElementById('staffName').value;
    const title = document.getElementById('staffTitle').value;
    const ward = document.getElementById('staffWard').value;

    if (!id || !name || !title || !ward) {
        alert("請填寫所有欄位！");
        return;
    }


    const tableBody = document.getElementById('staffTableBody');


    tableBody.innerHTML += `
        <tr>
            <td>${id}</td>
            <td>${name}</td>
            <td>${title}</td>
            <td>${ward}</td>
            <td>
                <button class="btn btn-danger btn-sm">刪除</button>
                <button class="btn btn-outline-primary btn-sm">編輯</button>
            </td>
        </tr>
    `;

    document.getElementById('staffID').value = '';
    document.getElementById('staffName').value = '';
    document.getElementById('staffTitle').value = '';
    document.getElementById('staffWard').value = '';
}