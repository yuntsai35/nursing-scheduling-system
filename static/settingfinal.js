function logout() {
    localStorage.removeItem("token");
    sessionStorage.clear();
    window.location.href = "/";
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
      window.location.href = "/";
    }
}
window.addEventListener("load", checkLoginStatus);


function renderPreview() {
    const ward_id = sessionStorage.getItem("current_ward_id");
    const step1 = JSON.parse(sessionStorage.getItem("settingtime_step1"));
    const step2 = JSON.parse(sessionStorage.getItem("settingmember_step2"));
    const step3 = JSON.parse(sessionStorage.getItem("settingstaffnumber_step3"));

    if (!step1 || !step2 || !step3) {
        alert("設定資料不完整，請重新設定。");
        window.location.href=`/main/${ward_id}`;
    }
    // settingtime
    document.getElementById("final-min-rest-2w").textContent = step1.min_rest_2w;
    document.getElementById("final-min-rest-1m").textContent = step1.min_rest_1m;
    document.getElementById("final-max-work").textContent = step1.max_continuous_work;
    document.getElementById("final-max-shifts").textContent = step1.max_shifts_1w;

    // settingdate
    const [year, month] = step2.selectedDate.split("-");
    document.getElementById("final-year").textContent = `${year}年`;
    document.getElementById("final-month").textContent = `${month}月`;
    document.getElementById("final-days-info").textContent = `(共 ${step2.days} 天)`;

    // settingmember
    const staffContainer = document.querySelector(".container-setting"); 
    staffContainer.innerHTML = "";
    if (step2.selectedStaff && step2.selectedStaff.length > 0) {
       
        step2.selectedStaff.forEach(staff => {
            const nameDiv = document.createElement("div");
            nameDiv.className = "formGroup"; 
            nameDiv.textContent = staff.name; 
            staffContainer.appendChild(nameDiv);
        });
    } else {
        staffContainer.textContent = "尚未選擇人員";
    }

    // setting staff number
    document.getElementById("final-day-required").textContent = step3.required_dayshift;
    document.getElementById("final-night-required").textContent = step3.required_nightshift;
    document.getElementById("final-midnight-required").textContent = step3.required_midnightshift;

    // 包班人員
    const packageContainer = document.querySelectorAll(".container-setting")[1]; 
    packageContainer.innerHTML = `
        <div>小夜包班：${step3.multi_selector.join(", ") || "無"}</div>
        <div>大夜包班：${step3.multi_selector_midnight.join(", ") || "無"}</div>
    `;
}
renderPreview();

function lastpage(){
    const ward_id = sessionStorage.getItem("current_ward_id");
    window.location.href=`/setting1/${ward_id}`
}

async function saveSettingmember() {
    const ward_id = sessionStorage.getItem("current_ward_id");
    const token = localStorage.getItem("token");

    const step1 = JSON.parse(sessionStorage.getItem("settingtime_step1"));
    const step2 = JSON.parse(sessionStorage.getItem("settingmember_step2"));
    const step3 = JSON.parse(sessionStorage.getItem("settingstaffnumber_step3"));

  
    if (!step1 || !step2 || !step3) {
        alert("設定資料不完整，請重新檢查各個步驟。");
        return;
    }

    const data = {
        // settingtime
        "min_rest_2w": step1.min_rest_2w,
        "min_rest_1m": step1.min_rest_1m,
        "max_continuous_work": step1.max_continuous_work,
        "max_shifts_1w": step1.max_shifts_1w,

        // settingdate
        "selectedDate": step2.selectedDate,
        "selectedStaff": step2.selectedStaff.map(s => s.id), 
        "days": step2.days,

        // setting staff number
        "required_dayshift": step3.required_dayshift,
        "required_nightshift": step3.required_nightshift,
        "required_mignightshift": step3.required_midnightshift, 
        "multi_selector": step3.multi_selector,
        "multi_selector_midnight": step3.multi_selector_midnight
    };

    try {
        const response = await fetch(`/api/ward/${ward_id}/setting`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok && result.ok) {
            alert("所有排班設定已成功儲存！");
            
            sessionStorage.removeItem("settingtime_step1");
            sessionStorage.removeItem("settingmember_step2");
            sessionStorage.removeItem("settingstaffnumber_step3");
            
            window.location.href = `/main/${ward_id}`;
        } else {
            alert("儲存失敗：" + (result.message || "未知錯誤"));
        }
    } catch (error) {
        console.error("發送請求時發生錯誤：", error);
        alert("伺服器連線失敗，請稍後再試。");
    }
}



