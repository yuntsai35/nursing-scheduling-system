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


async function getStaffDataNight() {
    const token = localStorage.getItem("token");
    const response = await fetch(`/api/staff`, {
        method: "GET",
        headers: { "Authorization": `Bearer ${token}` }
    });
    const result = await response.json();

    if (response.ok) {
        const staffList = result.data;
        // 核心修正：直接執行初始化，不要包在 window.onload
        const targetSelect = document.querySelector('.multi-selector');
        initMultiElement(targetSelect, staffList, "night");
    }
}

async function getStaffDataMidnight() {
    const token = localStorage.getItem("token");
    const response = await fetch(`/api/staff`, {
        method: "GET",
        headers: { "Authorization": `Bearer ${token}` }
    });
    const result = await response.json();

    if (response.ok) {
        const staffList = result.data;
        // 核心修正：直接執行初始化，對準大夜的 class
        const targetSelect = document.querySelector('.multi-selector-midnight');
        initMultiElement(targetSelect, staffList, "midnight");
    }
}

// 抽出來的通用初始化函式
function initMultiElement(targetSelect, staffList, type) {
    var multiElement = document.createElement('div');
    multiElement.setAttribute('class', `dropdown dropdown-${type}`); // 加入區別用的 class
    var html = `<div class="item text"><label></label></div>`;

    staffList.forEach(staff => {
        // 同步原始 select 的 options (如果 HTML 裡沒寫的話)
        let opt = document.createElement('option');
        opt.value = staff.full_name;
        opt.text = staff.full_name;
        targetSelect.appendChild(opt);

        html += `<div class="item">
                    <input type="checkbox" value="${staff.full_name}"/>
                    <span>${staff.full_name}</span>
                 </div>`;
    });
    
    multiElement.innerHTML = html;
    targetSelect.parentElement.appendChild(multiElement);

    // 設定點擊事件：只針對當前這個 multiElement 內部的 input
    const checkboxes = multiElement.querySelectorAll('input[type="checkbox"]');
    const label = multiElement.querySelector('.text label');

    checkboxes.forEach(function(checkItem) {
        checkItem.addEventListener("click", function(e) {
            let resultText = '';
            // 只抓「當前選單」被勾選的
            let checkedItems = multiElement.querySelectorAll('input:checked[type="checkbox"]');
            
            checkedItems.forEach(function(selectItem) {
                if (resultText !== '') resultText += ',';
                resultText += selectItem.value;
            });

            // 更新當前選單的 Label
            label.innerText = resultText;

            // 同步回原本對應的 ListBox (targetSelect)
            let option = targetSelect.querySelector(`option[value="${e.target.value}"]`);
            if (option) option.selected = e.target.checked;
        });
    });
}

// 執行兩次
getStaffDataNight();
getStaffDataMidnight();

async function saveSettingmember(){
    const token = localStorage.getItem("token"); 
    const required_dayshift = document.getElementById("required_dayshift").value;
    const required_nightshift = document.getElementById("required_nightshift").value;
    const required_midnightshift = document.getElementById("required_midnightshift").value;

    const nightSelect = document.querySelector('.multi-selector');
    const selectedNightStaff = Array.from(nightSelect.selectedOptions).map(opt => opt.value);
    
    const midnightSelect = document.querySelector('.multi-selector-midnight');
    const selectedMidnightStaff = Array.from(midnightSelect.selectedOptions).map(opt => opt.value);


    const response = await fetch(`/api/settingstaffnumber`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        },
        body:JSON.stringify({"required_dayshift":required_dayshift,"required_nightshift":required_nightshift,"required_mignightshift":required_midnightshift,"multi_selector":selectedNightStaff,"multi_selector_midnight":selectedMidnightStaff

        })}) 
    
    const result = await response.json();
    if (response.ok && result.data !== null){
        alert("儲存成功！");
        window.location.href="/main"
    }
}
