async function checkAccess() {
    const path = window.location.pathname;
    
    if (path === "/index" || path === "/membership") {
        return; 
    }

    const pathSegments = window.location.pathname.split('/');
    const currentWardId = pathSegments.pop();

    if (isNaN(currentWardId)) {
        return;
    }

    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "/login";
        return;
    }

    try {
        const response = await fetch("/api/member_ward", {
            headers: { "Authorization": `Bearer ${token}` }
        });

        const result = await response.json();
        const myWards = result.data;

        const currentAccess = myWards.find(item => item.ward_id == currentWardId);

        if (!currentAccess) {
            alert("您不屬於此病房群組！");
            window.location.href = "/index";
        } else {
            sessionStorage.setItem("current_role", currentAccess.role);
            sessionStorage.setItem("current_ward_id", currentAccess.ward_id);
            sessionStorage.setItem("current_ward_name", currentAccess.ward_name);
        }
    } catch (error) {
        console.error(error);
        window.location.href = "/index";
    }
}
checkAccess();

function getCurrentWard(){
    const path = window.location.pathname;
    
    if (path === "/index" || path === "/membership") {
        return; 
    }
    const wardId = sessionStorage.getItem("current_ward_id");
    if (!wardId) {
        window.location.href = "/index";
    }
    return wardId;
}
getCurrentWard();
