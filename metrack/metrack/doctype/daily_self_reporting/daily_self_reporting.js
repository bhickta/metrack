// Copyright (c) 2025, nishantbhickta and contributors
// For license information, please see license.txt

frappe.ui.form.on("Daily Self Reporting", {

    setup(frm) {
        if(frm.is_new()) {
            frm.doc.items = []
            frm.call("fetch_default_values");
        }
    },

	refresh(frm) {

	},
});
