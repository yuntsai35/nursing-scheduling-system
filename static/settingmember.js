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


async function getStaffData() {
    const token = localStorage.getItem("token");
    const ward_id = sessionStorage.getItem("current_ward_id");

    const response = await fetch(`/api/ward/${ward_id}/staff`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });
    
    const result = await response.json();
        
    if (response.ok){
        const container = document.querySelector(".container-setting");
        
        container.innerHTML = "";
        const staffList = result.data; 

        staffList.forEach(staff => {
            const div = document.createElement("div");
                div.className = "checkbox-group";
            div.innerHTML = 
              `
                <input type="checkbox" id="${staff.id}" class="checkbox-name" name="${staff.full_name}" />
                <label for="${staff.full_name}">${staff.full_name}</label>
            `;
            container.appendChild(div);
        });

        const selectAllCheckbox = document.querySelector(".checkAll");
        const taskCheckboxes = document.querySelectorAll(".checkbox-name");

        selectAllCheckbox.addEventListener("change", function() {
            taskCheckboxes.forEach(function(checkbox) {
                checkbox.checked = selectAllCheckbox.checked; 
            });
        });

        taskCheckboxes.forEach(function(checkbox) {
            checkbox.addEventListener("change", function() {
                const allSelected = Array.from(taskCheckboxes).every(cb => cb.checked);
                selectAllCheckbox.checked = allSelected;
            });
        });
    } else {
        console.error("無法取得員工資料");
    }
}
getStaffData();

function lastpage(){
    const ward_id = sessionStorage.getItem("current_ward_id");
    window.location.href=`/setting/${ward_id}`
}

function initDateSelector() {
    const yearSelect = document.getElementById("select-year");
    const monthSelect = document.getElementById("select-month");
    const daysInfo = document.getElementById("days-info");

    const currentYear = dayjs().year(); 
    const currentMonth = dayjs().month() + 1;
    const all_months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];

    const select_month = {
        [currentYear]: all_months.slice(currentMonth - 1),
        [currentYear + 1]: all_months
    };
    
    // 年份
    yearSelect.innerHTML = "";
    [currentYear, currentYear + 1].forEach(y => {
        yearSelect.options.add(new Option(`${y}年`, y));
    });
    //月份
    function updateMonthOptions() {
        const selectedYear = yearSelect.value;
        const availableMonths = select_month[selectedYear];
        
        monthSelect.innerHTML = "";
        availableMonths.forEach(m => {
            monthSelect.options.add(new Option(`${m}月`, m));
        });
        
        updateDays();
    }

    function updateDays() {
        const year = yearSelect.value;
        const month = monthSelect.value;
        if (year && month) {
            const daysInMonth = dayjs(`${year}-${month}`).daysInMonth();
            daysInfo.innerText = `(共 ${daysInMonth} 天)`;
            window.currentMonthDays = daysInMonth; 
        }
    }

    yearSelect.addEventListener("change", updateMonthOptions);
    monthSelect.addEventListener("change", updateDays);

    updateMonthOptions();
}
initDateSelector();

async function saveSettingmember(){
    const ward_id = sessionStorage.getItem("current_ward_id");
    const token = localStorage.getItem("token"); 
    const year = document.getElementById("select-year").value;
    const month = document.getElementById("select-month").value;
    const selected_date = `${year}-${month}`
    
    //選擇被勾選的id
    const checkedNodes = document.querySelectorAll(".checkbox-name:checked");
    const selectedStaff = Array.from(checkedNodes).map(cb => ({
        id: cb.id,
        name: cb.getAttribute('name')
    }));

    if (selectedStaff.length === 0) { 
    alert("請至少選擇一位員工！");
    return; 
}

    const days= window.currentMonthDays;

    const data={"selectedDate":selected_date, "selectedStaff":selectedStaff, "days": days}
    sessionStorage.setItem("settingmember_step2", JSON.stringify(data));
    
    window.location.href = `/setting1/${ward_id}`;

}