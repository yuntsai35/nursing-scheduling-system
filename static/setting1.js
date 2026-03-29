function logout() {
    localStorage.removeItem("token");
    sessionStorage.clear();
    window.location.href = "/login";
}
async function checkLoginStatus() {
    const userRole = sessionStorage.getItem("current_role");
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
      

        if (userRole === "Staff_Nurse") {
            const navbarsetting = document.querySelector("#nav-setting");
            const navbarautocalendar = document.querySelector("#nav-staffmanagement");
            navbarsetting.style.display = "none";
            navbarautocalendar.style.display = "none";
        }
      
    } else {
      window.location.href = "/login";
    }
}
window.addEventListener("load", checkLoginStatus);

const default_member = {
    required_dayshift: "6",
    required_nightshift: "4",
    required_midnightshift: "3"
};

function loadstep3(){
    const staff_number = sessionStorage.getItem("settingstaffnumber_step3");
    let data;

    if (staff_number == null) {
        data = default_member;
    } else {
        data = JSON.parse(staff_number);
    }
    document.querySelector("#required_dayshift").value=data.required_dayshift;
    document.querySelector("#required_nightshift").value=data.required_nightshift;
    document.querySelector("#required_midnightshift").value=data.required_midnightshift;
}
loadstep3();

let nightChoicesInstance;
let midnightChoicesInstance;

document.addEventListener('DOMContentLoaded', function() {
    dayChoicesInstance = new Choices('#day-staff-choices', {
        removeItemButton: true,
        maxItemCount: 2, 
        placeholderValue: '請選擇白班包班人員'
    });
    nightChoicesInstance = new Choices('#night-staff-choices', {
        removeItemButton: true,
        maxItemCount: 2, 
        placeholderValue: '請選擇小夜包班人員'
    });

    midnightChoicesInstance = new Choices('#midnight-staff-choices', {
        removeItemButton: true,
        maxItemCount: 2,
        placeholderValue: '請選擇大夜包班人員'
    });

    loadstep3();
    getStaffDataNight(); 
});


async function getStaffDataNight() {
    const ward_id = sessionStorage.getItem("current_ward_id");
    const step2member = sessionStorage.getItem("settingmember_step2");
    if (!step2member) {
        alert("找不到第二步的人員設定資料");
        window.location.href=`/main/${ward_id}/`;
    }
    const step2Data = JSON.parse(step2member);
    const selectedStaff = step2Data.selectedStaff;


        const staffChoices = selectedStaff.map(staff => ({
            value: staff.name,
            label: staff.name,
            selected: false,
            disabled: false
        }));

        // 將過濾後的人員名單餵給兩個實例
        dayChoicesInstance.setChoices(staffChoices, 'value', 'label', true);
        nightChoicesInstance.setChoices(staffChoices, 'value', 'label', true);
        midnightChoicesInstance.setChoices(staffChoices, 'value', 'label', true);

        // 讀取步驟三暫存回填包班人員 (如果有)
        const step3Cache = sessionStorage.getItem("settingstaffnumber_step3");
        if (step3Cache) {
            const data = JSON.parse(step3Cache);
            if (data.multi_selector) dayChoicesInstance.setChoiceByValue(data.multi_selector_day);
            if (data.multi_selector) nightChoicesInstance.setChoiceByValue(data.multi_selector);
            if (data.multi_selector_midnight) midnightChoicesInstance.setChoiceByValue(data.multi_selector_midnight);
        }
    }


async function saveSettingmember() {
    const ward_id = sessionStorage.getItem("current_ward_id");
    const token = localStorage.getItem("token"); 

    // 取得人數設定
    const required_dayshift = document.getElementById("required_dayshift").value;
    const required_nightshift = document.getElementById("required_nightshift").value;
    const required_midnightshift = document.getElementById("required_midnightshift").value;

    // 從 Choices.js 實例取得選中的人員陣列
    const selectedDayStaff = dayChoicesInstance.getValue(true);
    const selectedNightStaff = nightChoicesInstance.getValue(true);
    const selectedMidnightStaff = midnightChoicesInstance.getValue(true);

    const allSelectedStaff = [...selectedDayStaff, ...selectedNightStaff, ...selectedMidnightStaff];
    const hasDuplicate = new Set(allSelectedStaff).size !== allSelectedStaff.length;

    if(hasDuplicate){
        alert("白班、大小夜包班人員不可出現重複");
        return;
    }

    const payload = {
        "required_dayshift": required_dayshift,
        "required_nightshift": required_nightshift,
        "required_midnightshift": required_midnightshift,
        "multi_selector_day": selectedDayStaff,
        "multi_selector": selectedNightStaff,
        "multi_selector_midnight": selectedMidnightStaff
    };

    // 更新本頁暫存
    sessionStorage.setItem("settingstaffnumber_step3", JSON.stringify(payload));

    window.location.href = `/settingfinal/${ward_id}/`;
    }

function lastpage(){
    const ward_id = sessionStorage.getItem("current_ward_id");
    window.location.href=`/settingmember/${ward_id}`
}
