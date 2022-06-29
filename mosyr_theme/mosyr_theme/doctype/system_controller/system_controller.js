// Copyright (c) 2022, Mai and contributors
// For license information, please see license.txt

frappe.ui.form.on('System Controller', {
    refresh: function(frm) {
        frm.trigger('prepare_sidebar_lables');
    },
    prepare_sidebar_lables: function(frm) {
        let labels = '\n';
        let items = frm.doc['sidebar_labels'] || []
        let final_labels = []
        items.forEach(row => {
            if (row.label) final_labels.push(row.label)
        });
        labels = final_labels.join("\n")
        frm.fields_dict.sidebar_item.grid.update_docfield_property('parent_name', 'options', labels);
    },

    prepare_employee_lables: function(frm) {
        let labels = '\n';
        let items = frm.doc['employee_label'] || []
        let final_labels = []
        items.forEach(row => {
            if (row.label) final_labels.push(row.label)
        });
        labels = final_labels.join("\n")
        frm.fields_dict.employee_shortcuts.grid.update_docfield_property('parent_name', 'options', labels);
    }
});
frappe.ui.form.on('Sidebar Label', {
    sidebar_labels_add(frm, cdt, cdn) { frm.trigger('prepare_sidebar_lables'); },
    sidebar_labels_delete(frm, cdt, cdn) { frm.trigger('prepare_sidebar_lables'); },
    label(frm, cdt, cdn) { frm.trigger('prepare_sidebar_lables'); }
})

;
frappe.ui.form.on('Employee Label', {
    employee_label_add(frm, cdt, cdn) { frm.trigger('prepare_employee_lables'); },
    employee_label_delete(frm, cdt, cdn) { frm.trigger('prepare_employee_lables'); },
    label(frm, cdt, cdn) { frm.trigger('prepare_employee_lables'); }
})