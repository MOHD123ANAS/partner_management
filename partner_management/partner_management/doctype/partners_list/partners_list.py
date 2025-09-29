# Copyright (c) 2025, winspire tech  and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import base64

class PartnersList(Document):
    def before_submit(self):
        if self.status not in ["Approved", "Rejected"]:
            frappe.throw("You can only submit if the status is 'Approved' or 'Rejected'.")

    def on_submit(self):
        if self.status == "Approved":
            
            
            partner_doc = frappe.new_doc("Partner Details")
            partner_doc.business_name = self.partner_business_name
            partner_doc.partner_name = self.partner_name
            partner_doc.gst_number = self.gst_number
            partner_doc.address_line_1 = self.address_line_1
            partner_doc.address_line_2 = self.address_line_2
            partner_doc.pincode = self.pincode
            partner_doc.city = self.city
            partner_doc.state = self.state
            partner_doc.country = self.country
            partner_doc.contact_number = self.contact_number
            partner_doc.contact_email = self.contact_email_id

            if self.referred_by_agent == 1:
                partner_doc.sales_agent_refferal = self.agent_id

            partner_doc.posting_date = frappe.utils.nowdate()
            partner_doc.insert(ignore_permissions=True)

            
            if getattr(self, "gst_detailspdf_format", None):
                try:
                    file_content = base64.b64decode(self.gst_detailspdf_format)

                    
                    file_doc = frappe.get_doc({
                        "doctype": "File",
                        "file_name": f"{self.partner_name}_GST.pdf",
                        "attached_to_doctype": "Partner Details",
                        "attached_to_name": partner_doc.name,
                        "is_private": 1,
                        "content": file_content
                    })
                    file_doc.insert(ignore_permissions=True)
                except Exception as e:
                    frappe.log_error(frappe.get_traceback(), f"Failed to save GST PDF for {self.name}")

