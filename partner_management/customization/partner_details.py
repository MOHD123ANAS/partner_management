import frappe

@frappe.whitelist()
def create_supplier(partner_details_name):
    
    partner = frappe.get_doc("Partner Details", partner_details_name)
    
    partner_name_human = partner.partner_name.strip() if partner.partner_name else None
    gst_number = partner.gst_number.strip() if partner.gst_number else None

    
    if not partner_name_human:
        frappe.throw("Partner Name is empty in Partner Details!")
    if not gst_number:
        frappe.throw("GST number is missing in Partner Details!")
    if not partner.state:
        frappe.throw("State is required for creating a Supplier address in India!")
    if not getattr(partner, "city", None):
        frappe.throw("City is required for creating a Supplier address!")

    
    existing_supplier = frappe.db.get_value("Supplier", {"gstin": gst_number}, "name")
    if existing_supplier:
        frappe.throw(f"A Supplier with GST number {gst_number} already exists: {existing_supplier}")

    
    supplier = frappe.get_doc({
        "doctype": "Supplier",
        "supplier_name": partner_name_human,
        "is_partner": 1,
        "partner_name": partner.name,  
        "gstin": gst_number
    })
    supplier.insert(ignore_permissions=True)

    
    address = frappe.get_doc({
        "doctype": "Address",
        "address_title": partner_name_human,
        "address_type": "Shipping",
        "is_shipping_address":1,
        "address_line1": partner.address_line_1,
        "address_line2": partner.address_line_2,
        "city": partner.city,
        "state": partner.state,
        "pincode": partner.pincode,
        "country": partner.country,
        "phone": partner.contact_number,
        "email_id": partner.contact_email,
        "is_partner":1,
        "links": [{"link_doctype": "Supplier", "link_name": supplier.name}]
    })
    address.insert(ignore_permissions=True)

    frappe.db.commit()

    return supplier.name
