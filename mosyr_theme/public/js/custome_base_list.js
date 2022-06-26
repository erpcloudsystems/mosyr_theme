frappe.views.BaseList.prototype.setup_page = function () {
    this.page = this.parent.page;
    this.$page = $(this.parent);
    !this.hide_card_layout && this.page.main.addClass('frappe-card');
    this.page.page_form.removeClass("row").addClass("flex");
    this.hide_page_form && this.page.page_form.hide();
    this.hide_sidebar && this.$page.addClass('no-list-sidebar');
    this.setup_page_head();

    $(".page-head").prependTo($(".layout-main-section-wrapper"));
    $("header").prependTo($(".layout-main-section-wrapper"));
    $(".page-body").removeClass("container");
    $(".layout-main").removeClass("row")
    $(".layout-main").addClass("layout-container")
    $(".layout-container .layout-side-section").removeClass("col-lg-2")
    $(".layout-container .layout-main-section-wrapper").removeClass("col")
    $(".layout-main-section-wrapper").addClass("layout-page")
    $(".layout-container").removeClass("layout-main");
    $(".layout-main-section").addClass("content-wrapper");
    $(".page-head-content").removeClass("row");
    $(".page-title").removeClass("col-md-4");
    $(".page-title").removeClass("col-sm-6");
    $(".page-title").removeClass("col-xs-8 ");
    $(".page-actions").removeClass("col");

    $('<div class="custome-cont container-xxl flex-grow-1 container-p-y"></div>').appendTo(".layout-main-section")
    $(".page-form").appendTo(".custome-cont")
}

frappe.views.BaseList.prototype.setup_list_wrapper =function() {
    this.$frappe_list = $('<div class="frappe-list">').appendTo(".custome-cont");
}