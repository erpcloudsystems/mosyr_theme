

frappe.ui.toolbar.Toolbar.prototype.bind_events = function () {
    $("a.lang-switcher").on('click', async function (ev) {
        if(lang == frappe.boot.lang){return}
        frappe.msgprint(__("Refreshing..."));
        const lang = $(ev.target).attr("data-lang")
        frappe.call({
            'method': 'mosyr_theme.api.change_lang',
            args:{
                'lang': lang
            },
            callback: function(r){
                window.location.reload();
            }
        })
    });
    this.setup_sidebar_toggle();
}

frappe.ui.toolbar.Toolbar.prototype.setup_sidebar_toggle = function() {
    let sidebar_toggle = $('header').find('.custom-menu-btn-toggler');
    sidebar_toggle.click((event) => {
        window.Helpers.toggleCollapsed()
        if (frappe.utils.is_xs() || frappe.utils.is_sm()) {
            event.preventDefault();
            window.Helpers.toggleCollapsed()
        }
    });
}
