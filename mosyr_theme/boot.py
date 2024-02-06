
import subprocess
import frappe
from erpnext.hr.doctype.leave_application.leave_application import get_leave_details
from frappe.utils import flt ,cint, today
import datetime
from datetime import datetime
from datetime import datetime, timedelta
from frappe.permissions import get_valid_perms

def boot_session(bootinfo):
    bootinfo.language = frappe.local.lang
    bootinfo.role_profile = frappe.db.get_value("User", frappe.session.user, "role_profile_name")
    bootinfo.sidebar_items = get_sidebar_items()
    bootinfo.desk_settings = get_desk_settings()
    bootinfo.home_details = get_home_details()


def get_sidebar_items():    
    system_controller = frappe.get_single('System Controller')
    labels = []
    for row in system_controller.sidebar_labels:
        labels.append({'label': row.label, 'name': row.label,
                        'icon': row.icon, 'child_items': []})
    result = get_valid_perms(user=frappe.session.user)
    user_doctypes = [d.parent for d in result]
    for label in labels:
        sidebar_items_list = frappe.get_list("SideBar Item Table", fields=["doc_name", "type", "parent_name", "label", "icon"], filters={"parent_name": label.get('label')}, order_by="idx")
        for row in sidebar_items_list:
            role_profile_name = frappe.get_doc("User" , frappe.session.user).role_profile_name
            if frappe.session.user not in ["Administrator", "support@mosr.io"]:
                if row.doc_name in ["Translation", "System Controller"]:
                    continue
            route = ''
            has_permission = False

            if row.type == 'Report':
                route = 'query-report/' + row.doc_name
                report_name = row.doc_name
                user_name = frappe.session.user
                doc = frappe.get_doc("Report", report_name)

                # Check if the user has report permission on the report
                has_report_permission = frappe.has_permission(doc.ref_doctype, user=user_name, ptype='report')
                has_permission  =  has_report_permission


            elif row.type == 'DocType':
                has_permission = frappe.has_permission(
                    doctype=row.doc_name, user=frappe.session.user)
                route = '-'.join(row.doc_name.lower().split(' '))
                
            
            user_type = frappe.get_doc("User" , frappe.session.user).user_type
            if role_profile_name in ['SaaS Manager', 'Self Service', 'SaaS User']:

                if has_permission:
                    label.get('child_items').append({
                                'name': row.doc_name, 'label': row.label,
                                'has_permission': has_permission, 'icon': row.icon, 'route': route
                            })
            else:
                if row.doc_name in user_doctypes:
                    label.get('child_items').append({
                        'name': row.doc_name, 'label': row.label,
                        'has_permission': has_permission, 'icon': row.icon, 'route': route
                    })

    reports = frappe.db.sql(f""" SELECT DISTINCT(cr.report), sit.parent_name
                            FROM `tabCustom Role` cr
                            LEFT JOIN `tabHas Role` hr ON hr.parent=cr.name
                            LEFT JOIN `tabSideBar Item Table` sit ON sit.doc_name = cr.report
                            WHERE hr.role='{user_type}'
                            """,as_dict=1)
    final_labels = []
    for l in labels:
        if l.get("child_items"):
            final_labels.append(l)
    for items in final_labels:
        # for r in reports:
        if items.get("name") in reports:
            items.get("child_items").append({
            'label': items.get("name"),
            'name': items.get("name"),
            'has_permission': 1,
            'icon': '',
            'route': f'query-report/{items.get("name")}'
            })


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
    role_profile_name = current_user.role_profile_name
    if role_profile_name == 'Self Service':
        if current_employee:
            current_employee = {
                'emp_name': current_employee.employee_name,
                'emp_route': "/app/employee/"+current_employee.name
            }
            emp = get_employee_by_user_id(
                frappe.session.user).get("name", False)
            if emp:
                try:
                    leave_details = get_leave_details(emp, frappe.utils.nowdate())
                except Exception as e:
                    frappe.log_error(
                        title= ("Error While boot"),
                        message=e
                    )
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
                try:
                    leave_details = get_leave_details(emp, frappe.utils.nowdate())
                except Exception as e:
                    frappe.log_error(
                        title= ("Error While boot"),
                        message=e
                    )
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
        shifts_details = {}
        attendance_employee_list = []
        toda_is = frappe.utils.nowdate()
        today_attendance = frappe.db.sql("""
            SELECT status, late_entry, early_exit, shift, employee
            FROM `tabAttendance`
            WHERE docstatus=1 AND IFNULL(shift, '') <> '' AND attendance_date='{}'
            ORDER BY employee
        """.format(toda_is), as_dict=True)
        for ta in today_attendance:
            attendance_employee_list.append(ta.employee)
            presents = 1 if  ta.get("status") == "Present" else 0
            absents = 1 if  ta.get("status") == "Absent" else 0
            on_leaves = 1 if  ta.get("status") == "On Leave" else 0
            half_days = 1 if  ta.get("status") == "Half Day" else 0
            from_homes = 1 if  ta.get("status") == "Work From Home" else 0
            if shifts_details.get(ta.shift):
                old_shift_data = shifts_details.get(ta.shift, {})
                shift_data = {
                    "shift": ta.shift,
                    "presents": cint(old_shift_data.get("presents")) + presents,
                    "absents": cint(old_shift_data.get("absents")) + absents,
                    "on_leaves": cint(old_shift_data.get("on_leaves")) + on_leaves,
                    "half_days": cint(old_shift_data.get("half_days")) + half_days,
                    "from_homes": cint(old_shift_data.get("from_homes")) + from_homes,
                    "lates": cint(old_shift_data.get("lates")) + cint(ta.get("late_entry")),
                    "earlies": cint(old_shift_data.get("earlies")) + cint(ta.get("early_exit")),
                }
                shifts_details.update({
                    f"{ta.shift}": shift_data
                })
            else:
                shifts_details.update({
                    f"{ta.shift}":{
                        "shift": ta.shift,
                        "presents": presents,
                        "absents": absents,
                        "on_leaves": on_leaves,
                        "half_days": half_days,
                        "from_homes": from_homes,
                        "lates": cint(ta.get("late_entry")),
                        "earlies": cint(ta.get("early_exit"))
                    }
                })
        
        attendance_employee_list_str = [f"'{emp}'"for emp in attendance_employee_list]
        attendance_employee_list_str.append("''")
        attendance_employee_list_str = ", ".join(attendance_employee_list_str)
        logs = frappe.db.sql(f"""
            SELECT *
            FROM `tabEmployee Checkin`
            WHERE CAST(time AS DATE)='{toda_is}' AND IFNULL(shift, '') <> '' 
                  AND employee NOT IN ({attendance_employee_list_str})
        """, as_dict=True)
        log_per_employee = {}
        for log in logs:
            if log_per_employee.get(log.employee):
                emp_logs = log_per_employee.get(log.employee, {})
                if emp_logs.get(log.shift):
                    elis = emp_logs.get(log.shift, [])
                    elis.append(log)
                    emp_logs.update({
                        f"{log.shift}": elis
                    })
                else:
                    emp_logs.update({
                        f"{log.shift}": [log]
                    })
            else:
                log_per_employee.update({
                    f"{log.employee}": {
                        f"{log.shift}": [log]
                    }
                })
        for emp, sd in log_per_employee.items():
            for s, logs_in_shift in sd.items():
                status, total_working_hours, late_entry, early_exit, in_time, out_time = get_attendance(s, logs_in_shift)
                presents = 1 if  status == "Present" else 0
                absents = 1 if  status == "Absent" else 0
                on_leaves = 1 if  status == "On Leave" else 0
                half_days = 1 if  status == "Half Day" else 0
                from_homes = 1 if  status == "Work From Home" else 0
                if shifts_details.get(s):
                    old_shift_data = shifts_details.get(s, {})
                    shift_data = {
                        "shift": s,
                        "presents": cint(old_shift_data.get("presents")) + presents,
                        "absents": cint(old_shift_data.get("absents")) + absents,
                        "on_leaves": cint(old_shift_data.get("on_leaves")) + on_leaves,
                        "half_days": cint(old_shift_data.get("half_days")) + half_days,
                        "from_homes": cint(old_shift_data.get("from_homes")) + from_homes,
                        "lates": cint(old_shift_data.get("lates")) + cint(late_entry),
                        "earlies": cint(old_shift_data.get("earlies")) + cint(early_exit),
                    }
                    shifts_details.update({
                        f"{s}": shift_data
                    })
                else:
                    shifts_details.update({
                        f"{s}":{
                            "shift": s,
                            "presents": presents,
                            "absents": absents,
                            "on_leaves": on_leaves,
                            "half_days": half_days,
                            "from_homes": from_homes,
                            "lates": cint(late_entry),
                            "earlies": cint(early_exit)
                        }
                    })
        shifts_details = [v for k, v in shifts_details.items()]
        home_details.update({
            "saas_config" :saas_config,
            "shifts_details": shifts_details,
            "attendance_report_date": toda_is
        })
    attendence_details = get_employee_attendence_details()
    
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
        "attendence_details": attendence_details,
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

