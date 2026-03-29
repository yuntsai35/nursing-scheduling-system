async function signup(){
    let name = document.querySelector(".signup-name input").value;
    let account = document.querySelector(".signup-account input").value;
    let password = document.querySelector(".signup-password input").value;
    let hint = document.querySelector(".signup-hint")

    if(name === "" ||account === "" || password === ""){
            hint.innerHTML = "姓名、信箱或密碼不可為空格！";
            hint.style.color = "red"; 
        return 
    }
    
    let response=await fetch("/api/user/auth",{
        method:"POST",
        headers: {
            "Content-Type": "application/json"
        },
        body:JSON.stringify({"employee_num":account,"password":password,"name":name})
    });
    let result = await response.json();
    
    if(response.ok){
        hint.innerHTML = "註冊成功！";
        hint.style.color = "green";
        var clock = setTimeout(showlogin , 750);
        function showlogin() {
            const login = document.querySelector(".login-box");
            const signup = document.querySelector(".signup-box");
            
            signup.classList.add("is-hidden");
            login.classList.remove("is-hidden");
        }

        

    }else{
        hint.innerHTML = result.message;
        hint.style.color = "red";
    }
    }

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
         window.location.href = "/index";

    } 
}

function showsignup() {
    const login = document.querySelector(".login-box");
    const signup = document.querySelector(".signup-box");
    
    login.classList.add("is-hidden");
    signup.classList.remove("is-hidden");
}

function showlogin() {
    const login = document.querySelector(".login-box");
    const signup = document.querySelector(".signup-box");
    
    signup.classList.add("is-hidden");
    login.classList.remove("is-hidden");
}

document.addEventListener("DOMContentLoaded", function() {
    const token = localStorage.getItem("token");
    
    if (token) {
        checkLoginStatus();
    }
});