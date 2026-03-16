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

function setting() {
    window.location.href = "/setting";
}

function staff(role) {
   if (role == generalstaff){
    window.location.href ="/staff?role=generalstaff";}
}
function set(role) {
    if (role == generalstaff){
    window.location.href ="/setting1";
   }
}
function mainreservebreak() {
    window.location.href = "/mainreservebreak";
}

function mainfinalscheduling() {
    window.location.href = "/mainfinalscheduling";
}
function main(){
    Window.location.herf="/"
}