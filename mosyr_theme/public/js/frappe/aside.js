frappe.provide("frappe.ui.toolbar");
frappe.provide('frappe.search');

frappe.ui.toolbar.MosyrSidebar = class {
	constructor() {
		let sidebar_items = []
		$('#mosyrsidebar').empty()
		$('#mosyrsidebar').html(frappe.render_template("sidebar", {
			navbar_settings: frappe.boot.navbar_settings,
			side_items: frappe.boot.sidebar_items || []
		}));

		this.make();
		this.bind_events()
	}

	make() { }
	bind_events() {
		$("#mosyrsidebar .menu-item > a.menu-link.menu-toggle").on('click', function (ev) {
			ev.stopPropagation()
			if ($($(ev.target).parent()).hasClass('open')){
				$("#mosyrsidebar .menu-item").removeClass("open")
				return
			}
			$("#mosyrsidebar .menu-item").removeClass("open")
			$("#mosyrsidebar .menu-item").removeClass("active")

			$(ev.target).parent().addClass("open")
			$(ev.target).parent().addClass("active")

		})
	}
};

frappe.Application.prototype.make_nav_bar = function () {
	// toolbar
	if (frappe.boot && frappe.boot.home_page !== 'setup-wizard') {
		frappe.frappe_toolbar = new frappe.ui.toolbar.Toolbar();
		frappe.frappe_mosyr_sidebar = new frappe.ui.toolbar.MosyrSidebar();
	}

}