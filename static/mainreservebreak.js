async function getReserveMonth() {

    const token = localStorage.getItem("token");
    const response = await fetch(`/api/date`, {
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
            newDiv.textContent = item+"護理人力預假班表";
            newDiv.className = "date-card";
            newDiv.onclick = function() {
                reservebreak(item);
            };
            dateSelect.appendChild(newDiv);
        });
    } else {
        console.error("無法取得員工資料");
    }
}
getReserveMonth();

function reservebreak(date) {
    window.location.href = `/reservebreak?date=${date}`;
}

