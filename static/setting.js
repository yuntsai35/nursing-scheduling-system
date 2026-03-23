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

const default_time = {
    min_rest_2w: "4",
    min_rest_1m: "8",
    max_continuous_work: "6",
    max_shifts_1w: "3"
};

function loadsettingtime() {
    const settingtime = sessionStorage.getItem("settingtime_step1");
    let data;

    if (settingtime == null) {
        data = default_time;
    } else {
        data = JSON.parse(settingtime);
    }
    document.getElementById("min_rest_2w").value = data.min_rest_2w;
    document.getElementById("min_rest_1m").value = data.min_rest_1m;
    document.getElementById("max_continuous_work").value = data.max_continuous_work;
    document.getElementById("max_shifts_1w").value = data.max_shifts_1w;
}
loadsettingtime();

async function saveSettingtime(){
    const data = {
        "min_rest_2w": document.getElementById("min_rest_2w").value,
        "min_rest_1m": document.getElementById("min_rest_1m").value,
        "max_continuous_work": document.getElementById("max_continuous_work").value,
        "max_shifts_1w": document.getElementById("max_shifts_1w").value
    };
    
    sessionStorage.setItem("settingtime_step1", JSON.stringify(data));
    
    const ward_id = sessionStorage.getItem("current_ward_id");
    window.location.href = `/settingmember/${ward_id}`;
}