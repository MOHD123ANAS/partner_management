import frappe
from frappe.utils import nowdate

@frappe.whitelist()
def create_po_and_pi_for_supplier(doc, method):
    supplier_items = {}

    
    for item in doc.items:
        if item.delivered_by_supplier and item.supplier:
            supplier_items.setdefault(item.supplier, []).append(item)

    for supplier, items in supplier_items.items():

        
        supplier_doc = frappe.get_doc("Supplier", supplier)
        price_list = supplier_doc.default_price_list

        
        if not price_list:
            frappe.throw(f"Supplier {supplier} does not have a Default Buying Price List set in Supplier Master.")

        
        po = frappe.get_doc({
            "doctype": "Purchase Order",
            "supplier": supplier,
            "transaction_date": nowdate(),
            "schedule_date": nowdate(),
            "buying_price_list": price_list,
            "items": []
        })

        for so_item in items:
            
            rate = frappe.db.get_value(
                "Item Price",
                {
                    "item_code": so_item.item_code,
                    "price_list": price_list
                },
                "price_list_rate"
            )

            
            if rate is None:
                frappe.throw(
                    f"No rate found for Item {so_item.item_code} "
                    f"in Price List {price_list} (Supplier: {supplier})."
                )

            po.append("items", {
                "item_code": so_item.item_code,
                "qty": so_item.qty,
                "rate": rate,
                "sales_order": doc.name,
                "so_detail": so_item.name
            })

        po.insert(ignore_permissions=True)
        po.submit()

        
        pi = frappe.get_doc({
            "doctype": "Purchase Invoice",
            "supplier": supplier,
            "posting_date": nowdate(),
            "buying_price_list": price_list,
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
