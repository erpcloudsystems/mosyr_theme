
import frappe

def execute():
    if not frappe.db.exists("DocType", "System Controller"):
        return

    sc = frappe.get_doc("System Controller")
    sc.append("sidebar_labels", {
            "label": "Letters",
            "icon": "small-file",
    })
    sc.append("sidebar_item", {
            "type": "DocType",
            "doc_name": "Letter",
            "parent_name": "Letters",
            "icon": "",
    })

    sc.save(ignore_permissions=True)
    frappe.db.commit()
