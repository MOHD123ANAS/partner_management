# Copyright (c) 2025, winspire tech  and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PartnersList(Document):
    def before_submit(self):
        
        if self.status not in ["Approved", "Rejected"]:
            frappe.throw("You can only submit if the status is 'Approved' or 'Rejected'.")

    def on_submit(self):
        if self.status == "Approved":
            
            partner_doc = frappe.new_doc("Partner Details")
            
            
            partner_doc.business_name = self.partner_business_name
            partner_doc.partner_name = self.partner_name  # also set partner_name
            partner_doc.gst_number = self.gst_number
            partner_doc.address_line_1 = self.address_line_1
            partner_doc.address_line_2 = self.address_line_2
            partner_doc.pincode=self.pincode
            partner_doc.city=self.city
            partner_doc.state = self.state
            partner_doc.country=self.country
            partner_doc.contact_number=self.contact_number
            partner_doc.contact_email=self.contact_email_id



            
            if hasattr(self, "gst_number"):
                partner_doc.gst_number = self.gst_number

            partner_doc.posting_date = frappe.utils.nowdate()

            
            partner_doc.insert(ignore_permissions=True)

            

