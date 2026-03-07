//標題
const urlParams = new URLSearchParams(window.location.search);
  
const month = urlParams.get('date');
document.querySelector("#reservemonth").textContent=month+"月";

//人名資料scheduled_member
async function getStaffData() {
    const token = localStorage.getItem("token"); 
    const response = await fetch(`/api/reservestaff/${month}`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });
    const result = await response.json();
        
    if (response.ok && result.data) {

        const tablelist = document.querySelector(".tablelist");
        tablelist.innerHTML = ""; // 清空舊內容

        // 建立表頭 (第一列顯示日期數字)
        const thead = document.createElement("thead");
        let headerHtml = `<tr><th>員工姓名</th>`;
        const totalDays = result.data[0][1]; // 取得該月天數 (例如 30)
        for (let i = 1; i <= totalDays; i++) {
            headerHtml += `<th>${i}</th>`;
        }
        headerHtml += `</tr>`;
        thead.innerHTML = headerHtml;
        tablelist.appendChild(thead);

        // 建立表身 (每人一橫行)
        const tbody = document.createElement("tbody");
        result.data.forEach(staff => {
            const tr = document.createElement("tr");
            // staff[2] 是姓名
            let rowHtml = `<td class="name-column">${staff[2]}</td>`;
            
            // 根據天數產生空格子
            for (let i = 1; i <= totalDays; i++) {
                rowHtml += `<td class="date-cell"></td>`;
            }
            tr.innerHTML = rowHtml;
            tbody.appendChild(tr);
        });
        tablelist.appendChild(tbody);
        
    } else {
        console.error("無法取得員工資料:", result.message || "未知錯誤");
    }
}



async function getStaffData() {
    const token = localStorage.getItem("token"); 
    const response = await fetch(`/api/reservestaff/${month}`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });
    const result = await response.json();
        
        if (response.ok && result.data && result.data.length > 0) {
            renderTable(result.data);
        } else {
            console.warn("目前尚無排班資料");
            document.querySelector(".tablelist").innerHTML = "<tr><td>該月份尚無人員資料</td></tr>";
        }
    
}

/**
 * 3. 渲染邏輯：將資料轉換為 HTML 表格結構
 * 資料結構: [staff_id, month_days, full_name, leave_dates]
 */

function renderTable(data) {
    const tablelist = document.querySelector(".tablelist");
    tablelist.innerHTML = ""; // 清空舊內容

    // A. 取得該月總天數 (取第一筆資料的 index 1)
    const totalDays = data[0][1]; 

    // B. 建立 colgroup 固定寬度 (優化 CSS 盒子模型表現)
    const colgroup = document.createElement("colgroup");
    let colHtml = `<col style="width: 120px;">`; // 姓名欄寬度
    for (let i = 1; i <= totalDays; i++) {
        colHtml += `<col style="width: 40px;">`; // 日期格子寬度
    }
    colgroup.innerHTML = colHtml;
    tablelist.appendChild(colgroup);

    // C. 建立表頭 (第一列顯示日期數字)
    const thead = document.createElement("thead");
    let headerHtml = `<tr><th class="name-column">員工姓名</th>`;
    for (let i = 1; i <= totalDays; i++) {
        headerHtml += `<th>${i}</th>`;
    }
    headerHtml += `</tr>`;
    thead.innerHTML = headerHtml;
    tablelist.appendChild(thead);

    // D. 建立表身 (每人一橫行)
    const tbody = document.createElement("tbody");
    data.forEach(staff => {
        const tr = document.createElement("tr");
        
        // 第一欄：員工姓名
        const staffName = staff[2];
        let rowHtml = `<td class="name-column">${staffName}</td>`;
        
        // 處理請假日期：將字串 "5,10" 轉為陣列
        const leaveDatesStr = staff[3] || ""; 
        const leaveArray = leaveDatesStr.split(",").map(d => d.trim());

        // 產生後續的日期填寫格子
        for (let i = 1; i <= totalDays; i++) {
            // 比對當前日期是否在請假清單中
            const isLeave = leaveArray.includes(i.toString()) ? "is-leave" : "";
            rowHtml += `<td class="date-cell ${isLeave}" data-day="${i}"></td>`;
        }
        
        tr.innerHTML = rowHtml;
        tbody.appendChild(tr);
    });
    tablelist.appendChild(tbody);
}
getStaffData();