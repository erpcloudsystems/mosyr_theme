
import frappe
from erpnext.hr.doctype.leave_application.leave_application import get_leave_details

def boot_session(bootinfo):
    bootinfo.language = frappe.local.lang
    bootinfo.sidebar_items = get_sidebar_items()
    bootinfo.desk_settings = get_desk_settings()
    bootinfo.home_details = get_home_details()

def get_sidebar_items():
    system_controller = frappe.get_single('System Controller')
    labels = []
    for row in system_controller.sidebar_labels:
        labels.append({'label': row.label, 'name': row.label,'icon': row.icon, 'child_items':[]})

    for label in labels:
        for row in system_controller.sidebar_item:
            route = ''
            has_permission = False
            if row.type == 'Report':
                route = 'query-report/' + row.doc_name
            elif row.type == 'DocType':
                has_permission = frappe.has_permission(doctype=row.doc_name, user=frappe.session.user)
                route = '-'.join(row.doc_name.lower().split(' '))

            if label.get('label') == row.parent_name:
                label.get('child_items').append({
                    'name':row.doc_name, 'label':row.label,
                    'has_permission': has_permission, 'icon':row.icon, 'route':route
                })
    return labels


def get_desk_settings():
    role_list = frappe.get_all("Role", fields=["*"], filters=dict(name=["in", frappe.get_roles()]))
    desk_settings = {}

    from frappe.core.doctype.role.role import desk_properties

    for role in role_list:
        for key in desk_properties:
            desk_settings[key] = desk_settings.get(key) or role.get(key)
    show_sidebar = frappe.db.get_single_value('System Controller', 'show_sidebar') or 0
    if show_sidebar == 1:
        desk_settings['list_sidebar'] = 1
        desk_settings['form_sidebar'] = 1
    return desk_settings

def get_home_details():    
    home_details = {}
    current_user = frappe.get_doc("User", frappe.session.user)
    salary_details = 0
    loans = "nothing to show"
    leave_details = {}

    current_employee = get_employee_by_user_id(frappe.session.user)
    if current_employee:
        current_employee = {
            'emp_name': current_employee.employee_name,
            'emp_route': "/app/employee/"+current_employee.name
        }
        
        emp = current_employee.get("name", False)
        if emp:
            leave_details = get_leave_details(emp, frappe.utils.nowdate())
            paid_salaries = frappe.db.sql("""SELECT SUM(base_gross_pay) as base_gross_pay, SUM(base_total_deduction) base_total_deduction FROM `tabSalary Slip` WHERE employee='{}' """.format(emp), as_dict=True)
            loans = frappe.db.sql("""SELECT SUM(loan_amount) as total_loans FROM `tabLoan` WHERE applicant_type='Employee' applicant='{}' """.format(emp), as_dict=True)
    else:
        current_employee = {
            'emp_name': current_user.full_name,
            'emp_route': "/app/user/"+current_user.name
        }
        paid_salaries = frappe.db.sql("""SELECT SUM(base_gross_pay) as base_gross_pay, SUM(base_total_deduction) base_total_deduction FROM `tabSalary Slip` """, as_dict=True)
        loans = frappe.db.sql("""SELECT SUM(loan_amount) as total_loans FROM `tabLoan`""", as_dict=True)

    if len(loans) > 0:
        loans = loans[0].get("total_loans", 0)
    else:
        loans = 0
    home_details.update({
        "current_user": current_user,
        "current_employee": current_employee,
        "salary_details": salary_details,
        "leave_details": leave_details,
        "loans": loans,
    })
    print(home_details)
    return home_details

def get_employee_by_user_id(user_id):
	emp_id = frappe.db.exists("Employee", {"user_id": user_id})
	if emp_id:
		return frappe.get_doc("Employee", emp_id)
	return None