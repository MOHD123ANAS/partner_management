import frappe
from frappe.utils import nowdate
from frappe.model.document import Document

class PartnerItems(Document):
    pass

@frappe.whitelist()
def approve_item(docname):
    
    doc = frappe.get_doc("Partner Items", docname)

    if not doc.supplier_id:
        frappe.throw("Supplier ID is required to approve this item.")

    supplier_id = doc.supplier_id
    item_name = doc.item_name
    item_group = doc.item_category
    uom = doc.uom
    hsn_code = doc.hsn_code
    price = doc.item_price or 0  

    price_list_name = supplier_id  
    price_list_created_or_updated = False
    if frappe.db.exists("Price List", price_list_name):
        price_list_doc = frappe.get_doc("Price List", price_list_name)
        if not price_list_doc.buying:
            price_list_doc.buying = 1
            price_list_doc.selling = 0
            price_list_doc.save(ignore_permissions=True)
            price_list_created_or_updated = True
    else:
        price_list_doc = frappe.get_doc({
            "doctype": "Price List",
            "price_list_name": price_list_name,
            "buying": 1,
            "selling": 0,
            "enabled": 1
        })
        price_list_doc.insert(ignore_permissions=True)
        price_list_created_or_updated = True

    item_created = False
    if not frappe.db.exists("Item", {"item_name": item_name}):
        item_doc = frappe.get_doc({
            "doctype": "Item",
            "item_code": item_name,  
            "item_name": item_name,
            "item_group": item_group,
            "stock_uom": uom,
            "is_stock_item": 0,
            "gst_hsn_code": hsn_code,
            "delivered_by_supplier":1
        })
        item_doc.insert(ignore_permissions=True)
        item_created = True
    else:
        item_doc = frappe.get_doc("Item", {"item_name": item_name})

    item_price_created = False
    item_price_updated = False

    existing_price = frappe.db.get_value("Item Price", {
        "item_code": item_doc.name,
        "price_list": price_list_name
    }, "price_list_rate")

    if existing_price is None:
        
        item_price_doc = frappe.get_doc({
            "doctype": "Item Price",
            "item_code": item_doc.name,
            "price_list": price_list_name,
            "price_list_rate": price,
            "currency": frappe.db.get_single_value("Global Defaults", "default_currency"),
            "valid_from": nowdate()
        })
        item_price_doc.insert(ignore_permissions=True)
        item_price_created = True
    elif existing_price != price:
        
        frappe.db.set_value("Item Price", {
            "item_code": item_doc.name,
            "price_list": price_list_name
        }, "price_list_rate", price)
        item_price_updated = True


    frappe.db.set_value("Partner Items", docname, "status", "Accepted")
    frappe.db.commit()

    messages = []
    if price_list_created_or_updated:
        messages.append("Price List created/updated")
    if item_created:
        messages.append("Item created")
    if item_price_created:
        messages.append(f"Item Price created at rate {price}")
    if item_price_updated:
        messages.append(f"Item Price updated to rate {price}")

    if not messages:
        frappe.throw("All records already exist and Item Price matches the Partner Item price.")

    return f"Partner Item {docname} approved. " + ". ".join(messages)

@frappe.whitelist()
def reject_item(docname, reason):
    doc = frappe.get_doc("Partner Items", docname)

    if doc.status == "Pending":
        doc.db_set("status", "Rejected", update_modified=True)
        doc.db_set("rejection_reason", reason, update_modified=True)
        frappe.db.commit()
        return f"Partner Item {docname} has been Rejected. Reason: {reason}"
    else:
        frappe.throw("Only Pending Partner Items can be rejected.")
