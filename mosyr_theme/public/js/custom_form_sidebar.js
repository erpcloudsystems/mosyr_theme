
frappe.ui.form.Sidebar.prototype.make = function(){
    var sidebar_content = frappe.render_template("navbar", {
        allowed_doctypes: frappe.boot.sidebar_items
    });

    this.sidebar = $('<div class="form-sidebar overlay-sidebar hidden-xs hidden-sm"></div>')
        .html(sidebar_content)
        .appendTo(this.page.sidebar.empty());
        
        this.sidebar.find('a.toggler-btn').on('click', () => {
            $('.layout-side-section').toggleClass('toggle-sidebar');
            $('.nav-app-logo').toggle();
            $('.cus-app-logo').toggleClass('hidden');
            $('.sidebar-item-label').toggleClass('hidden');
            $('.user-account').toggleClass('hidden');
            $('.settings').toggleClass('hidden');
            $('.support-img').toggleClass('hidden');
            $('.toolbar-user').toggleClass('user-settings-list');
            $('.sidebar-reports').toggleClass('sm-nav');
            $('a.toggler-btn').toggleClass('toggle-side-sm-btn');
            $('.dropdown-btn').toggleClass('hide-dropdown-btn');
            $('.drop-down-menu').removeClass('show-menu');
            $('.drop-down-menu').toggleClass('hidden');
        });

        $('a.dropdown-btn').on('click', function(e){
            e.preventDefault();
            $(e.target).parent().next('.drop-down-menu').toggleClass('show-menu');
        })
}
