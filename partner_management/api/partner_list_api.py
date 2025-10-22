import frappe
from frappe.utils.file_manager import save_file

@frappe.whitelist(allow_guest=False)
def upload_partner_with_file():
    # Get file from request
    uploaded_file = frappe.local.request.files.get("file")
    partner_fields = frappe.form_dict

    # Step 1: Create partner doc (without file)
    partner = frappe.get_doc({
        "doctype": "Partners List",
        "partner_name": partner_fields.get("partner_name"),
        "partner_business_name": partner_fields.get("partner_business_name"),
        "gst_number": partner_fields.get("gst_number"),
        "business_established_date": partner_fields.get("business_established_date"),
        "contact_number": partner_fields.get("contact_number"),
        "contact_email_id": partner_fields.get("contact_email_id"),
        "address_line_1": partner_fields.get("address_line_1"),
        "address_line_2": partner_fields.get("address_line_2"),
        "city": partner_fields.get("city"),
        "pincode": partner_fields.get("pincode"),
        "explain_about_your_business": partner_fields.get("explain_about_your_business"),
        "source": partner_fields.get("source"),
        "state": partner_fields.get("state"),
        "country": partner_fields.get("country", "India"),
        "referred_by_agent": partner_fields.get("referred_by_agent"),
        "agent_id": partner_fields.get("agent_id"),
        "gst_not_applicable": partner_fields.get("gst_not_applicable"),
        "reason_for_not_applying_gst": partner_fields.get("reason_for_not_applying_gst")
    }).insert(ignore_permissions=True)

    file_url = None

    # Step 2: If file exists, attach to partner document
    if uploaded_file:
        file_doc = save_file(
            uploaded_file.filename,
            uploaded_file.read(),
            "Partners List",
            partner.name,
            is_private=0
        )

        # update partner field with file URL
        partner.db_set("gst_detailspdf_format", file_doc.file_url)
        file_url = file_doc.file_url

    frappe.db.commit()

    return {
        "message": "Partner created successfully",
        "partner": partner.name,
        "file_url": file_url
    }
