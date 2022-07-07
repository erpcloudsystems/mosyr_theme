from __future__ import unicode_literals
import frappe
from frappe import _, DoesNotExistError
from frappe.desk.desktop import Workspace, get_custom_workspace_for_user

@frappe.whitelist()
@frappe.read_only()
def get_desktop_page(page='Home'):
    """Applies permissions, customizations and returns the configruration for a page
    on desk.

    Args:
            page (string): page name

    Returns:
            dict: dictionary of cards, charts and shortcuts to be displayed on website
    """
    page = "Home"
    latest = {
        'label': 'Latest Data',
        'items': {}
    }
    if frappe.session.user == 'Administrator':
        d = frappe.db.sql('SELECT name, status, employee, employee_name FROM `tabLeave Application` WHERE docstatus!=2', as_dict=True)[:5]
        if len(d) > 0:
            latest['items'].update({
                'Leave Application': d
            })
        d = frappe.db.sql('SELECT name, status, employee, employee_name FROM `tabAttendance` WHERE docstatus!=2', as_dict=True)[:5]
        if len(d) > 0:
            latest['items'].update({
                'Attendance': d
            })
    else:
        employee = frappe.get_list('Employee', filters={'user_id': frappe.session.user})
        if employee:
            employee = employee[0].name
            d = frappe.db.sql("""SELECT name, status, employee, employee_name FROM `tabLeave Application` WHERE docstatus!=2 AND employee='{}'""".format(employee), as_dict=True)[:5]
            if len(d) > 0:
                latest['items'].update({
                    'Leave Application': d
                })
            d = frappe.db.sql("""SELECT name, status, employee, employee_name FROM `tabAttendance` WHERE docstatus!=2 AND employee='{}'""".format(employee), as_dict=True)[:5]
            if len(d) > 0:
                latest['items'].update({
                    'Attendance': d
                })


    try:
        wspace = Workspace(page)
        wspace.build_workspace()
        return {
            "charts": wspace.charts,
            "shortcuts": wspace.shortcuts,
            "cards": [],
            "latest": latest,
            "onboarding": wspace.onboarding,
            "allow_customization": not wspace.doc.disable_user_customization,
        }
    except DoesNotExistError:
        frappe.log_error(frappe.get_traceback())
        return {}


@frappe.whitelist()
def reset_customization(page):
    """Reset workspace customizations for a user

    Args:
            page (string): Name of the page to be reset
    """
    ws = get_custom_workspace_for_user(page)
    origin_page = frappe.get_doc('Workspace', page)

    print(ws.name)
    print(origin_page.name)

    if not ws.label:
        ws.label = f"{page}-{frappe.session.user}"
    ws.module = "Setup"
    
    # ws.update(origin_page.as_dict())
    ws.charts = []
    ws.shortcuts = []
    ws.links = []
    for chart in origin_page.charts:
        ws.append('charts', {
            'chart_name': chart.chart_name,
            'label': chart.label or chart.chart_name
        })
    
    for shortcut in origin_page.shortcuts:
        ws.append('shortcuts', {
            'type': shortcut.type,
            'link_to': shortcut.link_to,
            'label': shortcut.label or shortcut.link_to,
            'icon': shortcut.icon or 'folder-open',
            'color': shortcut.color or '#ffffff',
            # 'background': shortcut.background or "#885af8"
        })
    ws.save(ignore_permissions=True)
    frappe.db.commit()