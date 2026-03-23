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
        
    if (response.ok){
        const tbody = document.querySelector("#staffTableBody");
        
        const staffList = result.data; 
        tbody.innerHTML = ""; 
        staffList.forEach(staff => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
                <td>${staff.employee_num}</td> 
                <td>${staff.full_name}</td>
                <td>${staff.role}</td>
                <td>${staff.level}</td> 
                <td>${staff.ward}</td>

                <td class="button">
                    <button class="btn btn-sm btn-outline-primary" id="editStaff-btn" onclick='openmodal("edit",${JSON.stringify(staff)})'>編輯</button>
                    <button class="btn btn-sm btn-outline-danger" id="${staff.id}" onclick="deletestaffinfo(${staff.id})">刪除</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } else {
        console.error("無法取得員工資料");
    }
}
getStaffData()

// 選單連動
const roleobject={
"":["請先選取職稱"],
"IT_Admin":["無職級"],	
"Head_Nurse":["無職級"],	
"Staff_Nurse":["N0", "N1", "N2", "N3", "N4"]};

function renew(value){
    const memberSelect = document.myForm.member;
    const options = roleobject[value];
    memberSelect.length = 0;

	options.forEach(text => {
    // new Option(顯示文字, 數值)
    memberSelect.options.add(new Option(text, text));});
}

async function insertstaffinfo() {
    const token = localStorage.getItem("token");


    let staffid=document.querySelector(".addStaff-ID").value;
    let name=document.querySelector(".addStaff-name").value;
    let role = document.querySelector("#addStaff-role").value;
    let level=document.myForm.member.value;
    let ward=document.querySelector(".addStaff-ward").value;
    let joindate=document.querySelector(".addStaff-joindate").value;
    let hint=document.querySelector(".main-input-hint");
    

    let response = await fetch("/api/staff", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}` 
        },
        body:JSON.stringify({"staffid":staffid,"name":name,"role":role,"level":level,"ward":ward,"joindate":joindate})
    });

    const result = await response.json();

    if (response.ok && result.data !== null) {
      window.location.reload();

    } else {
      hint.textContent = result.message;
    }
}

async function deletestaffinfo(id) {
    const token = localStorage.getItem("token");

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

    let staffid=document.querySelector(".addStaff-ID").value;
    let name=document.querySelector(".addStaff-name").value;
    let role = document.querySelector("#addStaff-role").value;
    let level=document.myForm.member.value;
    let ward=document.querySelector(".addStaff-ward").value;
    let joindate=document.querySelector(".addStaff-joindate").value;
    let hint=document.querySelector(".main-input-hint");
    

    let response = await fetch("/api/staff", {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}` 
        },
        body:JSON.stringify({"staffid":staffid,"name":name,"role":role,"level":level,"ward":ward,"joindate":joindate})
    });

    const result = await response.json();

    if (response.ok && result.data !== null) {
      window.location.reload();

    } else {
      hint.textContent = result.message;
    }
}

function closeAddPage() {
    const mainInput = document.querySelector(".main-input");
    mainInput.style.display = 'none';   
}