def get_attendance(shift, logs):
    from mosyr.overrides import calculate_working_hours

    shift = frappe.get_doc("Shift Type", shift)
    late_entry = early_exit = False
    total_working_hours, in_time, out_time = calculate_working_hours(
        logs,
        shift.determine_check_in_and_check_out,
        shift.working_hours_calculation_based_on,
    )
    if (
        cint(shift.enable_entry_grace_period)
        and in_time
        and in_time
        > logs[0].shift_start
        + timedelta(minutes=cint(shift.late_entry_grace_period))
    ):
        late_entry = True

    if (
        cint(shift.enable_exit_grace_period)
        and out_time
        and out_time
        < logs[0].shift_end - timedelta(minutes=cint(shift.early_exit_grace_period))
    ):
        early_exit = True

    if (
        shift.working_hours_threshold_for_half_day
        and total_working_hours < shift.working_hours_threshold_for_half_day
    ):
        return (
            "Half Day",
            total_working_hours,
            late_entry,
            early_exit,
            in_time,
            out_time,
        )
    if (
        shift.working_hours_threshold_for_absent
        and total_working_hours < shift.working_hours_threshold_for_absent
    ):
        return (
            "Absent",
            total_working_hours,
            late_entry,
            early_exit,
            in_time,
            out_time,
        )
    return "Present", total_working_hours, late_entry, early_exit, in_time, out_time


