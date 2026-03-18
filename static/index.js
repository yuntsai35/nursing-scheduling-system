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
    if (!token) {
        window.location.href = "/";
        return;
    }

    const result = await response.json();

    if (response.ok && result.data !== null) {
      document.querySelector("#username").textContent = result.data.full_name;
      
    } else {
      window.location.href = "/";
    }
}
window.addEventListener("load", checkLoginStatus);

/*開關小視窗 */
function closeAddPage() {
    const mainInput = document.querySelector(".main-input");
    mainInput.style.display = 'none';   
    document.body.style.overflow = "auto";
}

function openAddPage(){
    const mainInput = document.querySelector(".main-input");
    mainInput.style.display = 'block';   
    document.body.style.overflow = "hidden";

}

/*新增病房名*/
async function addWard() {
    const token = localStorage.getItem("token");
    const addward=document.querySelector(".addward").value;
    const hint=document.querySelector(".main-input-hint");
    if (!token) {
        window.location.href = "/";
        return;
    }


    let response = await fetch("/api/ward", {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json" 
        },body:JSON.stringify({"ward_name":addward})
    });

    const result = await response.json();

    if (response.ok) {
        alert("新增成功！");
        window.location.reload();
    } else {
        hint.textContent =result.message
        hint.style.color = "red";
}
}


async function getmember_ward() {
    const token = localStorage.getItem("token");

    let response = await fetch("/api/member_ward", {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}` 
        }
    });
    if (!token) {
        window.location.href = "/";
        return;
    }

    const result = await response.json();

    if (response.ok && result.data !== null) {
        const mainContainer=document.querySelector(".main-container");
        const role = {
            'Head_Nurse': '護理長',
            'Staff_Nurse': '護理師'
        };

        result.data.forEach(item=> {
            const wardCard = document.createElement("div");
            wardCard.className = "container-bottom";
            
            
            wardCard.onclick = function() {
                sessionStorage.setItem("current_role", item.role);
                sessionStorage.setItem("current_ward_id", item.ward_id);
                window.location.href = "/main"; 
            };
            wardCard.innerHTML=`
            <div style="display:flex; ">
            <span class="material-symbols-outlined" id="icon" style="margin-right:10px;">flare</span>
            <div>
            <div class="container-bottom-text" id="autocalendar" style="display:flex; align-items: center;font-weight: bold;">${item.ward_name}</div>
            <div  class="container-bottom-explain">${role[item.role]}</div>
            </div>
            </div>`;
            mainContainer.appendChild(wardCard);    
        
        });

    } else {
      window.location.href = "/";
    }
}
getmember_ward();

async function deleteWard(wardId) {
    if (!confirm("確定要刪除此病房嗎？")) return;

    const token = localStorage.getItem("token");
    const response = await fetch("/api/member_ward", {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ "ward_id": wardId })
    });

    if (response.ok) {
        alert("刪除成功");
        window.location.reload();
    } else {
        const result = await response.json();
        alert(result.message);
    }
}