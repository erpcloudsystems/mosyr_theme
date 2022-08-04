

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
                console.log(r);
            }
        })
    });
}