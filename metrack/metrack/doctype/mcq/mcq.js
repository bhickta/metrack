// Copyright (c) 2024, nishantbhickta and contributors
// For license information, please see license.txt

frappe.ui.form.on('MCQ', {
    refresh(frm) {
        frm.add_custom_button(__('Open All URLs'), () => {
            (frm.doc.urls || []).forEach(row => {
                if (row.url) {
                    window.open(row.url, '_blank');
                }
            });
        }, __('Actions'));

        let timerDuration = 180;
        let timerElement = frm.dashboard.add_section(`<div id="mcq-timer" style="font-weight: bold; color: red;">Time left: ${formatTime(timerDuration)}</div>`);

        const timerInterval = setInterval(() => {
            timerDuration--;
            const timerDisplay = document.getElementById('mcq-timer');
            if (timerDisplay) {
                timerDisplay.textContent = `Time left: ${formatTime(timerDuration)}`;
            }

            if (timerDuration <= 0) {
                clearInterval(timerInterval);
                triggerNextQuestion(frm);
            }
        }, 1000);

        frm.add_custom_button(
            __('Next'),
            () => {
                triggerNextQuestion(frm);
            },
            __('Actions')
        ).addClass('btn-primary');
    }
});

function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

function triggerNextQuestion(frm) {
    frappe.confirm(
        __('Are you sure you want to move to the next question?'),
        () => {
            const nextDocButton = $('.next-doc');
            nextDocButton.click();
        },
        () => {
            // If the user clicks "No", reset the timer to 60 seconds
            resetTimer(frm);
        }
    );
}

function resetTimer(frm) {
    let timerDuration = 60;
    const timerDisplay = document.getElementById('mcq-timer');
    if (timerDisplay) {
        timerDisplay.textContent = `Time left: ${formatTime(timerDuration)}`;
    }

    const timerInterval = setInterval(() => {
        timerDuration--;
        if (timerDisplay) {
            timerDisplay.textContent = `Time left: ${formatTime(timerDuration)}`;
        }

        if (timerDuration <= 0) {
            clearInterval(timerInterval);
            triggerNextQuestion(frm);
        }
    }, 1000);
}



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