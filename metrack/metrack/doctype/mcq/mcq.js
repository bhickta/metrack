let activeTimerUtility = null;

frappe.ui.form.on('MCQ', {
    refresh(frm) {
        frm.events.add_custom_buttons(frm);
        frm.events.is_timer(frm);
    },

    async is_timer(frm) {
        const r = await frm.call({
            method: 'metrack.metrack.doctype.doctype_timer.doctype_timer.is_timer',
            args: { doc: frm.doc.doctype },
        });
        const is_timer = r.message;
        if (is_timer) {
            frm.events.add_timer(frm);
        }
    },

    add_timer(frm) {
        if (activeTimerUtility) {
            activeTimerUtility.clearTimer();
        }

        metrack.get_durations(frm).then(() => {
            activeTimerUtility = new metrack.TimerUtility(frm);
            activeTimerUtility.setupTimer();
        });
    },

    add_custom_buttons(frm) {
        frm.add_custom_button(__('Open All URLs'), () => {
            (frm.doc.urls || []).forEach(row => {
                if (row.url) {
                    window.open(row.url, '_blank');
                }
            });
        }, __('Actions'));
    },
});