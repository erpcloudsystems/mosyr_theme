// Copyright (c) 2022, Abdullah A. Zaqout and contributors
// For license information, please see license.txt

frappe.ui.form.on('Technical Support', {
	refresh: function (frm) {
		if (frm.doc.docstatus == 1 && frm.doc.status == "Open") {
			frm.add_custom_button(__("Mark as Complete"), function (doc) {
				frappe.confirm(
					__('Are you sure to complete this support ticket?'),
					function () {
						frappe.call({
							method: 'mark_complete',
							doc: frm.doc,
							callback: function (r) { frm.reload_doc() }
						})
					},
					function () { }
				)

			})
		}
	}
});
