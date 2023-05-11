
frappe.views.ListView.prototype.setup_columns = function(){
	// setup columns for list view
	this.columns = [];

	const get_df = frappe.meta.get_docfield.bind(null, this.doctype);

	// 1st column: title_field or name
	if (this.meta.title_field) {
		this.columns.push({
			type: "Subject",
			df: get_df(this.meta.title_field),
		});
	} else {
		this.columns.push({
			type: "Subject",
			df: {
				label: __("Name"),
				fieldname: "name",
			},
		});
	}


	this.columns.push({
		type: "Tag"
	});

	// 2nd column: Status indicator
	if (frappe.has_indicator(this.doctype)) {
		// indicator
		this.columns.push({
			type: "Status",
		});
	}

	const fields_in_list_view = this.get_fields_in_list_view();
	// Add rest from in_list_view docfields
	this.columns = this.columns.concat(
		fields_in_list_view
			.filter((df) => {
				if (
					frappe.has_indicator(this.doctype) &&
					df.fieldname === "status"
				) {
					return false;
				}
				if (!df.in_list_view) {
					return false;
				}
				return df.fieldname !== this.meta.title_field;
			})
			.map((df) => ({
				type: "Field",
				df,
			}))
	);

	if (this.list_view_settings.fields) {
		this.columns = this.reorder_listview_fields();
	}

	// limit max to 8 columns if no total_fields is set in List View Settings
	// Screen with low density no of columns 4
	// Screen with medium density no of columns 6
	// Screen with high density no of columns 8
	let total_fields = 6;

	if (window.innerWidth <= 767) {
		total_fields = 4;
	} else if (window.innerWidth >= 1920) {
		total_fields = 8;
	}

	this.columns = this.columns.slice(0, this.list_view_settings.total_fields || total_fields);

	if (
		!this.settings.hide_name_column &&
		this.meta.title_field &&
		this.meta.title_field !== 'name'
	) {
		this.columns.push({
			type: "Field",
			df: {
				label: __("Name"),
				fieldname: "name",
			},
		});
	}
}