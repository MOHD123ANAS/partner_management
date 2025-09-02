# Copyright (c) 2025, winspire tech and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate
import re

GST_REGEX = r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[0-9A-Z]{1}Z[0-9A-Z]{1}$"

class PartnerDetails(Document):
    def before_insert(self):
        # Set posting_date to today if not already set
        if not self.posting_date:
            self.posting_date = nowdate()

    def validate(self):
        # Ensure posting_date is always set (in case of edits)
        if not self.posting_date:
            self.posting_date = nowdate()

        # Validate GST Number if provided
        if self.gst_number and not re.match(GST_REGEX, self.gst_number):
            frappe.throw(f"Invalid GST Number: {self.gst_number}. Please enter a valid GSTIN.")
