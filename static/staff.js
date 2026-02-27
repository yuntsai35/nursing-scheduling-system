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
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${staff[2]}</td> 
                <td>${staff[1]}</td>
                <td>${staff[4]}</td>
                <td>${staff[5]}</td> 
                <td>${staff[6]}</td>
                <td>${staff[7]}</td>
                
                <td>
                    <button class="btn btn-sm btn-outline-primary" id="editStaff-btn" onclick='openmodal("edit",${JSON.stringify(staff)})'>編輯</button>
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

        document.querySelector(".main-input .addStaff-ID").value = staff[2]; 

        idField.readOnly = true; 
        idField.style.backgroundColor = "#f0f0f0";
        
        document.querySelector(".main-input .addStaff-name").value = staff[1]; 
        
        const roleSelect = document.querySelector(".main-input #addStaff-role");
        roleSelect.value = staff[4];
        
        renew(roleSelect.selectedIndex); 
        if(staff[5] == null){
            document.querySelector(".main-input select[name='member']").value = "無職級";
        }else{
            document.querySelector(".main-input select[name='member']").value = staff[5];
        }


        document.querySelector(".main-input .addStaff-ward").value = staff[6];
        document.querySelector(".main-input .addStaff-joindate").value = staff[7];

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