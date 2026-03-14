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

      const role=result.data.role;
      window.currentUserRole = role;
      return role;
      
    } else {
      window.location.href = "/";
      return null;
    }
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

        if(window.currentUserRole ==="Head_Nurse"){
            staffList.forEach(staff => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${staff.employee_num}</td> 
                <td>${staff.full_name}</td>
                <td>${staff.role}</td>
                <td>${staff.level}</td> 
                <td>${staff.ward}</td>
                <td>${staff.join_date}</td>

                <td class="button">
                    <button class="btn btn-sm btn-outline-primary" id="editStaff-btn" onclick='openmodal("edit",${JSON.stringify(staff)})'>編輯</button>
                    <button class="btn btn-sm btn-outline-danger" id="${staff.id}" onclick="deletestaffinfo(${staff.id})">刪除</button>
                </td>
            `;
            tbody.appendChild(tr);
        })

        };
    } else {
        console.error("無法取得員工資料");
    }
}

async function step(){
    const role= await checkLoginStatus();
    if (role){
        getStaffData();
    }
}
window.addEventListener("load", step);

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

function closeAddPage() {
    const mainInput = document.querySelector(".main-input");
    mainInput.style.display = 'none';   
}

function openmodal(mode, staff = null) {
    const add = document.querySelector("#addStaff-btn");
    const edit = document.querySelector("#edit");
    let maininput = document.querySelector(".main-input");
    let submitbtn = document.querySelector("#insert-btn");
    let title = document.querySelector(".main-input-title");
    let idField=document.querySelector(".main-input .addStaff-ID");
    const roleSelect = document.querySelector(".main-input #addStaff-role");
    
    const params = window.location.search;
    params_list = params.split('=');
    role=params_list[1]


    if(role=='adminstaff'){
            const staffnurseOption = roleSelect.querySelector('option[value="Staff_Nurse"]');
            staffnurseOption.style.display = 'none';

        }else if(role=='generalstaff'){
            const itadminOption = roleSelect.querySelector('option[value="IT_Admin"]');
            const headnurseOption = roleSelect.querySelector('option[value="Head_Nurse"]');   
            itadminOption.style.display = 'none';
            headnurseOption.style.display = 'none';
        }

    if(mode == 'edit' && staff){

        maininput.style.display = 'flex';
        title.innerText = "編輯員工檔案";
        submitbtn.innerText = "儲存修改";
        submitbtn.onclick = editstaffinfo;

        document.querySelector(".main-input .addStaff-ID").value = staff.employee_num; 

        idField.readOnly = true; 
        idField.style.backgroundColor = "#f0f0f0";
        
        document.querySelector(".main-input .addStaff-name").value = staff.full_name; 
        
        const roleSelect = document.querySelector(".main-input #addStaff-role");
        roleSelect.value = staff.role;
        
        renew(roleSelect.value); 
        if(staff.level == null){
            document.querySelector(".main-input select[name='member']").value = "無職級";
        }else{
            document.querySelector(".main-input select[name='member']").value = staff.level;
        }


        document.querySelector(".main-input .addStaff-ward").value = staff.ward;
        document.querySelector(".main-input .addStaff-joindate").value = staff.join_date;

    }else if(mode == 'add' && staff==null){

        maininput.style.display = 'flex';
        submitbtn.onclick = insertstaffinfo;
        title.innerText = "員工管理新增表單"; 
        submitbtn.innerText = "新增員工檔案";

        idField.value = "";
        idField.readOnly = false;
        idField.style.backgroundColor = "white";

        document.querySelector(".main-input .addStaff-name").value = "";
        document.querySelector(".main-input #addStaff-role").value = "";
        document.querySelector(".main-input select[name='member']").innerHTML = '<option value="">請先選取職級</option>';
        document.querySelector(".main-input .addStaff-ward").value = "";
        document.querySelector(".main-input .addStaff-joindate").value = "";
        
    }
}