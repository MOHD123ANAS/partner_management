import frappe
from frappe.utils.file_manager import save_file

@frappe.whitelist(allow_guest=False)
def upload_partner_with_file():
    

    
    uploaded_file = frappe.local.request.files.get("file")
    if not uploaded_file:
        frappe.throw("File is required")

    
    file_doc = save_file(
        uploaded_file.filename,      
        uploaded_file.read(),        
        None,                        
        None,                        
        is_private=0
    )

    
    partner_data = {
        "doctype": "Partners List",
        "partner_name": frappe.form_dict.get("partner_name"),
        "partner_business_name": frappe.form_dict.get("partner_business_name"),
        "gst_number": frappe.form_dict.get("gst_number"),
        "business_established_date": frappe.form_dict.get("business_established_date"),
        "contact_number": frappe.form_dict.get("contact_number"),
        "contact_email_id": frappe.form_dict.get("contact_email_id"),
        "address_line_1": frappe.form_dict.get("address_line_1"),
        "address_line_2":frappe.form_dict.get("address_line_2"),
        "city": frappe.form_dict.get("city"),
        "pincode": frappe.form_dict.get("pincode"),
        "explain_about_your_business":frappe.form_dict.get("explain_about_your_business"),
        "source":frappe.form_dict.get("source"),
        "state": frappe.form_dict.get("state"),
        "country": frappe.form_dict.get("country", "India"),
        "referred_by_agent":frappe.form_dict.get("referred_by_agent"),
        "agent_id":frappe.form_dict.get("agent_id"),
        "gst_detailspdf_format": file_doc.file_url
    }

    
    partner = frappe.get_doc(partner_data).insert()
    frappe.db.commit()

    return {
        "message": "Partner created successfully",
        "partner": partner.name,
        "file_url": file_doc.file_url
    }
