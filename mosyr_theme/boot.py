
import subprocess
import frappe
from erpnext.hr.doctype.leave_application.leave_application import get_leave_details
from frappe.utils import flt ,cint
import datetime
from datetime import datetime
from datetime import datetime, timedelta

def boot_session(bootinfo):
    bootinfo.language = frappe.local.lang
    bootinfo.sidebar_items = get_sidebar_items()
    bootinfo.desk_settings = get_desk_settings()
    bootinfo.home_details = get_home_details()


def get_sidebar_items():
    system_controller = frappe.get_single('System Controller')
    labels = []
    for row in system_controller.sidebar_labels:
        labels.append({'label': row.label, 'name': row.label,
                      'icon': row.icon, 'child_items': []})

    for label in labels:
        for row in system_controller.sidebar_item:
            route = ''
            has_permission = False
            if row.type == 'Report':
                route = 'query-report/' + row.doc_name
            elif row.type == 'DocType':
                has_permission = frappe.has_permission(
                    doctype=row.doc_name, user=frappe.session.user)
                route = '-'.join(row.doc_name.lower().split(' '))

            if label.get('label') == row.parent_name:
                user_type = frappe.get_doc("User" , frappe.session.user).user_type
                if user_type in ['System User' , 'Website User' , 'SaaS Manager']:
                    label.get('child_items').append({
                                'name': row.doc_name, 'label': row.label,
                                'has_permission': has_permission, 'icon': row.icon, 'route': route
                            })
                else:
                    user_doctypes=frappe.get_doc("User Type" , user_type).user_doctypes
                    for doctype in user_doctypes:
                        if doctype.document_type == row.doc_name:
                            label.get('child_items').append({
                                'name': row.doc_name, 'label': row.label,
                                'has_permission': has_permission, 'icon': row.icon, 'route': route
                            })
    final_labels = []
    for l in labels:
        if l.get("child_items"):
            final_labels.append(l)
    return final_labels


def get_desk_settings():
    role_list = frappe.get_all(
        "Role", fields=["*"], filters=dict(name=["in", frappe.get_roles()]))
    desk_settings = {}

    from frappe.core.doctype.role.role import desk_properties

    for role in role_list:
        for key in desk_properties:
            desk_settings[key] = desk_settings.get(key) or role.get(key)
    show_sidebar = frappe.db.get_single_value(
        'System Controller', 'show_sidebar') or 0
    if show_sidebar == 1:
        desk_settings['list_sidebar'] = 1
        desk_settings['form_sidebar'] = 1
    return desk_settings


