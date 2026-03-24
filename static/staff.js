function logout() {
    localStorage.removeItem("token");
    window.location.href = "/";
}

async function checkLoginStatus() {
    const token = localStorage.getItem("token");

    let response = await fetch("/api/user/auth", {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}` 
        }
    });

    const result = await response.json();

    if (response.ok && result.data !== null) {
      document.querySelector("#username").textContent = result.data.full_name;
      
      const userRole = result.data.role;

        if (userRole === "Staff_Nurse") {
            const navbarsetting = document.querySelector("#nav-setting");
            const navbarautocalendar = document.querySelector("#nav-staffmanagement");
            navbarsetting.style.display = "none";
            navbarautocalendar.style.display = "none";
        }
      
    } else {
      window.location.href = "/";
    }
}
window.addEventListener("load", checkLoginStatus);

async function getStaffData() {
    const ward_id = sessionStorage.getItem("current_ward_id");
    const token = localStorage.getItem("token");
    
    const response = await fetch(`/api/ward/${ward_id}/staff`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });
    
    const result = await response.json();
        
    if (response.ok) {
        const tbody = document.querySelector("#staffTableBody");
        const staffList = result.data;
        tbody.innerHTML = "";

        staffList.forEach(staff => {
            const tr = document.createElement("tr");
            const staffData = JSON.stringify(staff).replace(/"/g, '&quot;');

            let displayRole = staff.role;
            if (staff.role === "Staff_Nurse") {
                displayRole = "護理師";
            } else if (staff.role === "Head_Nurse") {
                displayRole = "管理員";
            }

            
            tr.innerHTML = `
                    <td>${staff.employee_num}</td> 
                    <td>${staff.full_name}</td>
                    <td>${displayRole}</td>
                    <td>${staff.level || 'None'}</td> 
                    <td>${staff.ward}</td>

                    <td class="button">
                        <button class="btn btn-sm btn-outline-primary" onclick='openeditPage(${staffData})'>編輯</button>
                        <button class="btn btn-sm btn-outline-danger" onclick="deletestaffinfo(${staff.id})">刪除</button>
                    </td>
                `;
            tbody.appendChild(tr);
        });

    } else {
        console.error("無法取得員工資料");
    }
}
getStaffData()


let staffChoices;
function initChoices() {
    const element = document.getElementById('available-staff-choices');
    if (element) {
        staffChoices = new Choices(element, {
            searchEnabled: true,
            removeItemButton: false,
            shouldSort: false,
            placeholder: true,
            placeholderValue: '請選擇一位人員',
            noResultsText: '找不到相符的人員',
            itemSelectText: '點擊選取',
        });
    }
}

async function loadStaffToChoices() {
    const ward_id = sessionStorage.getItem("current_ward_id");
    const token = localStorage.getItem("token");

    try {
        const response = await fetch(`/api/ward/${ward_id}/staffexcept`, {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` }
        });

        const result = await response.json();

        if (response.ok && result.data) {
            const choicesData = result.data.map(user => ({
                value: user.id,
                label: `${user.employee_num} - ${user.full_name}`,
                selected: false,
                disabled: false,
            }));
            staffChoices.clearChoices();
            staffChoices.setChoices(choicesData, 'value', 'label', true);
        }
    } catch (error) {
        console.error("Choices.js 載入資料失敗:", error);
    }
}

function openAddPage() {
    const mainInput = document.querySelector(".main-input");
    const overlay = document.getElementById("overlay");
    
    mainInput.style.display = 'flex';
    overlay.style.display = 'block';
    document.body.style.overflow = 'hidden';


    document.getElementById("form-title").textContent = "員工管理新增表單";
    document.getElementById("edit-info-group").style.display = "none";
    document.getElementById("add-select-group").style.display = "block";
    document.getElementById("submit-insert-btn").style.display = "inline-block";
    document.getElementById("submit-edit-btn").style.display = "none";
    document.getElementById("addStaff-role").value = "";
    
    if (!staffChoices) {
        initChoices();
    }
    loadStaffToChoices();
}

async function insertstaffinfo() {
    const token = localStorage.getItem("token");
    const ward_id = sessionStorage.getItem("current_ward_id");
    
    const selectedStaffId = staffChoices.getValue(true); 
    const level = document.querySelector("#addStaff-role").value;
    
    if (!selectedStaffId) {
        alert("請先選擇一位員工");
        return;
    }

    let response = await fetch(`/api/ward/${ward_id}/staff`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}` 
        },
        body: JSON.stringify({
            "staffid": selectedStaffId,
            "level": level,
            "ward": ward_id
        })
    });

    if (response.ok) {
        window.location.reload();
    }
}

async function deletestaffinfo(id) {
    const token = localStorage.getItem("token");
    const ward_id = sessionStorage.getItem("current_ward_id");

    let response = await fetch(`/api/ward/${ward_id}/staff`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}` 
        },
        body:JSON.stringify({"staffid":id})
    });

    const result = await response.json();

    if (response.ok && result.data !== null) {
      window.location.reload();

    } else {
      hint.textContent = result.message;
    }
}

async function editstaffinfo() {
    const token = localStorage.getItem("token");
    const ward_id = sessionStorage.getItem("current_ward_id");

    let staffid = document.getElementById("edit-staff-id").value;
    let level = document.querySelector("#addStaff-role").value;
    let hint=document.querySelector(".main-input-hint");
    

    let response = await fetch(`/api/ward/${ward_id}/staff`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}` 
        },
        body:JSON.stringify({"staffid":staffid,"level":level})
    });

    const result = await response.json();

    if (response.ok && result.ok === true) {
      window.location.reload();

    } else {
      hint.textContent = result.message;
      hint.style.color = "red";
    }
}


function openeditPage(staff) {
    const mainInput = document.querySelector(".main-input");
    const overlay = document.getElementById("overlay");
    
    mainInput.style.display = 'flex'; 
    overlay.style.display = 'block';  
    document.body.style.overflow = 'hidden';
    
    document.getElementById("form-title").textContent = "修改員工職級";
    document.getElementById("edit-info-group").style.display = "block";
    document.getElementById("add-select-group").style.display = "none";
    
    
    document.getElementById("display-emp-num").textContent = staff.employee_num;
    document.getElementById("display-full-name").textContent = staff.full_name;
    document.getElementById("edit-staff-id").value = staff.id;
    document.getElementById("addStaff-role").value = staff.level || "none";


    document.getElementById("submit-insert-btn").style.display = "none";
    document.getElementById("submit-edit-btn").style.display = "inline-block";
}

function closeAddPage() {
    const mainInput = document.querySelector(".main-input");
    const overlay = document.getElementById("overlay");
    mainInput.style.display = 'none';   
    overlay.style.display = 'none';   
    document.body.style.overflow = 'auto';
}


async function deleteWard() {
    const ward_id = sessionStorage.getItem("current_ward_id");
    if (!confirm("確定要刪除此病房嗎？")) return;

    const token = localStorage.getItem("token");
    const response = await fetch("/api/member_ward", {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ "ward_id": ward_id })
    });

    if (response.ok) {
        alert("刪除成功");
        window.location.href = "/index";
    } else {
        const result = await response.json();
        alert(result.message);
    }
}