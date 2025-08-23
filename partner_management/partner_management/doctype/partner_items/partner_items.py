# Copyright (c) 2025, winspire tech  and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PartnerItems(Document):
    pass

@frappe.whitelist()
def approve_item(docname):
    doc = frappe.get_doc("Partner Items", docname)

    
    frappe.db.set_value("Partner Items", docname, "status", "Accepted")

    
    if not frappe.db.exists("Item", {"item_code": doc.name}):
        item_doc = frappe.get_doc({
            "doctype": "Item",
            "item_code": doc.name,
            "item_name": doc.item_name,
            "gst_hsn_code": doc.hsn_code,
            "stock_uom": doc.uom,
            "is_stock_item": 1,
            "item_group": doc.item_category
        })
        item_doc.insert(ignore_permissions=True)

    frappe.db.commit()
    return f"Item created & Partner Item {docname} approved."


@frappe.whitelist()
def reject_item(docname, reason):
    doc = frappe.get_doc("Partner Items", docname)

    if doc.docstatus == 1 and doc.status == "Pending":
        frappe.db.set_value("Partner Items", docname, {
            "status": "Rejected",
            "rejection_reason": reason
        })
        frappe.db.commit()
        return f"Partner Item {docname} has been Rejected. Reason: {reason}"
    else:
        frappe.throw("Only Pending Partner Items can be rejected.")

