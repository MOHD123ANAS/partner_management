// Copyright (c) 2025, winspire tech and contributors
// For license information, please see license.txt

frappe.ui.form.on("Partner Items", {
    refresh: function(frm) {
        if (frm.doc.docstatus === 1 && frm.doc.status === "Pending") {
            
            frm.add_custom_button(__('Approve'), function() {
                frappe.call({
                    method: "partner_management.partner_management.doctype.partner_items.partner_items.approve_item",
                    args: { docname: frm.doc.name },
                    callback: function(r) {
                        if (!r.exc) {
                            frappe.msgprint(r.message);
                            frm.reload_doc();
                        }
                    }
                });
            }, __("Actions"));

            frm.add_custom_button(__('Reject'), function() {
                frappe.prompt(
                    [
                        {
                            fieldname: "reason",
                            label: "Rejection Reason",
                            fieldtype: "Small Text",
                            reqd: 1
                        }
                    ],
                    function(values) {
                        frappe.call({
                            method: "partner_management.partner_management.doctype.partner_items.partner_items.reject_item",
                            args: { 
                                docname: frm.doc.name,
                                reason: values.reason
                            },
                            callback: function(r) {
                                if (!r.exc) {
                                    frappe.msgprint(r.message);
                                    frm.reload_doc();
                                }
                            }
                        });
                    },
                    __("Reject Item"),
                    __("Reject")
                );
            }, __("Actions"));
            
        }
    }
});

