

frappe.ui.toolbar.Toolbar.prototype.bind_events = function () {

    $(".lang-switcher").on('click', function (ev) {
        if (frappe.boot.lang !== $(ev.target).attr("data-lang")) {
            frappe.db
                .set_value("User", frappe.session.user, "language", $(ev.target).attr("data-lang"))
                .then(() => {
                    location.reload();
                })
        }
    });
}