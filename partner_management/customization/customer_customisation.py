import frappe

def disable_customer_name_mandatory():
    
    frappe.db.sql("""
        UPDATE `tabDocField`
        SET reqd = 0
        WHERE parent = 'Customer' AND fieldname = 'customer_name'
    """)
    frappe.clear_cache(doctype="Customer")

def enable_customer_name_mandatory():
    
    frappe.db.sql("""
        UPDATE `tabDocField`
        SET reqd = 1
        WHERE parent = 'Customer' AND fieldname = 'customer_name'
    """)
    frappe.clear_cache(doctype="Customer")
