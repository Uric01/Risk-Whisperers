document.addEventListener("DOMContentLoaded", () => {
    // If we're on login page, don't execute role parsing since we assume it's pre-auth
    if(window.location.pathname.includes('login.html')) return;

    // Get the mocked role from local browser storage (set during login)
    const role = localStorage.getItem("userRole") || "viewer";
    
    // Dynamically update the profile name in the top-right nav bar
    const userDisplay = document.getElementById("navUserDisplay");
    if(userDisplay) {
        userDisplay.innerHTML = `<i class="bi bi-person-circle me-1"></i> ${role === 'admin' ? 'Admin User' : 'Read-Only User'}`;
    }

    // Process read-only restrictions
    if (role === "viewer") {
        // Globally hide any elements tagged as admin-only
        const adminElements = document.querySelectorAll(".admin-only");
        adminElements.forEach(el => el.style.display = "none");
        
        // Prevent direct URL navigation to write/restrict-pages for read-only users
        const restrictedPages = ['assets.html', 'risks.html', 'add_', 'audit_logs.html'];
        const isRestricted = restrictedPages.some(page => window.location.pathname.includes(page));
        if (isRestricted) {
            alert("Access Denied: Your Read-Only role does not have access to this module. Returning to Dashboard.");
            window.location.href = 'dashboard.html';
        }
    }
});
