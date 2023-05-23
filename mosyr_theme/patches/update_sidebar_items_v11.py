
import frappe


def execute():
    if not frappe.db.exists("DocType", "System Controller"):
        return

    sc = frappe.get_doc("System Controller")
    sc.append("sidebar_item", {
            "type": "DocType",
            "doc_name": "Vehicle Services",
            "parent_name": "Self service",
            "icon": "",
    })

    sc.save(ignore_permissions=True)
    frappe.db.commit()
