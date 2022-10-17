from __future__ import unicode_literals
import frappe


def after_install():
    set_sidebar()

side_bar_static = {
    "enable": 1,
    "show_sidebar": 1,
    "sidebar_labels": [
      {
        "label": "اعدادات النظام",
        "icon": "setting-gear"
      },
      {
        "label": "ادارة المستخدمين",
        "icon": "edit-round"
      },
      {
        "label": "اعدادات الموارد البشرية",
        "icon": "s"
      },
      {
        "label": "قائمة الموظفين",
        "icon": "share"
      },
      {
        "label": "الخدمة الذاتية",
        "icon": "reply-all"
      },
      {
        "label": "قائمة النماذج الالكترونية",
        "icon": "permission"
      },
      {
        "label": "ادارة الحضور والانصراف",
        "icon": "milestone"
      },
      {
        "label": "الرواتب والاجور",
        "icon": "accounting"
      },
      {
        "label": "اداء الموظفين",
        "icon": "star"
      },
      {
        "label": "الاجازات",
        "icon": "oranisation"
      },
      {
        "label": "القروض",
        "icon": "income"
      },
      {
        "label": "ادارة المركبات",
        "icon": "gantt"
      },
      {
        "label": "ادارة الوثائق",
        "icon": ""
      },
      {
        "label": "العهد العينية والنقدية",
        "icon": ""
      }
    ],
    "sidebar_item": [
        {
            "type": "DocType",
            "doc_name": "System Controller",
            "parent_name": "اعدادات النظام",
            "icon": "upload"
        },
        {
            "type": "DocType",
            "doc_name": "Company Controller",
            "parent_name": "اعدادات النظام",
            "icon": "tool"
        },
        {
            "type": "DocType",
            "doc_name": "Department",
            "parent_name": "اعدادات الموارد البشرية",
            "icon": "image-view"
        },
        {
            "type": "DocType",
            "doc_name": "Branch",
            "parent_name": "اعدادات الموارد البشرية",
            "icon": "equity"
        },
        {
            "type": "DocType",
            "doc_name": "Employee Group",
            "parent_name": "اعدادات الموارد البشرية",
            "icon": "drag-1"
        },
        {
            "type": "DocType",
            "doc_name": "Designation",
            "parent_name": "اعدادات الموارد البشرية",
            "icon": "permission"
        },
        {
            "type": "DocType",
            "doc_name": "Employee Grade",
            "parent_name": "اعدادات الموارد البشرية",
            "icon": "insert-below"
        },
        {
            "type": "DocType",
            "doc_name": "Employment Type",
            "parent_name": "اعدادات الموارد البشرية",
            "icon": "milestone"
        },
        {
            "type": "DocType",
            "doc_name": "Shift Type",
            "parent_name": "اعدادات الموارد البشرية",
            "icon": "group-by"
        },
        {
            "type": "DocType",
            "doc_name": "Staffing Plan",
            "parent_name": "اعدادات الموارد البشرية",
            "icon": "small-message"
        },
        {
            "type": "DocType",
            "doc_name": "Holiday List",
            "parent_name": "اعدادات الموارد البشرية",
            "icon": "assets"
        },
        {
            "type": "DocType",
            "doc_name": "Leave Type",
            "parent_name": "اعدادات الموارد البشرية",
            "icon": "oranisation"
        },
        {
            "type": "DocType",
            "doc_name": "Leave Period",
            "parent_name": "اعدادات الموارد البشرية",
            "icon": "projects"
        },
        {
            "type": "DocType",
            "doc_name": "Leave Policy",
            "parent_name": "اعدادات الموارد البشرية",
            "icon": "list_alt"
        },
        {
            "type": "DocType",
            "doc_name": "Leave Policy Assignment",
            "parent_name": "اعدادات الموارد البشرية"
        },
        {
            "type": "DocType",
            "doc_name": "Leave Allocation",
            "parent_name": "اعدادات الموارد البشرية",
            "icon": "criticize"
        },
        {
            "type": "DocType",
            "doc_name": "Leave Encashment",
            "parent_name": "اعدادات الموارد البشرية",
            "icon": "money-coins-1"
        },
        {
            "type": "DocType",
            "doc_name": "Employee Health Insurance",
            "parent_name": "اعدادات الموارد البشرية",
            "icon": "healthcare"
        },
        {
            "type": "DocType",
            "doc_name": "Employee",
            "parent_name": "قائمة الموظفين"
        },
        {
            "type": "DocType",
            "doc_name": "Salary Structure",
            "parent_name": "قائمة الموظفين",
            "icon": "faws-person-snowmobiling"
        },
        {
            "type": "DocType",
            "doc_name": "Mosyr Form",
            "parent_name": "قائمة النماذج الالكترونية",
            "icon": "edit"
        },
        {
            "type": "DocType",
            "doc_name": "Leave Application",
            "parent_name": "الخدمة الذاتية",
            "icon": "review"
        },
        {
            "type": "DocType",
            "doc_name": "Shift Request",
            "parent_name": "الخدمة الذاتية"
        },
        {
            "type": "DocType",
            "doc_name": "Contact Details",
            "parent_name": "الخدمة الذاتية"
        },
        {
            "type": "DocType",
            "doc_name": "Educational Qualification",
            "parent_name": "الخدمة الذاتية"
        },
        {
            "type": "DocType",
            "doc_name": "Emergency Contact",
            "parent_name": "الخدمة الذاتية"
        },
        {
            "type": "DocType",
            "doc_name": "Health Insurance",
            "parent_name": "الخدمة الذاتية"
        },
        {
            "type": "DocType",
            "doc_name": "Personal Details",
            "parent_name": "الخدمة الذاتية"
        },
        {
            "type": "DocType",
            "doc_name": "Salary Details",
            "parent_name": "الخدمة الذاتية"
        },
        {
            "type": "DocType",
            "doc_name": "Attendance",
            "parent_name": "ادارة الحضور والانصراف"
        },
        {
            "type": "DocType",
            "doc_name": "Employee Attendance Tool",
            "parent_name": "ادارة الحضور والانصراف"
        },
        {
            "type": "DocType",
            "doc_name": "Attendance Request",
            "parent_name": "ادارة الحضور والانصراف"
        },
        {
            "type": "DocType",
            "doc_name": "Upload Attendance",
            "parent_name": "ادارة الحضور والانصراف"
        },
        {
            "type": "DocType",
            "doc_name": "Employee Checkin",
            "parent_name": "ادارة الحضور والانصراف"
        },
        {
            "type": "DocType",
            "doc_name": "Payroll Settings",
            "parent_name": "الرواتب والاجور"
        },
        {
            "type": "DocType",
            "doc_name": "Payroll Entry",
            "parent_name": "الرواتب والاجور"
        },
        {
            "type": "DocType",
            "doc_name": "Payroll Period",
            "parent_name": "الرواتب والاجور"
        },
        {
            "type": "DocType",
            "doc_name": "Salary Structure",
            "parent_name": "الرواتب والاجور"
        },
        {
            "type": "DocType",
            "doc_name": "Salary Structure Assignment",
            "parent_name": "الرواتب والاجور"
        },
        {
            "type": "DocType",
            "doc_name": "Salary Slip",
            "parent_name": "الرواتب والاجور"
        },
        {
            "type": "DocType",
            "doc_name": "Additional Salary",
            "parent_name": "الرواتب والاجور"
        },
        {
            "type": "DocType",
            "doc_name": "Retention Bonus",
            "parent_name": "الرواتب والاجور"
        },
        {
            "type": "DocType",
            "doc_name": "Employee Incentive",
            "parent_name": "الرواتب والاجور"
        },
        {
            "type": "DocType",
            "doc_name": "Appraisal",
            "parent_name": "اداء الموظفين"
        },
        {
            "type": "DocType",
            "doc_name": "Appraisal Template",
            "parent_name": "اداء الموظفين"
        },
        {
            "type": "DocType",
            "doc_name": "Leave Application",
            "parent_name": "الاجازات"
        },
        {
            "type": "DocType",
            "doc_name": "Compensatory Leave Request",
            "parent_name": "الاجازات"
        },
        {
            "type": "DocType",
            "doc_name": "Travel Request",
            "parent_name": "الاجازات"
        },
        {
            "type": "DocType",
            "doc_name": "Employee Advance",
            "parent_name": "الاجازات"
        },
        {
            "type": "DocType",
            "doc_name": "Expense Claim",
            "parent_name": "الاجازات"
        },
        {
            "type": "DocType",
            "doc_name": "Loan Type",
            "parent_name": "القروض"
        },
        {
            "type": "DocType",
            "doc_name": "Loan",
            "parent_name": "القروض"
        },
        {
            "type": "DocType",
            "doc_name": "Loan Application",
            "parent_name": "القروض"
        },
        {
            "type": "DocType",
            "doc_name": "Vehicle",
            "parent_name": "ادارة المركبات"
        },
        {
            "type": "DocType",
            "doc_name": "Vehicle Log",
            "parent_name": "ادارة المركبات"
        },
        {
            "type": "DocType",
            "doc_name": "Employee Contract",
            "parent_name": "قائمة الموظفين"
        },
        {
            "type": "DocType",
            "doc_name": "Salary Structure Assignment",
            "parent_name": "قائمة الموظفين"
        },
        {
            "type": "DocType",
            "doc_name": "Leave Encashment",
            "parent_name": "الاجازات"
        },
        {
            "type": "DocType",
            "doc_name": "End Of Service",
            "parent_name": "قائمة الموظفين"
        },
        {
            "type": "DocType",
            "doc_name": "Document Manager",
            "parent_name": "ادارة الوثائق"
        },
        {
            "type": "DocType",
            "doc_name": "Document Type",
            "parent_name": "ادارة الوثائق"
        },
        {
            "type": "DocType",
            "doc_name": "User",
            "parent_name": "ادارة المستخدمين"
        },
        {
            "type": "Report",
            "doc_name": "Files in Saudi banks format",
            "parent_name": "الرواتب والاجور",
            "icon": ""
        }
    ],
    "shortcuts": [],
    "charts": [],
    "notifications": []
  }
def set_sidebar():
    if not frappe.db.exists('DocType', 'System Controller'): return
    sc = frappe.get_doc('System Controller')
    sc.enable = 1
    sc.show_sidebar = 1
    if len(sc.sidebar_labels) == 0:
        for label in side_bar_static['sidebar_labels']:
            sc.append('sidebar_labels', label)
    
    if len(sc.sidebar_item) == 0:
        for label in side_bar_static['sidebar_item']:
            sc.append('sidebar_item', label)
        sc.save(ignore_permissions=True)
        frappe.db.commit()