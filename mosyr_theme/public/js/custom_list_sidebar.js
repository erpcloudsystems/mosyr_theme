frappe.views.ListSidebar.prototype.make = function () {
    console.log("vv54545454547544444444445");
    var sidebar_content = frappe.render_template("list_sidebar", { doctype: this.doctype });

    this.sidebar = $('<div class="list-sidebar overlay-sidebar hidden-xs hidden-sm"></div>')
        .html(sidebar_content)
        .appendTo(this.page.sidebar.empty());

    this.setup_list_filter();
    this.setup_list_group_by();

    // do not remove
    // used to trigger custom scripts
    $(document).trigger('list_sidebar_setup');

    if (this.list_view.list_view_settings && this.list_view.list_view_settings.disable_sidebar_stats) {
        this.sidebar.find('.list-tags').remove();
    } else {
        this.sidebar.find('.list-stats').on('click', (e) => {
            this.reload_stats();
        });
    }
}
