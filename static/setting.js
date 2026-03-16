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


async function saveSettingtime(){
    const token = localStorage.getItem("token"); 
    const min_rest_2w= document.getElementById("min_rest_2w").value;
    const min_rest_1m= document.getElementById("min_rest_1m").value;
    const max_continuous_work= document.getElementById("max_continuous_work").value;
    const max_shifts_1w= document.getElementById("max_shifts_1w").value;

 
    const response = await fetch(`/api/settingtime`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        },
        body:JSON.stringify({"min_rest_2w":min_rest_2w, "min_rest_1m":min_rest_1m,"max_continuous_work":max_continuous_work, "max_shifts_1w":max_shifts_1w})
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
        document.getElementById("min_rest_2w").value = result.data.min_rest_2w;
        document.getElementById("min_rest_1m").value = result.data.min_rest_1m; 
        document.getElementById("max_continuous_work").value = result.data.max_continuous_work;
        document.getElementById("max_shifts_1w").value = result.data.max_shifts_1w;
    }
}
getSettingtime();