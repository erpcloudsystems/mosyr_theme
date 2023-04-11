def execute():
    import frappe
    from mosyr_theme.install import side_bar_static

    if not frappe.db.exists("DocType", "System Controller"):
        return
    sc = frappe.get_doc("System Controller")
    sc.enable = 1
    sc.show_sidebar = 1
    sc.sidebar_labels = []
    sc.sidebar_item = []

    for label in side_bar_static["sidebar_labels"]:
        sc.append("sidebar_labels", label)

    for label in side_bar_static["sidebar_item"]:
        sc.append("sidebar_item", label)
    sc.save(ignore_permissions=True)
    frappe.db.commit()
