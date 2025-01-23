// Copyright (c) 2024, nishantbhickta and contributors
// For license information, please see license.txt

frappe.ui.form.on("Subjective Question", {
    refresh(frm) {
        // Add a custom button to open all URLs
        frm.add_custom_button(__('Open All URLs'), () => {
            (frm.doc.urls || []).forEach(row => {
                if (row.url) {
                    window.open(row.url, '_blank');
                }
            });
        }, __('Actions'));
        metrack.get_durations(frm).then(() => {
            const timerUtility = new metrack.TimerUtility(
                frm
            );
            timerUtility.setupTimer();
        });
    },
});
