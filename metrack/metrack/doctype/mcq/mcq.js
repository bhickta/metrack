// Copyright (c) 2024, nishantbhickta and contributors
// For license information, please see license.txt

frappe.ui.form.on("MCQ", {
    // question_status(frm) {
    //     console.log("hte")
    //     let cleanmcq = new MCQ(frm);
    //     let state;
    //     if (frm.doc.workflow_state == "Done") {
    //         state = 'done';
    //     } else {
    //         state = 'not-done';
    //     }
    //     cleanmcq.run({ state });
    // },

    refresh(frm) {
        // let mcq = new MCQ(frm);
        // mcq.set_custom_buttons()
    }
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