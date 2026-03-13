//標題
const urlParams = new URLSearchParams(window.location.search);
const month = urlParams.get('date');
document.querySelector("#reservemonth").textContent=month+"月";

// 頁面載入時先初始化空的 Choices
document.addEventListener('DOMContentLoaded', function() {
    leaveChoicesInstance = new Choices('#choices-multiple-remove-button', {
        removeItemButton: true,
        placeholderValue: '請選擇預假日期'
    });
});


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
        
        if (response.ok && result.data && result.data.length > 0) {
            //日期選項
            const dateChoices = [];
            for (let date = 1; date <= result.data[0].schedule_date; date++) {
            dateChoices.push({
                value: date.toString(),
                label: `${date}號`,
                selected: false,
                disabled: false
            });}
            leaveChoicesInstance.setChoices(dateChoices, 'value', 'label', true);

            //第一行
            tablelist=document.querySelector(".tablelist")
            tablelist.innerHTML = "";
            thead=document.createElement("thead")
            let firstRow=`<tr><th class="staff">員工姓名</th>`;
            for (let i = 1; i < result.data[0].schedule_date+1; i++) {
                    firstRow += `<th>${i}</th>`
                }
            firstRow += `</tr>`;
            thead.innerHTML = firstRow;
            tablelist.appendChild(thead);

            //表格員工每列
            const tbody = document.createElement("tbody");
            let allnameRows="";
            result.data.forEach(namelist => {
                let nameRow=`<tr><td class="staff">${namelist.full_name}</td>`;
                if(namelist.leave_dates === null){
                for (let b = 1; b < result.data[0].schedule_date+1; b++) {
                    nameRow +=`<td id="${b}"></td>`;
                }
                }else{
                    const listarray=namelist.leave_dates.split(",")
                    for (let b = 1; b < result.data[0].schedule_date+1; b++) {
                        if (listarray.includes(String(b))) {
                        nameRow += `<td id="${b}">假</td>`;
                        } else {
                            nameRow += `<td id="${b}"></td>`;
                        }   
                    }}
                    nameRow+=`</tr>`;
                    allnameRows += nameRow;
            }); 
            tbody.innerHTML = allnameRows;
            tablelist.appendChild(tbody);
        };
}
getStaffData();

async function updateleavedates(){
    const token = localStorage.getItem("token"); 
    const leave_dates= leaveChoicesInstance.getValue(true);
    const reserve_dates = leave_dates.join(",");
    const response = await fetch(`/api/settingReserveBreak`, {
        method: "PATCH",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        },
        body:JSON.stringify({"reserve_dates":reserve_dates,"schedule_id":month})
    });
    const result = await response.json();
        
    if (response.ok && result.ok){
        window.location.reload();
    }
}