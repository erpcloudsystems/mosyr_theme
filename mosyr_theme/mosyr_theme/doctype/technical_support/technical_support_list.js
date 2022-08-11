// Copyright (c) 2022, Abdullah A. Zaqout and contributors
// For license information, please see license.txt

let imports_in_progress = [];

frappe.listview_settings['Technical Support'] = {
	onload(listview) {},
	get_indicator: function(doc) {
		var colors = {
			'Open': 'orange',
			'Completed': 'green',
			'Draft': 'blue',
			'Cancelled': 'red',
		};
		let status = doc.status;
		return [__(status), colors[status], 'status,=,' + doc.status];
	},
	hide_name_column: true
};
