async function saveSettingtime(){
    const token = localStorage.getItem("token"); 
    const min_shift_interval= document.getElementById("min_shift_interval").value;
    const min_rest_2w= document.getElementById("min_rest_2w").value;
    const min_rest_1m= document.getElementById("min_rest_1m").value;
    const max_hours_1w= document.getElementById("max_hours_1w").value;
    const max_hours_1d= document.getElementById("max_hours_1d").value;
    const max_continuous_work= document.getElementById("max_continuous_work").value;
    const max_shifts_1w= document.getElementById("max_shifts_1w").value;

 
    const response = await fetch(`/api/settingtime`, {
        method: "PATCH",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        },
        body:JSON.stringify({"min_shift_interval":min_shift_interval, "min_rest_2w":min_rest_2w, "min_rest_1m":min_rest_1m, "max_hours_1w":max_hours_1w, "max_hours_1d":max_hours_1d, "max_continuous_work":max_continuous_work, "max_shifts_1w":max_shifts_1w})
    });    
    const result = await response.json();
    if (response.ok && result.data !== null){
        window.location.href="/settingmember"
    }
}

async function getSettingtime(){
    const token = localStorage.getItem("token"); 
    const response = await fetch(`/api/settingtime`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });    
    const result = await response.json();

    if (response.ok && result.data !== null){
        document.getElementById("min_shift_interval").value = result.data.min_shift_interval;
        document.getElementById("min_rest_2w").value = result.data.min_rest_2w;
        document.getElementById("min_rest_1m").value = result.data.min_rest_1m; 
        document.getElementById("max_hours_1w").value = result.data.max_hours_1w;
        document.getElementById("max_hours_1d").value = result.data.max_hours_1d;
        document.getElementById("max_continuous_work").value = result.data.max_continuous_work;
        document.getElementById("max_shifts_1w").value = result.data.max_shifts_1w;
    }
}
getSettingtime();