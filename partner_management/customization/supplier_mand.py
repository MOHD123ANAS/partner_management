# apps/partner_management/partner_management/customization/supplier_mand.py
import re
from frappe import _
from frappe.model.naming import make_autoname
import frappe

def autoname(doc, method):
    
    if doc.is_partner and doc.partner_name:
        
        safe_partner = re.sub(r'[^A-Za-z0-9-]+', '', doc.partner_name).upper()
        
        doc.name = make_autoname(f"SUP-{safe_partner}-.####")
    
