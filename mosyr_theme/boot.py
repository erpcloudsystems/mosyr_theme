
from cmath import log
from operator import le
import frappe

def boot_session(bootinfo):
    bootinfo.language = frappe.local.lang
    bootinfo.sidebar_items = get_sidebar_items()
    bootinfo.desk_settings = get_desk_settings()

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

