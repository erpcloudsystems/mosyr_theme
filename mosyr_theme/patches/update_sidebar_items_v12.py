
import frappe


def execute():
    if not frappe.db.exists("DocType", "System Controller"):
        return

    v_services = frappe.get_list("SideBar Item Table", ["doc_name", "name"], {"doc_name": "Vehicle Services", "parent": "System Controller"})
    if len(v_services) > 0:
        for row in v_services:
            frappe.delete_doc("SideBar Item Table", row.name, True)
            frappe.db.commit()

    frappe.reload_doctype("System Controller")
    # frappe.db.commit()
