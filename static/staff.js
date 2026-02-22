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

    } else {
      window.location.href = "/";
    }
}
window.addEventListener("load", checkLoginStatus);

let addStaff = document.querySelector("#addStaff-btn");
let maininput = document.querySelector(".main-input");

if (addStaff) {
    addStaff.addEventListener('click', function() {
        maininput.style.display = 'flex';
    });
}

async function getStaffData() {
    const token = localStorage.getItem("token");
    const response = await fetch("/api/staff", {
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
            tr.innerHTML = `
                <td>${staff[2]}</td> 
                <td>${staff[1]}</td>
                <td>${staff[4]}</td>
                <td>${staff[5]}</td> 
                <td>${staff[6]}</td>
                <td>${staff[7]}</td>
                
                <td>
                    <button class="btn btn-sm btn-outline-primary" onclick='openEdit(${JSON.stringify(staff)})'>編輯</button>
                    <button class="btn btn-sm btn-outline-danger" id="${staff[0]}" onclick="deletestaffinfo(${staff[0]})">刪除</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } else {
        console.error("無法取得員工資料");
    }
}
getStaffData();

role=new Array();
role[0]=["請先選取職稱"];
role[1]=["無職級"];	
role[2]=["無職級"];	
role[3]=["N0", "N1", "N2", "N3", "N4"];

function renew(index){
	for(var i=0;i<role[index].length;i++)
		document.myForm.member.options[i]=new Option(role[index][i], role[index][i]);
	document.myForm.member.length=role[index].length;
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

    let response = await fetch("/api/staff", {
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

function openEdit(staff) {
    const editModal = document.querySelector(".edit-input");
    editModal.style.display = 'flex';

    document.querySelector(".edit-input .addStaff-id").textContent = staff[2]; 
    document.querySelector(".edit-input .addStaff-name").value = staff[1]; 
    
    const roleSelect = document.querySelector(".edit-input #addStaff-role");
    roleSelect.value = staff[5];
    
    renew(roleSelect.selectedIndex); 
    
    document.querySelector(".edit-input select[name='member']").value = staff[6];
    document.querySelector(".edit-input .addStaff-ward").value = staff[7];
    document.querySelector(".edit-input .addStaff-joindate").value = staff[8];
}

function closeAddPage() {
    const mainInput = document.querySelector(".main-input");
    mainInput.style.display = 'none';
    
}