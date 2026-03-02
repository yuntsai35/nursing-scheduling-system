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

            const container1 = document.querySelector("#container1");
            const setting = document.querySelector("#setting");
            const autocalendar = document.querySelector("#autocalendar");

            container1.style.display = "none";
            setting.style.display = "none";
            autocalendar.style.display = "none";
        }else if (userRole === "IT_Admin") {
            
            const container2 = document.querySelector("#container2");
            container2.style.display = "none";
        }
      

    } else {
      window.location.href = "/";
    }
}
window.addEventListener("load", checkLoginStatus);

function setting() {
    window.location.href = "/setting";
}

function staff(role) {
    if (role == generalstaff){
    window.location.href ="/staff?role=generalstaff";
   }else if((role == adminstaff)){
    
    window.location.href="/staff?role=adminstaff";

   }
}
function set(role) {
    if (role == generalstaff){
    window.location.href ="/setting1";
   }
}

