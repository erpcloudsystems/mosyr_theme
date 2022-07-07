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
    $("#logo").click(function (event) {
        set_active_page(event)
    });

    load_sidbar_icons()
    setTimeout(function () {
        if ( frappe.get_route() == '' || frappe.get_route()[1] == 'Home') {
            $("#body .content.page-container").addClass("custome_hide")
            $(".custom_content").removeClass("custome_hide")
        } else {
            $(".custom_content").addClass("custome_hide")
        }
    }, 100)

    load_chart()
})

function set_active_page(event) {
    setTimeout(function () {
        if (frappe.get_route()[1] == 'Home') {
            $("#body .content.page-container").addClass("custome_hide")
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

function load_sidbar_icons() {
    $('.sidebar-icon').each(function (i, obj) {
        let icon_name = $(obj).attr('icon-name')
        $(obj).append(frappe.utils.icon(icon_name || "folder-normal", "md"))
    });
}

function load_chart() {
    const chartOrderStatistics = document.querySelector('#orderStatisticsChart'),
    orderChartConfig = {
        chart: {
            height: 165,
            width: 130,
            type: 'donut'
        },
        labels: ['Electronic', 'Sports', 'Decor', 'Fashion'],
        series: [50, 20, 60, 50],
        colors: [config.colors.primary, config.colors.secondary, config.colors.info, config.colors.success],
        stroke: {
            width: 5,
            colors: cardColor
        },
        dataLabels: {
            enabled: false,
            formatter: function (val, opt) {
                return parseInt(val) + '%';
            }
        },
        legend: {
            show: false
        },
        grid: {
            padding: {
                top: 0,
                bottom: 0,
                right: 15
            }
        },
        plotOptions: {
            pie: {
                donut: {
                    size: '75%',
                    labels: {
                        show: true,
                        value: {
                            fontSize: '1.5rem',
                            fontFamily: 'Public Sans',
                            color: headingColor,
                            offsetY: -15,
                            formatter: function (val) {
                                return parseInt(val) + '%';
                            }
                        },
                        name: {
                            offsetY: 20,
                            fontFamily: 'Public Sans'
                        },
                        total: {
                            show: true,
                            fontSize: '0.8125rem',
                            color: axisColor,
                            label: 'Maaaaaaaaaaaaaaaaaaai',
                            formatter: function (w) {
                                return '30%';
                            }
                        }
                    }
                }
            }
        }
    };
    if (typeof chartOrderStatistics !== undefined && chartOrderStatistics !== null) {
        const statisticsChart = new ApexCharts(chartOrderStatistics, orderChartConfig);
        statisticsChart.render();
    }
}