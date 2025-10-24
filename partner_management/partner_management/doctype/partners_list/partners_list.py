import frappe
from frappe.model.document import Document
from frappe.utils import cint

class PartnersList(Document):
    def before_submit(self):
        
        if self.status not in ["Approved", "Rejected"]:
            frappe.throw("You can only submit if the status is 'Approved' or 'Rejected'.")

        if self.status == "Approved":
            if not self.partner_name:
                frappe.throw("Enter Partner Name.")
            if not self.contact_number:
                frappe.throw("Enter Contact Number.")
            if not self.contact_email_id:
                frappe.throw("Enter Email.")
            if not cint(self.gst_not_applicable) and not self.gst_detailspdf_format:
                frappe.throw("Attach GST File before submitting.")

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
