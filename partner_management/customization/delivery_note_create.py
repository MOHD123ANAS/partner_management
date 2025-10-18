import frappe

def create_delivery_note_from_sales_invoice(doc, method=None):
    pass
# @frappe.whitelist()
# def create_delivery_note_from_sales_invoice(doc, method=None):
#     # doc can be a string (name) or actual doc
#     if isinstance(doc, str):
#         si = frappe.get_doc("Sales Invoice", doc)
#     else:
#         si = doc

#     if si.docstatus != 1:
#         frappe.throw(f"Sales Invoice {si.name} must be submitted to create Delivery Note")

#     dn = frappe.new_doc("Delivery Note")
#     dn.customer = si.customer
#     dn.company = si.company
#     dn.posting_date = si.posting_date
#     dn.posting_time = si.posting_time
#     dn.currency = si.currency

#     for si_item in si.items:
#         dn.append("items", {
#             "item_code": si_item.item_code,
#             "item_name": si_item.item_name,
#             "qty": si_item.qty,
#             "stock_uom": si_item.stock_uom,
#             "uom": si_item.uom,
#             "conversion_factor": si_item.conversion_factor,
#             "warehouse": si_item.warehouse,
#             "rate": si_item.rate,
#             "amount": si_item.amount,
#             "against_sales_invoice": si.name,
#             "against_sales_invoice_item": si_item.name,
#             "against_sales_order": si_item.sales_order or None,
#             # "against_sales_order_item": si_item.so_detail or None
#         })

#     dn.insert()
#     dn.submit()

#     return dn.name
