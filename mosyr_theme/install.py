from __future__ import unicode_literals
import frappe


def after_install():
    set_sidebar()
    make_settings_dropdown_clean()


def make_settings_dropdown_clean():
    for navbar_item in frappe.get_list(
        "Navbar Item", filters={"parentfield": "settings_dropdown", "is_standard": 1}
    ):
        navbar_item = frappe.get_doc("Navbar Item", navbar_item.name)
        if navbar_item.item_label in ["My Profile", "My Settings", "Logout"]:
            continue
        if navbar_item.item_type in ["Separator"]:
            continue
        navbar_item.delete()
    frappe.db.commit()


side_bar_static = {
    "enable": 1,
    "show_sidebar": 1,
    "sidebar_labels": [
        {"label": "Vehicle management", "icon": "gantt"},
        {"label": "payroll", "icon": "accounting"},
        {"label": "Employees performance", "icon": "star"},
        {"label": "Leave", "icon": "oranisation"},
        {"label": "Custody management", "icon": ""},
        {"label": "Loans", "icon": "income"},
        {"label": "Timesheet Attendees management", "icon": "milestone"},
        {"label": "System management", "icon": "setting-gear"},
        {"label": "Documents management", "icon": ""},
        {"label": "E-form", "icon": "permission"},
        {"label": "Self service", "icon": "reply-all"},
        {"label": "Employees list", "icon": "share"},
        {"label": "User management", "icon": "edit-round"},
        {"label": "HR management", "icon": "s"},
    ],
    "sidebar_item": [
        {
            "type": "Report",
            "doc_name": "Employee Attendance Sheet",
            "parent_name": "Timesheet Attendees management",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Leave Policy Assignment",
            "parent_name": "HR management",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Personal Details",
            "parent_name": "Self service",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Document Type",
            "parent_name": "Documents management",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Salary Component",
            "parent_name": "payroll",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Employment Type",
            "parent_name": "HR management",
            "icon": "milestone",
        },
        {
            "type": "DocType",
            "doc_name": "Salary Details",
            "parent_name": "Self service",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Attendance Request",
            "parent_name": "Timesheet Attendees management",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Leave Policy",
            "parent_name": "HR management",
            "icon": "list_alt",
        },
        {
            "type": "DocType",
            "doc_name": "Emergency Contact",
            "parent_name": "Self service",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Translation",
            "parent_name": "System management",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Vehicle",
            "parent_name": "Vehicle management",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Leave Block List",
            "parent_name": "HR management",
            "icon": "",
        },
        {"type": "DocType", "doc_name": "Loan", "parent_name": "Loans", "icon": ""},
        {
            "type": "Report",
            "doc_name": "Leave Balance Encashment",
            "parent_name": "Leave",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Loan Type",
            "parent_name": "Loans",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Employee",
            "parent_name": "Employees list",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Travel Request",
            "parent_name": "Leave",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Educational Qualification",
            "parent_name": "Self service",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Mosyr Form",
            "parent_name": "E-form",
            "icon": "edit",
        },
        {
            "type": "DocType",
            "doc_name": "Employee Health Insurance",
            "parent_name": "HR management",
            "icon": "healthcare",
        },
        {
            "type": "DocType",
            "doc_name": "Payroll Entry",
            "parent_name": "payroll",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Employee Grade",
            "parent_name": "HR management",
            "icon": "insert-below",
        },
        {
            "type": "Report",
            "doc_name": "Employee Leave Balance",
            "parent_name": "Leave",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "User",
            "parent_name": "User management",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Retention Bonus",
            "parent_name": "payroll",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Branch",
            "parent_name": "HR management",
            "icon": "equity",
        },
        {
            "type": "DocType",
            "doc_name": "Staffing Plan",
            "parent_name": "HR management",
            "icon": "small-message",
        },
        {
            "type": "Report",
            "doc_name": "Employee Attendance Sheet",
            "parent_name": "Timesheet Attendees management",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Cash Custody",
            "parent_name": "Custody management",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Custody",
            "parent_name": "Custody management",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Leave Type",
            "parent_name": "HR management",
            "icon": "oranisation",
        },
        {
            "type": "DocType",
            "doc_name": "Department",
            "parent_name": "HR management",
            "icon": "image-view",
        },
        {
            "type": "DocType",
            "doc_name": "Salary Slip",
            "parent_name": "payroll",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Health Insurance",
            "parent_name": "Self service",
            "icon": "",
        },
        {
            "type": "Report",
            "doc_name": "Insurances and Risk",
            "parent_name": "Employees list",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Leave Application",
            "parent_name": "Leave",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Leave Period",
            "parent_name": "HR management",
            "icon": "projects",
        },
        {
            "type": "DocType",
            "doc_name": "Leave Encashment",
            "parent_name": "HR management",
            "icon": "money-coins-1",
        },
        {
            "type": "DocType",
            "doc_name": "Payroll Settings",
            "parent_name": "payroll",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Employee Checkin",
            "parent_name": "Timesheet Attendees management",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Document Manager",
            "parent_name": "Documents management",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Employee Group",
            "parent_name": "HR management",
            "icon": "drag-1",
        },
        {
            "type": "DocType",
            "doc_name": "Designation",
            "parent_name": "HR management",
            "icon": "permission",
        },
        {
            "type": "DocType",
            "doc_name": "Salary Structure",
            "parent_name": "payroll",
            "icon": "",
        },
        {
            "type": "Report",
            "doc_name": "Biomitric Devices",
            "parent_name": "Timesheet Attendees management",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Cash Custody Expense",
            "parent_name": "Custody management",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Company Controller",
            "parent_name": "System management",
            "icon": "tool",
        },
        {
            "type": "DocType",
            "doc_name": "System Controller",
            "parent_name": "System management",
            "icon": "upload",
        },
        {
            "type": "DocType",
            "doc_name": "Shift Type",
            "parent_name": "HR management",
            "icon": "group-by",
        },
        {
            "type": "DocType",
            "doc_name": "Upload Attendance",
            "parent_name": "Timesheet Attendees management",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Vehicle Service",
            "parent_name": "Vehicle management",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Leave Encashment",
            "parent_name": "Leave",
            "icon": "",
        },
        {
            "type": "Report",
            "doc_name": "Files in Saudi banks format",
            "parent_name": "payroll",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Employee Incentive",
            "parent_name": "payroll",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "End Of Service",
            "parent_name": "Employees list",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Employee Attendance Tool",
            "parent_name": "Timesheet Attendees management",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Appraisal",
            "parent_name": "Employees performance",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Users Permission Manager",
            "parent_name": "User management",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Loan Application",
            "parent_name": "Loans",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Compensatory Leave Request",
            "parent_name": "Leave",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Employee Benefit",
            "parent_name": "payroll",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Attendance",
            "parent_name": "Timesheet Attendees management",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Leave Application",
            "parent_name": "Self service",
            "icon": "review",
        },
        {
            "type": "DocType",
            "doc_name": "Appraisal Template",
            "parent_name": "Employees performance",
            "icon": "",
        },
        {
            "type": "Report",
            "doc_name": "Employee Leave Balance Summary",
            "parent_name": "Leave",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Shift Request",
            "parent_name": "Self service",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Salary Structure Assignment",
            "parent_name": "payroll",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Leave Allocation",
            "parent_name": "HR management",
            "icon": "criticize",
        },
        {
            "type": "DocType",
            "doc_name": "Employee Deduction",
            "parent_name": "payroll",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Holiday List",
            "parent_name": "HR management",
            "icon": "assets",
        },
        {
            "type": "DocType",
            "doc_name": "Vehicle Log",
            "parent_name": "Vehicle management",
            "icon": "",
        },
        {
            "type": "DocType",
            "doc_name": "Contact Details",
            "parent_name": "Self service",
            "icon": "",
        },
    ],
    "shortcuts": [],
    "charts": [],
    "notifications": [],
}


def set_sidebar():
    if not frappe.db.exists("DocType", "System Controller"):
        return
    sc = frappe.get_doc("System Controller")
    sc.enable = 1
    sc.show_sidebar = 1

    for label in side_bar_static["sidebar_labels"]:
        sc.append("sidebar_labels", label)

    for label in side_bar_static["sidebar_item"]:
        sc.append("sidebar_item", label)
    sc.save(ignore_permissions=True)
    frappe.db.commit()
