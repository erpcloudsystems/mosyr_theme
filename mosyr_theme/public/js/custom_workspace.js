frappe.views.Workspace.prototype.setup_workspaces = function (page) {
    this.workspaces = {};
    for (let page of frappe.boot.allowed_workspaces) {
        if (!this.workspaces[page.category]) {
            this.workspaces[page.category] = [];
        }
        this.workspaces[page.category].push(page);
    }

    $(".layout-side-section").css("display", "none")
    $(".sidebar-toggle-btn").css("display", "none")
}