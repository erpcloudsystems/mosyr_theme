$(document).ready(function () {
    $("header").prependTo($(".layout-main-section-wrapper"));
    $(".page-head").css("display", "none")
    $(".page-body").removeClass("container")
    $(".main-section").addClass("layout-wrapper layout-content-navbar")
    $(".layout-main").removeClass("row")
    $(".layout-main").addClass("layout-container")
    $(".layout-container .layout-side-section").removeClass("col-lg-2")
    $(".layout-container .layout-main-section-wrapper").removeClass("col")
    $(".layout-main-section-wrapper").addClass("layout-page")
    $(".layout-container").removeClass("layout-main")
    $(".layout-main-section").addClass("content-wrapper")
    $(".desk-page").addClass("container-xxl flex-grow-1 container-p-y")
})