def get_home_details():
    d = datetime.now()
    date = d.date()
    home_details = {}
    current_user = frappe.get_doc("User", frappe.session.user)
    salary_details = 0
    loans = "nothing to show"
    leave_details = {}
    active_employee = ""
    employee = ""
    leave_encashment = []
    paid_salaries = []
    total_leave_all_employees = {}
    # self services module
    work_experience = []
    dependants_details = []
    passport_detail = []
    health_insurance = []
    contact_details = []
    emergency_contact = []
    educational_qualification = []
    personal_details = []
    employee_id = []
    lateness_permission = []
    timesheet_list = []
    saas_config = {}
    current_employee = get_employee_by_user_id(frappe.session.user)
    user_type = current_user.user_type
    if user_type == 'Employee Self Service':
        if current_employee:
            current_employee = {
                'emp_name': current_employee.employee_name,
                'emp_route': "/app/employee/"+current_employee.name
            }
            emp = get_employee_by_user_id(
                frappe.session.user).get("name", False)
            if emp:
                leave_details = get_leave_details(emp, frappe.utils.nowdate())
                paid_salaries = frappe.db.sql(
                    """SELECT SUM(base_gross_pay) as base_gross_pay, SUM(base_total_deduction) base_total_deduction FROM `tabSalary Slip` WHERE employee='{}' and docstatus=1 """.format(emp), as_dict=True)
                loans = frappe.db.sql(
                    """SELECT SUM(loan_amount) as total_loans FROM `tabLoan` WHERE applicant_type='Employee' and applicant='{}' and docstatus=1 """.format(emp), as_dict=True)
                leave_encashment = frappe.db.sql(
                    """SELECT SUM(encashable_days) as encashable_days,SUM(encashment_amount) as encashment_amount, currency FROM `tabLeave Encashment` WHERE employee ='{}' """.format(emp), as_dict=True)
                # Self Services Doctypes
                salary_details = frappe.db.sql(
                    """SELECT name,workflow_state FROM `tabSalary Details` WHERE employee ='{}' limit 4""".format(emp), as_dict=True)
                work_experience = frappe.db.sql(
                    """SELECT name,workflow_state FROM `tabWork Experience` WHERE employee ='{}' limit 4""".format(emp), as_dict=True)
                dependants_details = frappe.db.sql(
                    """SELECT name,workflow_state FROM `tabDependants Details` WHERE employee ='{}' limit 4""".format(emp), as_dict=True)
                passport_detail = frappe.db.sql(
                    """SELECT name,workflow_state FROM `tabPassport Details` WHERE employee ='{}' limit 4""".format(emp), as_dict=True)
                health_insurance = frappe.db.sql(
                    """SELECT name,workflow_state FROM `tabHealth Insurance` WHERE employee ='{}' limit 4""".format(emp), as_dict=True)
                contact_details = frappe.db.sql(
                    """SELECT name,workflow_state FROM `tabContact Details` WHERE employee ='{}' limit 4""".format(emp), as_dict=True)
                emergency_contact = frappe.db.sql(
                    """SELECT name,workflow_state FROM `tabEmergency Contact` WHERE employee ='{}' limit 4""".format(emp), as_dict=True)
                educational_qualification = frappe.db.sql(
                    """SELECT name,workflow_state FROM `tabEducational Qualification` WHERE employee ='{}' limit 4""".format(emp), as_dict=True)
                personal_details = frappe.db.sql(
                    """SELECT name,workflow_state FROM `tabPersonal Details` WHERE employee ='{}' limit 4""".format(emp), as_dict=True)
                employee_id = frappe.db.sql(
                    """SELECT name,workflow_state FROM `tabEmployee ID` WHERE employee ='{}' limit 4""".format(emp), as_dict=True)
                lateness_permission = frappe.db.sql(
                    """SELECT name,workflow_state FROM `tabLateness Permission` WHERE employee ='{}' limit 4""".format(emp), as_dict=True)
        else:
            current_employee = {
                'emp_name': current_user.full_name,
                'emp_route': "/app/user/"+current_user.name
            }

        if len(loans) > 0:
            loans = loans[0].get("total_loans", 0)
        else:
            loans = 0

    else:
        if current_employee:
            current_employee = {
                'emp_name': current_employee.employee_name,
                'emp_route': "/app/employee/"+current_employee.name
            }
            emp = get_employee_by_user_id(
                frappe.session.user).get("name", False)
            if emp:
                leave_details = get_leave_details(emp, frappe.utils.nowdate())

        else:
            current_employee = {
                'emp_name': current_user.full_name,
                'emp_route': "/app/user/"+current_user.name
            }

        timediff = 0
        if frappe.conf.get("subscription_end_date" or "") :
            today = datetime.now()
            d1 = today
            d2 = frappe.conf.get("subscription_end_date" or "")
            d2 = datetime.strptime(d2, '%Y-%m-%d')
            timediff = abs(d2-d1).days
        active_users = frappe.db.count('User', {'name' :[ 'not in', ['Administrator','Guest']]})
        saas_config = {
            "enable_saas":frappe.conf.get("enable_saas"  or ""),
            "storage_space":frappe.conf.get("storage_space"  or ""),
            "used_space" :get_site_size(),
            "available_users":frappe.conf.get("available_users"  or ""),
            "active_users" :active_users,
            "remaining_days" : timediff ,
            "subscription_end_date":frappe.conf.get("subscription_end_date" or ""),
        }

        if frappe.session.user in ['Administrator', 'support@mosyr.io']:
            employees = frappe.get_list("Employee",pluck='name')
            for emp in employees:
                for k,v in get_leave_details(emp,frappe.utils.nowdate()).get('leave_allocation' or {}).items():
                    total_leave_all_employees.update({
                        k: {
                            "total_leaves": v.get("total_leaves", 0)+total_leave_all_employees.get(k, {}).get("total_leaves", 0),
                            "expired_leaves": v.get("expired_leaves", 0)+total_leave_all_employees.get(k, {}).get("expired_leaves", 0),
                            "leaves_taken":v.get("leaves_taken", 0)+total_leave_all_employees.get(k, {}).get("leaves_taken", 0),
                            "leaves_pending_approval":v.get("leaves_pending_approval", 0)+total_leave_all_employees.get(k, {}).get("leaves_pending_approval", 0),
                            "remaining_leaves":v.get("remaining_leaves", 0)+total_leave_all_employees.get(k, {}).get("remaining_leaves", 0),
                        }
                    })
            leave_details = {"leave_allocation":total_leave_all_employees}
        paid_salaries = frappe.db.sql(
            """SELECT SUM(base_gross_pay) as base, SUM(base_total_deduction) deduction FROM `tabSalary Slip` """, as_dict=True)
        loans = frappe.db.sql(
            """SELECT SUM(loan_amount) as total_loans FROM `tabLoan` """, as_dict=True)
        employee = frappe.db.sql(
            """SELECT count(Employee) as employee FROM `tabEmployee` """, as_dict=True)
        active_employee = frappe.db.sql(
            """SELECT count(Employee) as employee FROM `tabEmployee` where status='active' """, as_dict=True)
        leave_encashment = frappe.db.sql(
            """SELECT SUM(encashable_days) as encashable_days,SUM(encashment_amount) as encashment_amount, currency FROM `tabLeave Encashment` """, as_dict=True)
        timesheet_list = frappe.db.sql(
            """SELECT employee_name ,customer,parent_project,total_hours FROM `tabTimesheet` where docstatus=1  ORDER BY -creation limit 3""", as_dict=True)
        salary_details = frappe.db.sql(
            """SELECT name,workflow_state FROM `tabSalary Details`  limit 4""", as_dict=True)
        work_experience = frappe.db.sql(
            """SELECT name,workflow_state FROM `tabWork Experience`  limit 4""", as_dict=True)
        dependants_details = frappe.db.sql(
            """SELECT name,workflow_state FROM `tabDependants Details`  limit 4""", as_dict=True)
        passport_detail = frappe.db.sql(
            """SELECT name,workflow_state FROM `tabPassport Details`  limit 4""", as_dict=True)
        health_insurance = frappe.db.sql(
            """SELECT name,workflow_state FROM `tabHealth Insurance`  limit 4""", as_dict=True)
        contact_details = frappe.db.sql(
            """SELECT name,workflow_state FROM `tabContact Details`  limit 4""", as_dict=True)
        emergency_contact = frappe.db.sql(
            """SELECT name,workflow_state FROM `tabEmergency Contact`  limit 4""", as_dict=True)
        educational_qualification = frappe.db.sql(
            """SELECT name,workflow_state FROM `tabEducational Qualification`  limit 4""", as_dict=True)
        personal_details = frappe.db.sql(
            """SELECT name,workflow_state FROM `tabPersonal Details`  limit 4""", as_dict=True)
        employee_id = frappe.db.sql(
            """SELECT name,workflow_state FROM `tabEmployee ID`  limit 4""", as_dict=True)
        lateness_permission = frappe.db.sql(
            """SELECT name,workflow_state FROM `tabLateness Permission`  limit 4""", as_dict=True)
        
        if len(loans) > 0:
            loans = loans[0].get("total_loans", 0)
        else:
            loans = 0

        if len(employee) > 0:
            employee = employee[0].get("employee", 0)
        else:
            employee = 0

        if len(active_employee) > 0:
            active_employee = active_employee[0].get("employee", 0)
        else:
            active_employee = 0
        
        shifts_details = frappe.db.sql("""
            SELECT st.name as shift, IFNULL(presents.total, 0) AS presents, IFNULL(absents.total, 0) AS absents, IFNULL(on_leaves.total, 0) AS on_leaves,
                IFNULL(half_days.total, 0) AS half_days, IFNULL(from_homes.total, 0) AS from_homes, IFNULL(lates.total, 0) AS lates, IFNULL(earlies.total, 0) AS earlies
            FROM `tabShift Type` st
            LEFT JOIN (SELECT shift, COUNT(name) AS total FROM `tabAttendance` WHERE status='Present' AND docstatus=1 AND IFNULL(shift, '') <> '' AND attendance_date=curdate() GROUP BY shift) presents ON presents.shift=st.name
            LEFT JOIN (SELECT shift, COUNT(name) AS total FROM `tabAttendance` WHERE status='Absent' AND docstatus=1 AND IFNULL(shift, '') <> '' AND attendance_date=curdate() GROUP BY shift) absents ON absents.shift=st.name
            LEFT JOIN (SELECT shift, COUNT(name) AS total FROM `tabAttendance` WHERE status='On Leave' AND docstatus=1 AND IFNULL(shift, '') <> '' AND attendance_date=curdate() GROUP BY shift) on_leaves ON on_leaves.shift=st.name
            LEFT JOIN (SELECT shift, COUNT(name) AS total FROM `tabAttendance` WHERE status='Half Day' AND docstatus=1 AND IFNULL(shift, '') <> '' AND attendance_date=curdate() GROUP BY shift) half_days ON half_days.shift=st.name
            LEFT JOIN (SELECT shift, COUNT(name) AS total FROM `tabAttendance` WHERE status='Work From Home' AND docstatus=1 AND IFNULL(shift, '') <> '' AND attendance_date=curdate() GROUP BY shift) from_homes ON from_homes.shift=st.name
            LEFT JOIN (SELECT shift, COUNT(name) AS total FROM `tabAttendance` WHERE late_entry=1 AND docstatus=1 AND IFNULL(shift, '') <> '' AND attendance_date=curdate() GROUP BY shift) lates ON lates.shift=st.name
            LEFT JOIN (SELECT shift, COUNT(name) AS total FROM `tabAttendance` WHERE early_exit=1 AND docstatus=1 AND IFNULL(shift, '') <> '' AND attendance_date=curdate() GROUP BY shift) earlies ON earlies.shift=st.name
            WHERE st.name IN (SELECT shift FROM `tabAttendance` WHERE docstatus=1 AND IFNULL(shift, '') <> '' AND attendance_date=curdate() group by shift)
        """, as_dict=True)
        for sd in shifts_details:
            pass

        home_details.update({
            "saas_config" :saas_config,
            "shifts_details": shifts_details
        })
    home_details.update({
        "date":date,
        "current_user": current_user,
        "current_employee": current_employee,
        "leave_details": leave_details,
        "len_leave_details" : len(leave_details),
        "len_leave_allocation":len(leave_details.get('leave_allocation', [])),
        "loans": loans,
        "employee": employee,
        "active_employee": active_employee,
        "paid_salaries": paid_salaries,
        "leave_encashment": leave_encashment,
        "timesheet_list": timesheet_list,
        "total_leave_all_employees":total_leave_all_employees,
        # Self Services
        "salary_details": {"salary_details": salary_details[:3], "len": len(salary_details)},
        "work_experience": {"work_experience": work_experience[:3], "len": len(work_experience)},
        "dependants_details": {"dependants_details": dependants_details[:3], "len": len(dependants_details)},
        "passport_detail": {"passport_detail": passport_detail[:3], "len": len(passport_detail)},
        "health_insurance": {"health_insurance": health_insurance[:3], "len": len(health_insurance)},
        "contact_details": {"contact_details": contact_details[:3], "len": len(contact_details)},
        "emergency_contact": {"emergency_contact": emergency_contact[:3], "len": len(emergency_contact)},
        "educational_qualification": {"educational_qualification": educational_qualification[:3], "len": len(educational_qualification)},
        "personal_details": {"personal_details": personal_details[:3], "len": len(personal_details)},
        "employee_id": {"employee_id": employee_id[:3], "len": len(employee_id)},
        "lateness_permission": {"lateness_permission": lateness_permission[:3], "len": len(lateness_permission),
        },

    })
    return home_details


def get_employee_by_user_id(user_id):
    emp_id = frappe.db.exists("Employee", {"user_id": user_id})
    if emp_id:
        return frappe.get_doc("Employee", emp_id)
    return None

def get_site_size():
    # all possible file locations
    from frappe.utils import flt
    site_path = frappe.get_site_path()
    private_files_path = site_path + '/private/files'
    public_files_path  = site_path + '/public/files'
    backup_files_path = site_path + '/private/backups'

    # Calculating Sizes
    private_files_size = get_directory_size(private_files_path)
    backup_files_size = get_directory_size(backup_files_path)
    public_files_size = get_directory_size(public_files_path)
    total_size = private_files_size + backup_files_size + public_files_size
    return flt(total_size,2)

def get_directory_size(path):
    """
    returns total size of directory in MBs
    """
    import os
 
    # assign size
    size = 0
    
    # get size
    for path, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(path, f)
            size += os.path.getsize(fp)
    
    # display size
    return  int(str(size))/1000000.0