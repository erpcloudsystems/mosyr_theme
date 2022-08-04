import frappe

@frappe.whitelist()
def change_lang(lang):
    if not frappe.db.exists('Language', lang):
        lang = "en"
    if frappe.session.user == 'Guest': return
    u = frappe.get_doc('User', frappe.session.user)
    u.language = lang
    u.save()
    frappe.db.commit()
    return 'reload'