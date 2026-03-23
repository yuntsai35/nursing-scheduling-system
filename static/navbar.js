function logout() {
    localStorage.removeItem("token");
    window.location.href = "/";
}

function getCurrentWard(){
    const wardId = sessionStorage.getItem("current_ward_id");
    if (!wardId) {
        window.location.href = "/index";
    }
    return wardId;
}

function setting() {
    const wardId = getCurrentWard();
    window.location.href = `/setting/${wardId}`;
}

function staff() {
   const wardId = getCurrentWard();
    window.location.href =`/staff/${wardId}`;}

function set() {
    const wardId = getCurrentWard();
    window.location.href = `/setting1/${wardId}`;
   }

function mainreservebreak() {
    const wardId = getCurrentWard();
    window.location.href = `/mainreservebreak/${wardId}`;
}

function mainfinalscheduling() {
    const wardId = getCurrentWard();
    window.location.href = `/mainfinalscheduling/${wardId}`;
}
function main(){
    const wardId= getCurrentWard();
    window.location.href = `/main/${wardId}`;
}