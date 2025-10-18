import frappe
from frappe.utils import nowdate

@frappe.whitelist()
def create_po_and_pi_for_supplier(doc, method):

    supplier_items = {}
    
    # Collect items grouped by supplier
    for item in doc.items:
        if item.delivered_by_supplier and item.supplier:
            if item.supplier not in supplier_items:
                supplier_items[item.supplier] = []
            supplier_items[item.supplier].append(item)
    
    for supplier, items in supplier_items.items():
        # Create Purchase Order
        po = frappe.get_doc({
            "doctype": "Purchase Order",
            "supplier": supplier,
            "transaction_date": nowdate(),
            "schedule_date": nowdate(),
            "items": []
        })

        for so_item in items:
            po.append("items", {
                "item_code": so_item.item_code,
                "qty": so_item.qty,
                "rate": so_item.rate,  
                "sales_order": doc.name,
                "so_detail": so_item.name
            })
        
        po.insert(ignore_permissions=True)
        po.submit()
        
        
        pi = frappe.get_doc({
            "doctype": "Purchase Invoice",
            "supplier": supplier,
            "posting_date": nowdate(),
            "items": []
        })

        for po_item in po.items:
            pi.append("items", {
                "item_code": po_item.item_code,
                "qty": po_item.qty,
                "rate": po_item.rate,
                "purchase_order": po.name,
                "po_detail": po_item.name
            })
        
        pi.insert(ignore_permissions=True)
        pi.submit()
