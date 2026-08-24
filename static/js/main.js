document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("employerSidebar");
    const overlay = document.getElementById("employerSidebarOverlay");
    const openButtons = [document.getElementById("sidebarToggle"), document.getElementById("sidebarMenuBtn")];
    const closeButtons = [document.getElementById("sidebarCloseBtn"), document.getElementById("sidebarClose")];

    function openSidebar() {
        if (sidebar) sidebar.classList.add("active");
        if (overlay) overlay.classList.add("active");
    }
    function closeSidebar() {
        if (sidebar) sidebar.classList.remove("active");
        if (overlay) overlay.classList.remove("active");
    }
    openButtons.forEach(function (button) { if (button) button.addEventListener("click", openSidebar); });
    closeButtons.forEach(function (button) { if (button) button.addEventListener("click", closeSidebar); });
    if (overlay) overlay.addEventListener("click", closeSidebar);
});
