
$.extend(frappe.router, {
    convert_to_standard_route: function (route) {
        // /app/settings = ["Workspaces", "Settings"]
        // /app/user = ["List", "User"]
        // /app/user/view/report = ["List", "User", "Report"]
        // /app/user/view/tree = ["Tree", "User"]
        // /app/user/user-001 = ["Form", "User", "user-001"]
        // /app/user/user-001 = ["Form", "User", "user-001"]
        // /app/event/view/calendar/default = ["List", "Event", "Calendar", "Default"]
        if (frappe.workspaces[route[0]]) {
            // workspace
            route = ['Workspaces', 'Home'];
        } else if (this.routes[route[0]]) {
            // route
            route = this.set_doctype_route(route);
        }

        return route;
    }
})