import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def create_custom_fields():
    custom_fields = {
        "Supplier": [
            {
                "fieldname": "is_partner",
                "fieldtype": "Check",
                "label": "Is Partner?",
                "insert_after": "supplier_name",
                "in_list_view": 1,
                "reqd": 0,
            },
            {
                "fieldname": "partner_name",
                "fieldtype": "Link",
                "label": "Partner Name",
                "insert_after": "supplier_type",
                "options": "Partner Details",
                "in_list_view": 1,
                "depends_on": "eval:doc.is_partner==1",
                "mandatory_depends_on": "eval:doc.is_partner==1",
                "reqd": 0,
            },
        ],
        "Address": [
            {
                "fieldname": "is_partner",
                "fieldtype": "Check",
                "label": "Is Partner?",
                "insert_after": "is_shipping_address",
                "in_list_view": 1,
                "reqd": 0,
            }
        ],
    }

    for doctype, fields in custom_fields.items():
        for field in fields:
            if not frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field["fieldname"]}):
                create_custom_field(doctype, field)
                
                frappe.db.commit()
                frappe.clear_cache(doctype=doctype)


def delete_custom_fields():
    custom_fields_to_delete = {
        "Supplier": ["is_partner", "partner_name"],
        "Address": ["is_partner"],
    }

    for doctype, fields in custom_fields_to_delete.items():
        for field_name in fields:
            if frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field_name}):
                frappe.delete_doc("Custom Field", f"{doctype}-{field_name}", ignore_missing=True)
                frappe.db.commit()
                frappe.clear_cache(doctype=doctype)
