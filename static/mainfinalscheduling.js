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


async function getfinal() {

    const token = localStorage.getItem("token");
    const response = await fetch(`/api/finalmonth`, {
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
            newDiv.textContent = item+"護理人力班表";
            newDiv.className = "date-card";
            newDiv.onclick = function() {
                final(item);
            };
            dateSelect.appendChild(newDiv);
        });
    } else {
        console.error("無法取得員工資料");
    }
}
getfinal();

function final(date) {
    window.location.href = `/finalscheduling?date=${date}`;
}

