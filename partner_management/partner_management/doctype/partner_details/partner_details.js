// Copyright (c) 2025, winspire tech  and contributors
// For license information, please see license.txt

frappe.ui.form.on("Partner Details", {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('Create Supplier'), function() {
                frappe.call({
                    method: "partner_management.customization.partner_details.create_supplier",
                    args: {
                        partner_details_name: frm.doc.name  // pass the DocType ID
                    },
                    callback: function(r) {
                        if (!r.exc) {
                            
                            frappe.msgprint({
                                title: __('Success'),
                                indicator: 'green',
                                message: 'Supplier Created: ' + r.message
                            });
                            
                            frappe.set_route("Form", "Supplier", r.message);
                        }
                    }
                });
            }, __("Actions"));
        }
    }
});
