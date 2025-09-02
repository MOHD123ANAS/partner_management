import frappe
from frappe.utils import get_url

def notify_supplier_on_draft(doc, method):

    try:
        if doc.docstatus != 0: 
            return

        for item in doc.items:
            if not item.supplier:
                continue


            supplier_addresses = frappe.db.sql("""
                SELECT a.email_id
                FROM `tabAddress` a
                INNER JOIN `tabDynamic Link` dl ON dl.parent = a.name
                WHERE dl.link_doctype = 'Supplier'
                  AND dl.link_name = %s
                  AND a.email_id IS NOT NULL
            """, (item.supplier,), as_dict=True)

            if not supplier_addresses:
                continue

            
            emails = [row.email_id for row in supplier_addresses if row.email_id]

            if not emails:
                continue

            
            so_link = get_url(f"/app/sales-order/{doc.name}")

            
            subject = f"New Draft Sales Order {doc.name} Assigned to You"
            message = f"""
            <p>Dear Partner,</p>
            <p>You have received a new <b>Draft Sales Order</b>: <b>{doc.name}</b>.</p>
            <p><b>Item:</b> {item.item_name}</p>
            <p>Please review the Sales Order and let us know if you accept it:</p>
            <p>
                <a href="{so_link}" style="padding:10px 20px;background:#4CAF50;color:white;text-decoration:none;border-radius:5px;">
                    Accept Order
                </a>
                &nbsp;
                <a href="{so_link}" style="padding:10px 20px;background:#f44336;color:white;text-decoration:none;border-radius:5px;">
                    Reject Order
                </a>
            </p>
            <p>We would appreciate your prompt response.</p>
            """

           
            frappe.sendmail(
                recipients=emails,
                subject=subject,
                message=message
            )

    except Exception as e:
        frappe.log_error(f"Error in notify_supplier_on_draft: {str(e)}", "Sales Order Notification")
