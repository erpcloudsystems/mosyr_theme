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


@frappe.whitelist()
def get_loan_totals():
    totals = frappe.db.sql("""
                            SELECT SUM(total_payment) as total_payment, SUM(total_amount_paid) as total_amount_paid,
                                SUM(total_amount_remaining) as total_amount_remaining
                            FROM tabLoan
                            WHERE docstatus = 1
                        """, as_dict=1)[0]
    return {"totals":totals}