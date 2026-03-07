
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

async function getStaffData() {
    const params = window.location.search;
    params_list = params.split('=');
    role=params_list[1]

    const token = localStorage.getItem("token");
    const response = await fetch(`/api/staff/${role}`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });
    
    const result = await response.json();
        
    if (response.ok){
        const tbody = document.querySelector("#staffTableBody");
        
        const staffList = result.data; 
        tbody.innerHTML = ""; 

        staffList.forEach(staff => {
            const div = document.createElement("div");
            div.innerHTML = `
                <span class="tag">${staff[1]}<span class="remove-tag">&times;</span></span>
                <div class="option" data-value="${staff[1]}">${staff[1]}</div>


            `;
            
            tbody.appendChild(tr);
        });
    } else {
        console.error("無法取得員工資料");
    }
}
getStaffData();