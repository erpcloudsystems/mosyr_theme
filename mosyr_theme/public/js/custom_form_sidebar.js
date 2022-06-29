
frappe.ui.form.Sidebar.prototype.make = function () {
    var sidebar_content = frappe.render_template("list_sidebar", { doctype: frappe.boot.sidebar_items });

    this.sidebar = $('<aside class="list-sidebar layout-menu menu-vertical menu bg-menu-theme"></aside>')
        .html(sidebar_content)
        .appendTo(this.page.sidebar.empty());

    this.comments = this.sidebar.find(".form-sidebar-stats .comments");
    this.user_actions = this.sidebar.find(".user-actions");
    this.image_section = this.sidebar.find(".sidebar-image-section");
    this.image_wrapper = this.image_section.find('.sidebar-image-wrapper');
    this.make_assignments();
    this.make_attachments();
    this.make_review();
    this.make_shared();

    this.make_tags();
    this.make_like();
    this.make_follow();

    this.bind_events();
    this.setup_keyboard_shortcuts();
    this.show_auto_repeat_status();
    frappe.ui.form.setup_user_image_event(this.frm);

    this.refresh();
}
