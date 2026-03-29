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


//標題
const urlParams = new URLSearchParams(window.location.search);
const month = urlParams.get('date');
document.querySelector("#reservemonth").textContent=month+"月";

//人名資料scheduled_member
async function getStaffData() {
    const ward_id = sessionStorage.getItem("current_ward_id");
    const token = localStorage.getItem("token"); 
    const response = await fetch(`/api/ward/${ward_id}/finalstaff/${month}`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });
    const result = await response.json();
        
    if (response.ok && result.data && result.data.length > 0) {
        const tablelist = document.querySelector(".tablelist");
        tablelist.innerHTML = "";

        const shiftMap = { 0: "休", 1: "D", 2: "E", 3: "N" };

        // 產生表頭
        const thead = document.createElement("thead");
        let firstRow = `<tr><th class="staff">員工姓名</th>`;
        
        // 取得該月份的第一天，用來計算星期
        // 假設 month 變數內容是 "2026-3"
        const baseDate = dayjs(month, "YYYY-M"); 
        const daysInMonth = baseDate.daysInMonth();

        for (let i = 1; i <= daysInMonth; i++) {
            // 計算該日期的星期縮寫 (Mon, Tue...)
            const dayOfWeek = baseDate.date(i).format("ddd"); 
            
            // 將日期與星期組合顯示
            firstRow += `<th>${i}<br><small>${dayOfWeek}</small></th>`;
        }
        firstRow += `</tr>`;
        thead.innerHTML = firstRow;
        tablelist.appendChild(thead);

        // 產生表格內容
        const tbody = document.createElement("tbody");
        let allnameRows = "";

        result.data.forEach(namelist => {
            let nameRow = `<tr><td class="staff">${namelist.full_name}<br>${namelist.level}</td>`;
            const schedule = namelist.schedule_date;

            for (let b = 1; b <= daysInMonth; b++) {
                const shiftValue = schedule[b.toString()]; 
                let displayText = (shiftValue !== undefined) ? shiftMap[shiftValue] : "";
                
                let cellStyle = "";
                if(shiftValue===0){
                    cellStyle = 'color: #e03131; font-weight: bold;'
                }else if(shiftValue===1){
                    cellStyle = 'background-color: #fff9db;border-radius:12px;'

                }else if(shiftValue===2){
                    cellStyle = 'background-color: #fff4e6;border-radius:12px;'

                }else if(shiftValue===3){
                    cellStyle = 'background-color: #edf2ff;border-radius:12px;'
                }
        

                nameRow += `<td id="day-${b}" style="${cellStyle}">${displayText}</td>`;
            }
            nameRow += `</tr>`;
            allnameRows += nameRow;
        }); 
        
        tbody.innerHTML = allnameRows;
        tablelist.appendChild(tbody);
    }
}
getStaffData();