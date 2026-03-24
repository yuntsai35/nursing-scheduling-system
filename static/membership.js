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


window.addEventListener("load", () => {
    checkLoginStatus();
    memberinfo(); 
});

async function memberinfo() {
    const token = localStorage.getItem("token");
    
    const nameInput = document.querySelector(".changename");

    try {
        const response = await fetch("/api/memberinfo", {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` }
        });

        const result = await response.json();

        if (response.ok && result.data) {
            
            document.getElementById("current-name").textContent = result.data.name;
            document.getElementById("current-employee-num").textContent = result.data.employee_num;
            

            
        } else {
        }
    } catch (error) {
        console.error("JS 執行過程發生錯誤:", error);
    }
}


async function saveMembership() {
    const token = localStorage.getItem("token");
    const nameValue = document.querySelector(".changename").value;
    const oldPassword = document.querySelector(".changeoldpassword").value;
    const newPassword = document.querySelector(".changenewpassword").value;
    
    const nameHint = document.getElementById("name-hint");
    const passwordHint = document.getElementById("password-hint");

    nameHint.textContent = "";
    passwordHint.textContent = "";

    let updateData = {};

    if (nameValue.trim() !== "") {
        updateData.name = nameValue;
    }

    if (oldPassword || newPassword) {
        if (!oldPassword || !newPassword) {
            passwordHint.textContent = "修改密碼需同時輸入新舊密碼";
            passwordHint.style.color = "red";
            return; 
        }
        updateData.oldpassword = oldPassword;
        updateData.newpassword = newPassword;
    }

    if (Object.keys(updateData).length === 0) {
        alert("請至少輸入一項要修改的內容");
        return;
    }

    try {
        const response = await fetch("/api/membership", {
            method: "PATCH",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(updateData) 
        });

        const result = await response.json();

        if (response.ok) {
            alert(result.message || "修改成功");
            memberinfo(); 
            document.querySelector(".changeoldpassword").value = "";
            document.querySelector(".changenewpassword").value = "";
        } else {
            passwordHint.textContent = result.message;
            passwordHint.style.color = "red";
        }
    } catch (error) {
        console.error("更新失敗:", error);
    }
}