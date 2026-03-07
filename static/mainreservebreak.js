const { createElement } = require("react");

async function getStaffData() {

    const token = localStorage.getItem("token");
    const response = await fetch(`/api/staff`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });
    const result = await response.json();
    if (response.ok){
      table=document.createElement("table");
      
        
      
    } else {
        console.error("無法取得員工資料");
    }
}
getStaffData();
