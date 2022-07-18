# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import print_function, unicode_literals
import this
from mosyr_theme.boot import get_sidebar_items
from frappe.utils.jinja import is_rtl
from frappe import _
import frappe.sessions
import frappe
from datetime import date
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

    """ 
    1. Get today date . today() 
    2. Get current year from step 1.
    3. sql to get emp join in this year . ( total employee for year X)
    4. sql to get emp join in this year-1 . ( total employee for year Y)

    5- For year Y example 1.1.2021 , get last month for the current date 31.1.2021 this month number 1 
    Now we have from and To to get employees .
    6- Sql total number like step 4 and 4.
    7- add 1 month to year Y .
    8 - get last month 
    7 do sql 
    repeat with each month until you reach a 12 -- then stop .

    """

    result = get_growth_persentage()
    growth_persentage = result.get("growth_persentage")
    total_employees_in_current_year = result.get("total_employees_in_current_year")
    total_employees_in_prev_year = result.get("total_employees_in_prev_year")

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
            "total_compensatory_leave": total_leave_without_pay_leave_days,
            "growth_persentage": growth_persentage,
            "current_year": date.today().year,
            "prev_year": (date.today().year) - 1,
            "total_employees_in_current_year": total_employees_in_current_year,
            "total_employees_in_prev_year": total_employees_in_prev_year
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


@frappe.whitelist()
def get_growth_persentage():
    """
        Calculate growth persentage
        20 - 10  = 10
        10/10 = 1
        1 * 100 = 100%
    """
    from datetime import date

    def get_total_emp(year):
        first_day_of_year = date(year, 1, 1)
        last_day_of_year = date(year, 12, 31)

        result = frappe.db.sql("""
            SELECT
                name
            FROM
                `tabEmployee`
            WHERE
                status=%(status)s AND date_of_joining BETWEEN %(first_day)s AND %(last_day)s
        """, {"status": "Active", "first_day": first_day_of_year, "last_day": last_day_of_year}, as_dict=True)

        return len(result)

    current_year = date.today().year
    prev_year = current_year - 1

    total_employees_in_current_year = get_total_emp(current_year)
    total_employees_in_prev_year = get_total_emp(prev_year)

    diff_no = total_employees_in_current_year - total_employees_in_prev_year

    growth_persentage = (diff_no / (total_employees_in_prev_year or 1)) * 100

    return {
        "growth_persentage":growth_persentage,
        "total_employees_in_current_year": total_employees_in_current_year,
        "total_employees_in_prev_year":total_employees_in_prev_year
    }
