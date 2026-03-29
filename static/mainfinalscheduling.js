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


async function getfinal() {
    const ward_id = sessionStorage.getItem("current_ward_id");
    const token = localStorage.getItem("token");
    const response = await fetch(`/api/ward/${ward_id}/finalmonth`, {
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
            newDiv.textContent = item+"月 護理人力班表";
            newDiv.className = "date-card";
            newDiv.style.cursor="pointer";
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
    const ward_id = sessionStorage.getItem("current_ward_id");
    window.location.href = `/finalscheduling/${ward_id}?date=${date}`;
}
