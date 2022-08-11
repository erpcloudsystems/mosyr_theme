frappe.views.Workspace.prototype.show = function () {
    this.in_customize_mode = false
    let page =  'Home'//this.get_page_to_show();
    this.page.set_title(`${__(page)}`);
    this.show_page(page);
}

frappe.views.Workspace.prototype.make_page = function(page) {
    page = 'Home'
    $(this.wrapper).find('.sidebar-toggle-btn').remove()
    let $temp = frappe.render_template("workspace", {
        "total_loans_amount": 0,
        "total_salaries_amount": 0,
        "timesheet_list": [],
        "total_leave_encashment_amount": 0,
        "total_employee":0,
        "total_leave_application": 0,
        "approved_leave": 0,
        "total_casual_leave": 0,
        "total_sick_leave": 0,
        "total_leave_without_pay_leave": 0,
        "total_compensatory_leave": 0,
        "growth_persentage": 0,
        "prev_year": '5222',
        "total_employees_in_current_year": 0,
        "total_employees_in_prev_year": 0,
        "current_year_totals_list": 0,
        "prev_year_totals_list": 0,
    });
    $(this.body).html('')
    $($temp).find('#new-tech-support').click(ev => { frappe.new_doc('Technical Support') })
    $($temp).appendTo(this.body);
}

frappe.views.Workspace.prototype.show_or_hide_sidebar = function(){
    $('#page-workspace .layout-side-section').toggleClass('hidden', true);
}
frappe.views.Workspace.prototype.make_sidebar = function(){}
frappe.views.Workspace.prototype.save_customization = function(){}
frappe.views.Workspace.prototype.setup_dropdown = function(){}
frappe.views.Workspace.prototype.customize = function(){}
frappe.views.Workspace.prototype.prepare_container = function() {
    const current = frappe.get_route()
    if(current.length > 1){
        if(current[0] == "Workspaces" && current[1] !== ""){
            location.href = '/app'
        }
    }
    let list_sidebar = $(`
        <div class="list-sidebar overlay-sidebar hidden-xs hidden-sm">
            <div class="desk-sidebar list-unstyled sidebar-menu"></div>
        </div>
    `).appendTo(this.wrapper.find(".layout-side-section"));
    this.sidebar = list_sidebar.find(".desk-sidebar");

    this.body = this.wrapper.find(".layout-main-section");
}
