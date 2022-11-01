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
        let status = e.target.innerHTML
        let early_exit = 0
        let late_entry = 0
        if (e.target.innerHTML == 'Late Entry'){
            status = 'Present',
            late_entry = 1
        }
        if (e.target.innerHTML == 'Exit Early'){
            status = 'Present',
            early_exit = 1
        }
        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                'doctype': "Attendance",
                'filters': { 'attendance_date': frappe.datetime.get_today(),'status' : status ,'late_entry':late_entry,'early_exit':early_exit},
                'fields': [
                    'name',
                    'employee_name',
                ]
            },
            callback: function (r) {
                if (!r.exc) {
                    let attendance_list = r.message;
                    let attendanceHTML = "<div>"
                        + "<table style='width: 100%'>"
                        + "<tr>"
                        + "<th>Attendance</th>"
                        + "<th>Employee</th>"
                        + "</tr>";
                    attendance_list.forEach(element => {
                        attendanceHTML += "<tr>"
                            + "<td><a href='app/attendance/" + element.name  +"'>" + element.name + "</a>  </td>"
                            + "<td> " + element.employee_name + " </td>"
                            + "</tr>";
                    });
                    attendanceHTML += "</table></div>";
                    var d = new frappe.ui.Dialog({
                        title: "Attendande Details",
                        fields: [
                            { 'fieldname': "attendance_table", 'fieldtype': "HTML" }
                        ]
                    });
        
                    d.fields_dict.attendance_table.$wrapper.html(attendanceHTML);
                    d.show();
                }
            }
        });
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
