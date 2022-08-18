# Copyright (c) 2022, Mai and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class TechnicalSupport(Document):
	# def autoname(self):
	# 	self.issue_date = frappe.utils.nowdate()
	def validate(self):
		self.ticket_url = f"{frappe.request.host_url}app/technical-support/{self.name}"

		if self.docstatus == 0:
			if not self.issue_date:
				self.issue_date = frappe.utils.nowdate()

			if not self.company_name:
				c = frappe.db.sql("SELECT name FROM `tabCompany` ORDER BY creation ASC")
				if len(c) > 0: self.company_name = c[0][0]
			
			if not self.user_name:
				self.user_name = frappe.session.user
				self.user_email = frappe.session.email

			self.subject_title = self.subject

	def on_cancel(self):
		self.db_set('status', 'Cancelled')
	
	def on_submit(self):
		self.db_set('status', 'Open')
	
	@frappe.whitelist()
	def mark_complete(self):
		u = frappe.get_doc('User', frappe.session.user)
		if 'Complete Tech Support' not in [r.role for r in u.roles]:
			frappe.msgprint(frappe._("Not allowed to complete Technical Support"))
			return

		if self.docstatus == 1 and self.status == "Open":
			self.db_set('status', 'Completed')
			return "Completed"
