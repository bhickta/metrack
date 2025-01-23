frappe.ui.form.on('MCQ', {
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


class MCQ {
    constructor(frm) {
        this.frm = frm;
        this.doc = this.frm.doc;
    }

    run({ state }) {
        this.state = state;
        this.clean();
        this.mark_complete();
        this.navigate();
    }

    navigate() {
        this.frm.navigate_records(1)
    }

    mark_complete() {
        this.frm.add_child('mark', {
            user: frappe.session.user,
            is_done: this.state
        });
    }

    set_custom_buttons() {
        this.frm.add_custom_button(__("Insight Ias"), () => {
            this.frm.call({
                doc: this.frm.doc,
                method: "scrape_insight_ias_quiz"
            })
        }, "Fetch");
    }
    clean() {
        this.clean_question();
        this.clean_options();
        this.frm.refresh();
        this.frm.save();
    }

    clean_question() {
    }

    clean_options() {
        let options_fields = ['a', 'b', 'c', 'd', 'e', 'f'];
        options_fields.forEach(field => {
            this.clean_prefix_options(field);
        });
    }

    clean_prefix_options(field) {
        let value = this.doc[field]?.trim();
        let options_startswith = ["a)", "b)", "c)", "d)", "e)", "f)", "(a)", "(b)", "(c)", "(d)", "(e)", "(f)"];
        options_startswith.forEach(opt => {
            if (value?.startsWith(opt)) {
                value = value.substring(opt.length).trim();
            }
        });
        this.frm.set_value(field, value);
    }
}