app_name = "partner_management"
app_title = "Partner Management"
app_publisher = "winspire tech "
app_description = "Partner Management"
app_email = "mohammedanas19025@gmail.com"
app_license = "mit"

doc_events = {
    "Supplier": {
        "autoname": "partner_management.customization.supplier_mand.autoname"
    },
    "Sales Order":{
        "on_submit":"partner_management.customization.purchase.create_po_and_pi_for_supplier",
        "on_update":"partner_management.customization.sales_order_notify.notify_supplier_on_draft"
    }
}



fixtures = [
    "Workflow",
    "Workflow State",
    "Workflow Action Master"
]
# doc_events = {
#     "Sales Partner": {
#         "before_insert": "agent_management.customization.sales_partner_customization.set_sales_partner_name"
#     }
# }

after_migrate = [
    "partner_management.customization.supplier_customization.create_custom_fields",
    "partner_management.customization.customer_customisation.disable_customer_name_mandatory"
   
    
]


after_install = ["partner_management.customization.supplier_customization.create_custom_fields",
                 "partner_management.customization.customer_customisation.disable_customer_name_mandatory"]
before_uninstall = ["partner_management.customization.supplier_customization.delete_custom_fields",
                    "partner_management.customization.customer_customisation.enable_customer_name_mandatory"]

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "partner_management",
# 		"logo": "/assets/partner_management/logo.png",
# 		"title": "Partner Management",
# 		"route": "/partner_management",
# 		"has_permission": "partner_management.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/partner_management/css/partner_management.css"
# app_include_js = "/assets/partner_management/js/partner_management.js"

# include js, css files in header of web template
# web_include_css = "/assets/partner_management/css/partner_management.css"
# web_include_js = "/assets/partner_management/js/partner_management.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "partner_management/public/scss/website"

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

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "partner_management/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "partner_management.utils.jinja_methods",
# 	"filters": "partner_management.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "partner_management.install.before_install"
# after_install = "partner_management.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "partner_management.uninstall.before_uninstall"
# after_uninstall = "partner_management.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "partner_management.utils.before_app_install"
# after_app_install = "partner_management.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "partner_management.utils.before_app_uninstall"
# after_app_uninstall = "partner_management.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "partner_management.notifications.get_notification_config"

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
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"partner_management.tasks.all"
# 	],
# 	"daily": [
# 		"partner_management.tasks.daily"
# 	],
# 	"hourly": [
# 		"partner_management.tasks.hourly"
# 	],
# 	"weekly": [
# 		"partner_management.tasks.weekly"
# 	],
# 	"monthly": [
# 		"partner_management.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "partner_management.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "partner_management.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "partner_management.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["partner_management.utils.before_request"]
# after_request = ["partner_management.utils.after_request"]

# Job Events
# ----------
# before_job = ["partner_management.utils.before_job"]
# after_job = ["partner_management.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"partner_management.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

