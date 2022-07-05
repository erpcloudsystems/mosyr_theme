$(document).ready(function () {
    $(".layout-container .layout-side-section").css("display", "none")
    $(".page-head  .sidebar-toggle-btn").css("display", "none")
    
    $(".menu-item").removeClass("active")
    $(".menu-item").removeClass("open")
    let id = frappe.get_route()[1]

    let element = $(id)
    element.closest('.menu-item').addClass("active")
    element.closest('ul').parent().addClass("active")
    element.closest('ul').parent().addClass("open")

    $(".menu-link").click(function (event) {
        set_active_page(event)
    });

    load_sidbar_icons()
    setTimeout(function(){
        if(frappe.get_route()[1] == 'Home'){
            $("#body .content.page-container").addClass("hide")
            $(".custom_content").removeClass("hide")
        }else {
            $(".custom_content").addClass("hide")
        }
    }, 100)
})

function set_active_page(event){
    setTimeout(function() {
        if(frappe.get_route()[1] == 'Home'){
            $("#body .content.page-container").addClass("hide")
            $(".custom_content").removeClass("hide")
        }else {
            $(".custom_content").addClass("hide")
        }
        if ( event.target.id == frappe.get_route()[1]) {
            $(".menu-item").removeClass("active")
            $(".menu-item").removeClass("open")
            $(event.target).closest('.menu-item').addClass("active")
            let elm = $(event.target).closest("ul")
            elm.parent().addClass("active")
            elm.parent().addClass("open")

        }
    }, 100);
}

function load_sidbar_icons(){
    $('.sidebar-icon').each(function(i, obj) {
        let icon_name = $(obj).attr('icon-name')
        $(obj).append(frappe.utils.icon(icon_name || "folder-normal", "md"))
    });
}