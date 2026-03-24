function logout() {
    localStorage.removeItem("token");
    window.location.href = "/";
}

function getCurrentWard(){
    const wardId = sessionStorage.getItem("current_ward_id");
    if (!wardId) {
        window.location.href = "/index";
    }
    return wardId;
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
            
            const setting = document.querySelector("#setting");
            const autocalendar = document.querySelector("#staffmanagement");
            const step3 = document.querySelector("#step3");

            setting.style.display = "none";
            autocalendar.style.display = "none";
            step3.style.display="none";
            navbarsetting.style.display = "none";
            navbarautocalendar.style.display = "none";
        }
      
    } else {
      window.location.href = "/";
    }
}
window.addEventListener("load", checkLoginStatus);


async function getStaffData() {
    const ward_id = sessionStorage.getItem("current_ward_id");
    const token = sessionStorage.getItem("token");

    const response = await fetch(`/api/ward/${ward_id}/staff`, {
        headers: { "Authorization": `Bearer ${token}` }
    });

    const result = await response.json();
    if (response.ok) {
        renderTable(result.data); // 每次都拿最新的渲染
    }
}
getStaffData()