def get_employee_attendence_details():
    date = '2023-08-16'
    result = {
        "present":[],
        "late_entry":[],
        "absent":[],
        "early_exit":[],
        "overtime":[]
    }
    attendance_list = frappe.db.get_list("Attendance", fields=["name"], filters={"attendance_date":date}, ignore_permissions=True)
    for row in attendance_list:
        doc = frappe.get_doc("Attendance", row.get("name"))
        if doc.status == "Present" and not doc.late_entry and not doc.early_exit:
            result.get('present').append({
                "employee_name":doc.employee_name,
                "shift":doc.shift,
                "in_time": doc.in_time,
                "out_name":doc.out_time
            })
            
        elif doc.status == "Present" and doc.late_entry:
            result.get('late_entry').append({
                "employee_name":doc.employee_name,
                "shift":doc.shift,
                "in_time": doc.in_time,
                "out_name":doc.out_time
            })
            
        elif doc.status == "Present" and doc.early_exit:
            result.get('early_exit').append({
                "employee_name":doc.employee_name,
                "shift":doc.shift,
                "in_time": doc.in_time,
                "out_name":doc.out_time
            })
        
        elif doc.status == "Absent":
            result.get('absent').append({
                "employee_name":doc.employee_name,
                "shift":doc.shift,
                "in_time": "_",
                "out_name": "_"
            })

    return result