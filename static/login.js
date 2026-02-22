async function login(){
    let account = document.querySelector(".account input").value;
    let password = document.querySelector(".password input").value;
    let hint = document.querySelector(".hint")

    if(account === "" || password === ""){
            hint.innerHTML = "姓名、信箱或密碼不可為空格！";
            hint.style.color = "red"; 
        return 
    }
    
    let response=await fetch("/api/user/auth",{
        method:"PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body:JSON.stringify({"employee_num":account,"password":password})
    });
    let result = await response.json();
    
    if(response.ok){
        localStorage.setItem('token', result.token);
        checkLoginStatus();
    }else{
        hint.innerHTML = result.message;
        hint.style.color = "red";
    }
    }

async function checkLoginStatus() {
    const token = localStorage.getItem("token"); 
    const authText = document.getElementById("item"); 

    let response = await fetch("/api/user/auth", {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}` 
        }
    });

    const result = await response.json();

    if (response.ok && result.data !== null) {
         window.location.href = "/main";

    } else {
        window.location.href = "/";
    }
}
