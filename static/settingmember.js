async function getStaffData() {
    const token = localStorage.getItem("token");

    const response = await fetch(`/api/staff`, {
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

        //全選功能
        const selectAllCheckbox = document.querySelector(".checkAll");
        const taskCheckboxes = document.querySelectorAll(".checkbox-name");

        // 監聽全選
        selectAllCheckbox.addEventListener("change", function() {
            taskCheckboxes.forEach(function(checkbox) {
                // 正確做法：將子選框狀態設為跟全選框一致
                checkbox.checked = selectAllCheckbox.checked; 
            });
        });

        // 監聽子選框
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
    window.location.href="/setting"
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
    const token = localStorage.getItem("token"); 
    const year = document.getElementById("select-year").value;
    const month = document.getElementById("select-month").value;
    const selected_date = `${year}-${month}`
    
    //選擇被勾選的id
    const checkedNodes = document.querySelectorAll(".checkbox-name:checked");
    const selectedStaff = Array.from(checkedNodes).map(cb => cb.id);

    if (selectedStaff.length === 0) { 
    alert("請至少選擇一位員工！");
    return; 
}

    const days= window.currentMonthDays;

    const response = await fetch(`/api/settingmember`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        },
        body:JSON.stringify({"selectedDate":selected_date, "selectedStaff":selectedStaff, "days": days})
    });    
    const result = await response.json();
    if (response.ok && result.data !== null){
        alert("儲存成功！");
        window.location.href="/setting1"
    }
}

