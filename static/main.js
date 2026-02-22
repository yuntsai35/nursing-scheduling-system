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

    } else {
      window.location.href = "/";
    }
}
window.addEventListener("load", checkLoginStatus);

function setting() {
    window.location.href = "/setting";
}
function staff() {
    window.location.href = "/staff";
}

