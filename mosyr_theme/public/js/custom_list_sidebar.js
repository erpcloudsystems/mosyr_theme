frappe.views.ListSidebar.prototype.make = function () {
    
    var sidebar_content = frappe.render_template("list_sidebar", { doctype: frappe.boot.sidebar_items });

    this.sidebar = $('<aside class="list-sidebar layout-menu menu-vertical menu bg-menu-theme"></aside>')
        .html(sidebar_content)
        .appendTo(this.page.sidebar.empty());

}
