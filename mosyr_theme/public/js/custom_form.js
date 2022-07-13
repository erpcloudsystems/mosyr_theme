frappe.ui.form.Form.prototype.setup = function() {
    this.fields = [];
    this.fields_dict = {};
    this.state_fieldname = frappe.workflow.get_state_fieldname(this.doctype);

    // wrapper
    this.wrapper = this.parent;
    this.$wrapper = $(this.wrapper);
    frappe.ui.make_app_page({
        parent: this.wrapper,
        single_column: this.meta.hide_toolbar
    });
    this.page = this.wrapper.page;
    this.layout_main = this.page.main.get(0);

    this.toolbar = new frappe.ui.form.Toolbar({
        frm: this,
        page: this.page
    });

    // navigate records keyboard shortcuts
    this.add_form_keyboard_shortcuts();

    // 2 column layout
    this.setup_std_layout();

    // client script must be called after "setup" - there are no fields_dict attached to the frm otherwise
    this.script_manager = new frappe.ui.form.ScriptManager({
        frm: this
    });
    this.script_manager.setup();
    this.watch_model_updates();

    if (!this.meta.hide_toolbar && frappe.boot.desk_settings.timeline) {
        this.footer = new frappe.ui.form.Footer({
            frm: this,
            parent: $('<div>').appendTo(this.page.main.parent())
        });
        $("body").attr("data-sidebar", 1);
    }
    this.setup_file_drop();
    this.setup_doctype_actions();
    this.setup_notify_on_rename();
    
    $(".form-footer").addClass("container-xxl flex-grow-1 container-p-y")

    $(".form-page .form-section").removeClass("row")

    $(".layout-side-section").css("display", "none")

    this.setup_done = true;
}