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


async function getReserveMonth() {
    const ward_id = sessionStorage.getItem("current_ward_id");
    const token = localStorage.getItem("token");
    const response = await fetch(`/api/ward/${ward_id}/date`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });
    const results = await response.json();
    if (response.ok){
        const dateSelect = document.querySelector(".month-group");
        const result = results.data.date;

        result.forEach(item => {
            const newDiv = document.createElement("div");
            newDiv.textContent = item+"護理人力預假班表";
            newDiv.className = "date-card";
            newDiv.onclick = function() {
                reservebreak(item);
            };
            dateSelect.appendChild(newDiv);
        });
    } else {
        console.error("無法取得員工資料");
    }
}
getReserveMonth();

function reservebreak(date) {
    const ward_id = sessionStorage.getItem("current_ward_id");
    window.location.href = `/reservebreak/${ward_id}?date=${date}`;
}
