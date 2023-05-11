
frappe.ui.Page.prototype.add_main_section = function () {
    $(frappe.render_template("page", {})).appendTo(this.wrapper);
    if (this.single_column) {
        // nesting under col-sm-12 for consistency
        this.add_view("main", '<div class="row layout-main">\
                    <div class="col-md-12 layout-main-section-wrapper">\
                        <div class="employee-cards row g-4 mb-4"></div>\
                        <div class="layout-main-section"></div>\
                        <div class="layout-footer hide"></div>\
                    </div>\
                </div>');
    } else {
        this.add_view("main", `
                <div class="row layout-main">
                    <div class="col-lg-2 layout-side-section"></div>
                    <div class="col layout-main-section-wrapper">
                        <div class="employee-cards row g-4 mb-4"></div>\
                        <div class="layout-main-section"></div>
                        <div class="layout-footer hide"></div>
                    </div>
                </div>
            `);
    }

    this.setup_page();
}

frappe.views.Container.prototype.change_to = function (label) {
    cur_page = this;
    if (this.page && this.page.label === label) {
        $(this.page).trigger('show');
    }
    var me = this;
    if (label.tagName) {
        // if sent the div, get the table
        var page = label;
    } else {
        var page = frappe.pages[label];
    }
    if (!page) {
        console.log(__('Page not found') + ': ' + label);
        return;
    }
    // hide dialog
    if (window.cur_dialog && cur_dialog.display && !cur_dialog.keep_open) {
        if (!cur_dialog.minimizable) {
            cur_dialog.hide();
        } else if (!cur_dialog.is_minimized) {
            cur_dialog.toggle_minimize();
        }
    }
    // hide current
    if (this.page && this.page != page) {
        $(this.page).hide();
        $(this.page).trigger('hide');
    }
    // show new
    if (!this.page || this.page != page) {
        this.page = page;
        // $(this.page).fadeIn(300);
        $(this.page).show();
    }
    $(document).trigger("page-change");

    this.page._route = frappe.router.get_sub_path();
    $(this.page).trigger('show');
    !this.page.disable_scroll_to_top && frappe.utils.scroll_to(0);
    frappe.breadcrumbs.update();

    let currentDoc = frappe.get_route()[1]
    let listCurrentDoc = frappe.get_route()[0]
    if (currentDoc == 'Employee' && listCurrentDoc == 'List') {
        async function totalInactive(status) {
            let total = await frappe.db.get_list('Employee', { filters: { 'status': status }, limit:50000000 })
            let template = `    
                            <div class="col-sm-6 col-xl-4">
                                <div class="card">
                                    <div class="card-body">
                                        <div class="d-flex align-items-start justify-content-between">
                                            <div class="content-left">
                                                <span>${__(status)}</span>
                                                <div class="d-flex align-items-end mt-2">
                                                    <h4 class="mb-0 me-2 ${status == 'Active' ? 'text-success' : status == 'Inactive' ? 'text-secondary' : status == 'On Leave' ? 'text-primary' : 'text-warning'}">${total.length} </h4>
                                                </div>
                                                <small> ${__( "Total " + status + " Employee")} </small>
                                            </div>
                                            <span class="badge ${status == 'Active' ? 'bg-label-success' : status == 'Inactive' ? 'bg-label-secondary' : status == 'On Leave' ? 'bg-label-primary' : 'bg-label-warning'} rounded p-2">
                                                <i class="bx bx-user bx-sm"></i>
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        `
            $('.employee-cards').prepend(template)
        }
        totalInactive('Active')
        totalInactive('Inactive')
        totalInactive('Left')
    } else {
        $('.employee-cards').empty();
    }

    if (currentDoc == 'Loan' && listCurrentDoc == 'List') {
        $(document).ready(function(){
            setTimeout(function() { 
                frappe.call({
                    'method': 'mosyr_theme.api.get_loan_totals',
                    callback: function(r){
                        let totals = r.message.totals
                        const totals_result = `
                            <p class="total-title">Total Payable Amount: <span class="total-val">${totals.total_payment}</span></p>
                            <p class="total-title">Total Amount Paid: <span class="total-val">${totals.total_amount_paid}</span></p>
                            <p class="total-title">Total Amount Remaining: <span class="total-val">${totals.total_amount_remaining}</span></p>
                        `;
                        $("#loan-totals").append(totals_result)
                        $('#loan-totals').css("border-top","1px solid #f4f5f6");
                    }
                })
            }, 2000);
        });
    } else {
        $('#loan-totals').empty();
    }

    return this.page;
}