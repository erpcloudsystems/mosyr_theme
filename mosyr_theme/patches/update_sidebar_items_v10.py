import frappe


def execute():
    if not frappe.db.exists("DocType", "System Controller"):
        return

    sc = frappe.get_doc("System Controller")

    for row in sc.sidebar_item:
        if row.type == "DocType" and row.doc_name == "Vehicle Service":
            row.doc_name = "Vehicle Services"

            sc.save(ignore_permissions=True)
            frappe.db.commit()
