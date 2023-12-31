from . import __version__ as app_version

app_name = "mosyr_theme"
app_title = "Mosyr Theme"
app_publisher = "Mai"
app_description = "Theme"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "mai.mq.1995@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = [
	"/assets/mosyr_theme/build/css/mosyr_theme.min.css",
	"/assets/mosyr_theme/build/css-rtl/mosyr_theme_rtl.min.css"
]

app_include_js = [
	"/assets/mosyr_theme/build/js/web/web-js.min.js",
	"/assets/mosyr_theme/build/js/frappe-custom.min.js",
	"/assets/mosyr_theme/build/ui/mosyr_theme.min.js",
]

# base_template = "templates/custome-base.html"

# include js, css files in header of web template
web_include_css = ["/assets/mosyr_theme/build/css/web/web-css.min.css"]
web_include_js =  ["/assets/mosyr_theme/build/js/web/web-js.min.js"]

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "mosyr_theme/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "app"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "mosyr_theme.install.before_install"
after_install = "mosyr_theme.install.after_install"


# Uninstallation
# ------------

# before_uninstall = "mosyr_theme.uninstall.before_uninstall"
# after_uninstall = "mosyr_theme.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "mosyr_theme.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"mosyr_theme.tasks.all"
# 	],
# 	"daily": [
# 		"mosyr_theme.tasks.daily"
# 	],
# 	"hourly": [
# 		"mosyr_theme.tasks.hourly"
# 	],
# 	"weekly": [
# 		"mosyr_theme.tasks.weekly"
# 	]
# 	"monthly": [
# 		"mosyr_theme.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "mosyr_theme.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.desktop.get_desktop_page": "mosyr_theme.desktop.get_desktop_page",
# 	"frappe.desk.desktop.reset_customization": "mosyr_theme.desktop.reset_customization"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "mosyr_theme.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"mosyr_theme.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []

extend_bootinfo = "mosyr_theme.boot.boot_session"

website_context = {
    "favicon": "/assets/mosyr_theme/img/min-mosyrlogo.png",
    "splash_image": "/assets/mosyr_theme/img/mosyrlogo.png"
}

# website_redirects = [
#     {"source": "/app/home", "target": "/app"}
# ]

fixtures = [
    {"dt": "Role", "filters": [
        [
            "name", "in", [
                "Complete Tech Support"
            ]
        ]
    ]},
	{"dt": "Webhook", "filters": [
        [
            "name", "in", [
                "HOOK-0001"
            ]
        ]
    ]},
	{"dt": "Translation"}
]