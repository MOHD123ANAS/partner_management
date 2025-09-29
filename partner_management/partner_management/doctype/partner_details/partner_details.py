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
        if self.business_name and not self.abbr:
            self.abbr = self.get_abbr(self.business_name)

    def validate(self):
        # Ensure posting_date is always set (in case of edits)
        if not self.posting_date:
            self.posting_date = nowdate()

        # Validate GST Number if provided
        if self.gst_number and not re.match(GST_REGEX, self.gst_number):
            frappe.throw(f"Invalid GST Number: {self.gst_number}. Please enter a valid GSTIN.")
    def get_abbr(self, business_name):
        """
        Generate abbreviation from business_name (like ERPNext does for Customer/Supplier)
        Example:
        - "Winspire Technologies" → "WT"
        - "Global Cement Traders" → "GCT"
        """
    # Split words, take first letters, make uppercase
        abbr = "".join(word[0] for word in business_name.strip().split() if word).upper()

        # If abbr is too short, fallback to first 3 chars of business_name
        if len(abbr) < 2:
            abbr = business_name[:3].upper()

        return abbr