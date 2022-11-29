frappe.views.Workspace.prototype.show = function () {
    this.in_customize_mode = false
    let page =  'Home'//this.get_page_to_show();
    this.page.set_title(`${__(page)}`);
    this.show_page(page);
}

frappe.views.Workspace.prototype.make_page = function(page) {
    page = 'Home'
    $(this.wrapper).find('.sidebar-toggle-btn').remove()
    let workspace_html = "workspace"
    let workspace_details = {
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
    }

    if (frappe.boot.user && frappe.boot.user.user_type == "Employee Self Service" ){
        workspace_html = "self_service"
    }
    workspace_details = {...workspace_details, ...(frappe.boot.home_details || {})} 
    let $temp = frappe.render_template(workspace_html, workspace_details);
    $(this.body).html('')
    $($temp).appendTo(this.body);
    $('#new-tech-support').click(ev => { frappe.new_doc('Technical Support') })


    if (!jQuery.isEmptyObject(frappe.boot.home_details.leave_details.leave_allocation)){
        let taken = [];
        let rem = [];
        let pend = [];
        let total = [];

        let labels = []

        for(const [key, value] of Object.entries(frappe.boot.home_details.leave_details.leave_allocation || {})) {
            labels.push(key)
            taken.push(value['leaves_taken'] || "")
            rem.push(value['remaining_leaves'] || "")
            pend.push(value['leaves_pending_approval'] || "")
            total.push(value['total_leaves'] || "")
        }
        
        const data = {
            labels: labels,
            datasets: [
            {
                name: "Taken",
                values: taken,
                chartType: 'bar'
            },
            {
                name: "Remaining",
                values: rem,
                chartType: 'bar'
            },
            {
                name: "Pending",
                values:pend,
                chartType: 'bar'
            },
            {
                name: "Total",
                values: total,
                chartType: 'bar'
            }
            ]
        }
        
        const chart = new frappe.Chart("#leaves-chart-container", { 
            title: "Leave Statistics",
            data: data,
            type: 'axis-mixed', // or 'bar', 'line', 'scatter', 'pie', 'percentage'
            height: 250,
            colors: ['#71dd37', '#03c3ec' ,'#ffab00', '#743ee2']
        })
    }
    let attendance =  $('.attendance')
    attendance.click(function(e){
        let status = e.target.getAttribute('data-val')
        if(status == 'Present' && frappe.boot.home_details.attendance_employee_present.attendance_employee_present.length > 0){
                let attendance_list = frappe.boot.home_details.attendance_employee_present.attendance_employee_present;
                let attendanceHTML = "<div>"
                    + "<table style='width: 100%'>"
                    + "<tr>"
                    + "<th>Employee</th>"
                    + "</tr>";
                attendance_list.forEach(element => {
                    attendanceHTML += "<tr>"
                        + "<td> " + element.employee_name + " </td>"
                        + "</tr>";
                });
                attendanceHTML += "</table></div>";
                var d = new frappe.ui.Dialog({
                    title: "Employees " +  status,
                    fields: [
                        { 'fieldname': "attendance_table", 'fieldtype': "HTML" }
                    ]
                });
                d.fields_dict.attendance_table.$wrapper.html(attendanceHTML);
        }
        else if(status == 'Work From Home' && frappe.boot.home_details.attendance_employee_work_home.attendance_employee_work_home.length > 0){
                let attendance_list = frappe.boot.home_details.attendance_employee_work_home.attendance_employee_work_home;
                let attendanceHTML = "<div>"
                    + "<table style='width: 100%'>"
                    + "<tr>"
                    + "<th>Employee</th>"
                    + "</tr>";
                attendance_list.forEach(element => {
                    attendanceHTML += "<tr>"
                        + "<td> " + element.employee_name + " </td>"
                        + "</tr>";
                });
                attendanceHTML += "</table></div>";
                var d = new frappe.ui.Dialog({
                    title: "Employees " +  status,
                    fields: [
                        { 'fieldname': "attendance_table", 'fieldtype': "HTML" }
                    ]
                });
                d.fields_dict.attendance_table.$wrapper.html(attendanceHTML);
        }
        else if(status == 'Half Day' && frappe.boot.home_details.attendance_employee_half_day.attendance_employee_half_day.length > 0){
                let attendance_list = frappe.boot.home_details.attendance_employee_half_day.attendance_employee_half_day;
                let attendanceHTML = "<div>"
                    + "<table style='width: 100%'>"
                    + "<tr>"
                    + "<th>Employee</th>"
                    + "</tr>";
                attendance_list.forEach(element => {
                    attendanceHTML += "<tr>"
                        + "<td> " + element.employee_name + " </td>"
                        + "</tr>";
                });
                attendanceHTML += "</table></div>";
                var d = new frappe.ui.Dialog({
                    title: "Employees " +  status,
                    fields: [
                        { 'fieldname': "attendance_table", 'fieldtype': "HTML" }
                    ]
                });
                d.fields_dict.attendance_table.$wrapper.html(attendanceHTML);
            
        }
        else if(status == 'Late Entry' && frappe.boot.home_details.attendance_employee_late_entry.attendance_employee_late_entry.length > 0){
                let attendance_list = frappe.boot.home_details.attendance_employee_late_entry.attendance_employee_late_entry;
                let attendanceHTML = "<div>"
                    + "<table style='width: 100%'>"
                    + "<tr>"
                    + "<th>Employee</th>"
                    + "</tr>";
                attendance_list.forEach(element => {
                    attendanceHTML += "<tr>"
                        + "<td> " + element.employee_name + " </td>"
                        + "</tr>";
                });
                attendanceHTML += "</table></div>";
                var d = new frappe.ui.Dialog({
                    title: "Employees " +  status,
                    fields: [
                        { 'fieldname': "attendance_table", 'fieldtype': "HTML" }
                    ]
                });
                d.fields_dict.attendance_table.$wrapper.html(attendanceHTML);
        }
        else if(status == 'Exit Early' && frappe.boot.home_details.attendance_employee_early_exit.attendance_employee_early_exit.length > 0){
                let attendance_list = frappe.boot.home_details.attendance_employee_early_exit.attendance_employee_early_exit;
                let attendanceHTML = "<div>"
                    + "<table style='width: 100%'>"
                    + "<tr>"
                    + "<th>Employee</th>"
                    + "</tr>";
                attendance_list.forEach(element => {
                    attendanceHTML += "<tr>"
                        + "<td> " + element.employee_name + " </td>"
                        + "</tr>";
                });
                attendanceHTML += "</table></div>";
                var d = new frappe.ui.Dialog({
                    title: "Employees " +  status,
                    fields: [
                        { 'fieldname': "attendance_table", 'fieldtype': "HTML" }
                    ]
                });
                d.fields_dict.attendance_table.$wrapper.html(attendanceHTML);
        }
        else if(status == 'Absent' && frappe.boot.home_details.attendance_employee_absent.attendance_employee_absent.length > 0){
                let attendance_list = frappe.boot.home_details.attendance_employee_absent.attendance_employee_absent;
                let attendanceHTML = "<div>"
                    + "<table style='width: 100%'>"
                    + "<tr>"
                    + "<th>Employee</th>"
                    + "</tr>";
                attendance_list.forEach(element => {
                    attendanceHTML += "<tr>"
                        + "<td> " + element.employee_name + " </td>"
                        + "</tr>";
                });
                attendanceHTML += "</table></div>";
                var d = new frappe.ui.Dialog({
                    title: "Employees " +  status,
                    fields: [
                        { 'fieldname': "attendance_table", 'fieldtype': "HTML" }
                    ]
                });
                d.fields_dict.attendance_table.$wrapper.html(attendanceHTML);
        }
        else if(status == 'On Leave'  && frappe.boot.home_details.attendance_employee_on_leave.attendance_employee_on_leave.length > 0){
                let attendance_list = frappe.boot.home_details.attendance_employee_on_leave.attendance_employee_on_leave;
                let attendanceHTML = "<div>"
                    + "<table style='width: 100%'>"
                    + "<tr>"
                    + "<th>Employee</th>"
                    + "</tr>";
                attendance_list.forEach(element => {
                    attendanceHTML += "<tr>"
                        + "<td> " + element.employee_name + " </td>"
                        + "</tr>";
                });
                attendanceHTML += "</table></div>";
                var d = new frappe.ui.Dialog({
                    title: "Employees " +  status,
                    fields: [
                        { 'fieldname': "attendance_table", 'fieldtype': "HTML" }
                    ]
                });
                d.fields_dict.attendance_table.$wrapper.html(attendanceHTML);
        }
        else {
            let attendanceHTML = `
                                <div class="col-md-12 col-lg-12 order-1 mb-4">
                                    <div class="card">
                                        <div class="card-body" style="position: relative;">
                                            <div class="d-flex align-items-start justify-content-center"
                                            style="width: 100%;
                                            position: absolute;
                                            left: 50%;
                                            top: 50%;
                                            transform: translate(-50%, -50%);">
                                                <span class="text-center">No Employee ${e.target.innerHTML} today</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            `
            
            var d = new frappe.ui.Dialog({
                title: "Attendande Details",
                fields: [
                    { 'fieldname': "attendance_table", 'fieldtype': "HTML" }
                ]
            });    
            d.fields_dict.attendance_table.$wrapper.html(attendanceHTML);
        }
        d.show();
    });

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
