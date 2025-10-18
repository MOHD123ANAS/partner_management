import frappe

@frappe.whitelist()
def create_supplier(partner_details_name):
    partner = frappe.get_doc("Partner Details", partner_details_name)

    partner_name_human = partner.business_name.strip() if partner.business_name else None
    gst_number = partner.gst_number.strip() if partner.gst_number else None
    sales_agent = getattr(partner, "sales_agent_refferal", None)

    
    if not partner_name_human:
        frappe.throw("Partner Name is empty in Partner Details!")
    if not partner.state:
        frappe.throw("State is required for creating a Supplier address in India!")
    if not getattr(partner, "city", None):
        frappe.throw("City is required for creating a Supplier address!")

    
    if gst_number:
        existing_supplier = frappe.db.get_value("Supplier", {"gstin": gst_number}, "name")
        if existing_supplier:
            frappe.throw(f"A Supplier with GST number {gst_number} already exists: {existing_supplier}")

    
    supplier_data = {
        "doctype": "Supplier",
        "supplier_name": partner_name_human,
        "is_partner": 1,
        "partner_name": partner.name,
    }


    if gst_number:
        supplier_data["gstin"] = gst_number

    
    if sales_agent:
        supplier_data["sales_partner"] = sales_agent

    supplier = frappe.get_doc(supplier_data)
    supplier.insert(ignore_permissions=True)

    
    address = frappe.get_doc({
        "doctype": "Address",
        "address_title": partner_name_human,
        "address_type": "Shipping",
        "is_shipping_address": 1,
        "address_line1": partner.address_line_1,
        "address_line2": partner.address_line_2,
        "city": partner.city,
        "state": partner.state,
        "pincode": partner.pincode,
        "country": partner.country,
        "phone": partner.contact_number,
        "email_id": partner.contact_email,
        "is_partner": 1,
        "links": [{"link_doctype": "Supplier", "link_name": supplier.name}]
    })
    address.insert(ignore_permissions=True)

    
    price_list_name = f"{supplier.name}"
    existing_price_list = frappe.db.exists("Price List", {"price_list_name": price_list_name})

    if not existing_price_list:
        price_list = frappe.get_doc({
            "doctype": "Price List",
            "price_list_name": price_list_name,
            "buying": 1,
            "selling": 0,
            "enabled": 1,
            "currency": frappe.db.get_single_value("Global Defaults", "default_currency") or "INR"
        })
        price_list.insert(ignore_permissions=True)
        price_list_name = price_list.name
    else:
        price_list_name = existing_price_list

    
    supplier.default_price_list = price_list_name
    supplier.save(ignore_permissions=True)

    
    partner.supplier = supplier.name
    partner.save(ignore_permissions=True)

    return supplier.name
