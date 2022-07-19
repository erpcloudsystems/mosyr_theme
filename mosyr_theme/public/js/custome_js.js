$(document).ready(function () {
    $(".menu-item").removeClass("active")
    $(".menu-item").removeClass("open")
    let id = frappe.get_route()[1]

    let element = $(id)
    element.closest('.menu-item').addClass("active")
    element.closest('ul').parent().addClass("active")
    element.closest('ul').parent().addClass("open")

    $(".menu-link").click(function (event) {
        window.location.reload();
        set_active_page(event)
    });
    $("#logo").click(function (event) {
        set_active_page(event)
    });

    load_sidbar_icons()
    setTimeout(function () {
        if ( frappe.get_route() == '' || frappe.get_route()[1] == 'Home') {
            $("#body .content.page-container").css("display","none")
            $(".custom_content").removeClass("custome_hide")
        } else {
            $(".custom_content").addClass("custome_hide")
        }
    }, 100)

    set_active_tab()
    $(".custom-menu-btn").click(function (event){
        $("html").toggleClass("layout-menu-expanded")
    })
})

function set_active_page(event) {
    setTimeout(function () {
        if (frappe.get_route()[1] == 'Home') {
            $("#body .content.page-container").css("display","none")
            $(".custom_content").removeClass("custome_hide")
        } else {
            $(".custom_content").addClass("custome_hide")
        }
        if (event.target.id == frappe.get_route()[1]) {
            $(".menu-item").removeClass("active")
            $(".menu-item").removeClass("open")
            $(event.target).closest('.menu-item').addClass("active")
            let elm = $(event.target).closest("ul")
            elm.parent().addClass("active")
            elm.parent().addClass("open")

        }
    }, 100);
}


function set_active_tab(){
    setTimeout(function(){
        $(".menu-item").removeClass("active")
        $(".menu-item").removeClass("open")
        let id = frappe.get_route()[1]
        let element = document.getElementById(id)
        $(element).closest('.menu-item').addClass("active")
        $(element).closest('ul').parent().addClass("active")
        $(element).closest('ul').parent().addClass("open")
    }, 100)
}

function load_sidbar_icons(){
    $('.sidebar-icon').each(function(i, obj) {
        let icon_name = $(obj).attr('icon-name')
        $(obj).append(frappe.utils.icon(icon_name || "folder-normal", "md"))
    });
}