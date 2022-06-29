import frappe

default_home_workspace = {
 'label': 'Home',
 'for_user': None,
 'extends': None,
 'module': 'Setup',
 'category': 'Modules',
 'icon': 'getting-started',
 'restrict_to_domain': None,
 'onboarding': None,
 'extends_another_page': 0,
 'is_default': 0,
 'is_standard': 0,
 'developer_mode_only': 0,
 'disable_user_customization': 0,
 'pin_to_top': 1,
 'pin_to_bottom': 0,
 'hide_custom': 0,
 'charts_label': None,
 'shortcuts_label': None,
 'cards_label': None,
 'doctype': 'Workspace',
 'charts': [],
 'shortcuts': [],
 'links': []
}

def clear_home_workspace():
    if not frappe.db.exists('Workspace', 'Home'):
        ws = frappe.new_doc('Workspace')
        ws.update(default_home_workspace)
        ws.insert(ignore_permissions=True)
        frappe.db.commit()
    else:
        ws = frappe.get_doc('Workspace', 'Home')
        ws.charts = []
        ws.shortcuts = []
        ws.links = []

def check_home_workspace():
    if not frappe.db.exists('Workspace', 'Home'):
        ws = frappe.new_doc('Workspace')
        ws.update(default_home_workspace)
        ws.insert(ignore_permissions=True)
        frappe.db.commit()
        return ws
    else:
        return frappe.get_doc('Workspace', 'Home')

def make_user_workspace(user):
    if len(frappe.get_list('Workspace', filters={'for_user': user, 'extends': 'Home'})) > 0:
        return

    if frappe.db.exists('User', user):    
        ws = check_home_workspace()
        ws = frappe.new_doc('Workspace')
        ws.update(ws.as_dict())
        ws.for_user = user
        ws.extends = 'Home'
        ws.label = f"{default_home_workspace['label']}-{user}"
        ws.insert(ignore_permissions=True)
        frappe.db.commit()




