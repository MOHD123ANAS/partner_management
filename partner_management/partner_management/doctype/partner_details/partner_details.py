# Copyright (c) 2025, winspire tech and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate

class PartnerDetails(Document):
    def before_insert(self):
        # Set posting_date to today if not already set
        if not self.posting_date:
            self.posting_date = nowdate()

    def validate(self):
        # Ensure posting_date is always set (in case of edits)
        if not self.posting_date:
            self.posting_date = nowdate()
