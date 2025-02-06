let activeTimerUtility = null;

frappe.ui.form.on('MCQ', {
    refresh(frm) {
        // Add a custom button to open all URLs
        // frm.add_custom_button(__('Open All URLs'), () => {
        //     (frm.doc.urls || []).forEach(row => {
        //         if (row.url) {
        //             window.open(row.url, '_blank');
        //         }
        //     });
        // }, __('Actions'));

        // // Clear existing timer before initializing a new one
        // if (activeTimerUtility) {
        //     activeTimerUtility.clearTimer();
        // }

        // metrack.get_durations(frm).then(() => {
        //     activeTimerUtility = new metrack.TimerUtility(frm);
        //     activeTimerUtility.setupTimer();
        // });
    },

});