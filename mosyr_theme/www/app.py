# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import print_function, unicode_literals
from mosyr_theme.boot import get_sidebar_items
from frappe.utils.jinja import is_rtl
from frappe import _
import frappe.sessions
import frappe
import time
import re
import os

no_cache = 1
base_template_path = "templates/www/app.html"


def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw(_("Log in to access this page."), frappe.PermissionError)
    elif frappe.db.get_value("User", frappe.session.user, "user_type") == "Website User":
        frappe.throw(_("You are not permitted to access this page."),
                     frappe.PermissionError)

    hooks = frappe.get_hooks()
    try:
        boot = frappe.sessions.get()
    except Exception as e:
        boot = frappe._dict(status="failed", error=str(e))
        print(frappe.get_traceback())

    # this needs commit
    csrf_token = frappe.sessions.get_csrf_token()

    frappe.db.commit()

    desk_theme = frappe.db.get_value("User", frappe.session.user, "desk_theme")

    boot_json = frappe.as_json(boot)

    # remove script tags from boot
    boot_json = re.sub(r"\<script[^<]*\</script\>", "", boot_json)

    # TODO: Find better fix
    boot_json = re.sub(r"</script\>", "", boot_json)

    style_urls = hooks["app_include_css"]

    sidebar_items = get_sidebar_items()

    # Dashboard Data
    user_name = frappe.session.user
    # Loans
    total_loans = frappe.db.sql(
        "SELECT SUM(loan_amount) AS total FROM `tabLoan` WHERE docstatus=1", as_dict=True)
    total_loans_amount = total_loans[0].total or 0
    # salaries
    total_salaries = frappe.db.sql(
        "SELECT SUM(net_pay) AS total FROM `tabSalary Slip` WHERE docstatus=1", as_dict=True)
    total_salaries_amount = total_salaries[0].total or 0
    # Leave Encashment
    total_leave_encashment = frappe.db.sql(
        "SELECT SUM(encashment_amount) AS total FROM `tabLeave Encashment` WHERE docstatus=1", as_dict=True)
    total_leave_encashment_amount = total_leave_encashment[0].total or 0
    # Active Employee
    employee = frappe.db.get_list("Employee", filters={"status": "Active"})

    # Timesheets
    timesheet_list = frappe.get_all("Timesheet", fields=[
                                    "employee_name", "total_hours", "parent_project", "customer"], filters={"docstatus": 1},	limit=6)

    # Leaves
    total_leave = frappe.db.sql(
        "SELECT SUM(total_leave_days) AS total FROM `tabLeave Application`", as_dict=True)
    total_leave_days = total_leave[0].total or 0

    approved_leave = frappe.db.sql(
        "SELECT SUM(total_leave_days) AS total FROM `tabLeave Application` WHERE status='Approved'", as_dict=True)
    approved_leave_days = approved_leave[0].total or 0

    total_casual_leave = frappe.db.sql(
        "SELECT SUM(total_leave_days) AS total FROM `tabLeave Application` WHERE status='Approved' and leave_type='Casual Leave'", as_dict=True)
    total_casual_leave_days = total_casual_leave[0].total or 0

    total_sick_leave = frappe.db.sql(
        "SELECT SUM(total_leave_days) AS total FROM `tabLeave Application` WHERE status='Approved' and leave_type='Sick Leave'", as_dict=True)
    total_sick_leave_days = total_sick_leave[0].total or 0

    total_leave_without_pay_leave = frappe.db.sql(
        "SELECT SUM(total_leave_days) AS total FROM `tabLeave Application` WHERE status='Approved' and leave_type='Leave Without Pay'", as_dict=True)
    total_leave_without_pay_leave_days = total_leave_without_pay_leave[0].total or 0

    total_leave_without_pay_leave = frappe.db.sql(
        "SELECT SUM(total_leave_days) AS total FROM `tabLeave Application` WHERE status='Approved' and leave_type='Compensatory Off'", as_dict=True)
    total_leave_without_pay_leave_days = total_leave_without_pay_leave[0].total or 0

    years = ["2022", "2021"]
    list_1 = []
    list_2 = []

    employee_list = frappe.db.get_list("Employee", fields=["name", "date_of_joining"])
    for row in employee_list:
        date = row.get("date_of_joining").strftime("%Y")
        if date in years:
            if date == "2022":
                month = row.get("date_of_joining").strftime("%m")
                list_1.update({
                    month: list_1.get(month)+1
                })
            if date == "2021":
                list_2.update({
                    month: list_2.get(month)+1
                })
                

    context.update(
        {
            "no_cache": 1,
            "build_version": frappe.utils.get_build_version(),
            "include_js": hooks["app_include_js"],
            "include_css": get_rtl_styles(style_urls) if is_rtl() else style_urls,
            "layout_direction": "rtl" if is_rtl() else "ltr",
            "lang": frappe.local.lang,
            "sounds": hooks["sounds"],
            "boot": boot if context.get("for_mobile") else boot_json,
            "desk_theme": desk_theme or "Light",
            "csrf_token": csrf_token,
            "google_analytics_id": frappe.conf.get("google_analytics_id"),
            "google_analytics_anonymize_ip": frappe.conf.get("google_analytics_anonymize_ip"),
            "mixpanel_id": frappe.conf.get("mixpanel_id"),
            "side_items": sidebar_items,
            "user_name": user_name,
            "total_loans_amount": total_loans_amount,
            "total_salaries_amount": total_salaries_amount,
            "timesheet_list": timesheet_list,
            "total_leave_encashment_amount": total_leave_encashment_amount,
            "total_employee": len(employee),
            "total_leave_application": total_leave_days,
            "approved_leave": approved_leave_days,
            "total_casual_leave": total_casual_leave_days,
            "total_sick_leave": total_sick_leave_days,
            "total_leave_without_pay_leave": total_leave_without_pay_leave_days,
            "total_compensatory_leave": total_leave_without_pay_leave_days
        }
    )

    return context


def get_rtl_styles(style_urls):
    rtl_style_urls = []
    for style_url in style_urls:
        rtl_style_urls.append(style_url.replace("/css/", "/css-rtl/"))
    return rtl_style_urls


@frappe.whitelist()
def get_desk_assets(build_version):
    """Get desk assets to be loaded for mobile app"""
    data = get_context({"for_mobile": True})
    assets = [{"type": "js", "data": ""}, {"type": "css", "data": ""}]

    if build_version != data["build_version"]:
        # new build, send assets
        for path in data["include_js"]:
            # assets path shouldn't start with /
            # as it points to different location altogether
            if path.startswith("/assets/"):
                path = path.replace("/assets/", "assets/")
            try:
                with open(os.path.join(frappe.local.sites_path, path), "r") as f:
                    assets[0]["data"] = assets[0]["data"] + "\n" + \
                        frappe.safe_decode(f.read(), "utf-8")
            except IOError:
                pass

        for path in data["include_css"]:
            if path.startswith("/assets/"):
                path = path.replace("/assets/", "assets/")
            try:
                with open(os.path.join(frappe.local.sites_path, path), "r") as f:
                    assets[1]["data"] = assets[1]["data"] + "\n" + \
                        frappe.safe_decode(f.read(), "utf-8")
            except IOError:
                pass

    return {"build_version": data["build_version"], "boot": data["boot"], "assets": assets}
