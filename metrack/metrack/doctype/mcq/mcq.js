// Global variable to store the timer interval
let globalTimerInterval;
let timerDuration = 0;

frappe.ui.form.on('MCQ', {
    async get_durations(frm) {
        frm.per_mcq_interval = await frappe.db.get_single_value('Metrack Settings', 'per_mcq_interval');
        frm.per_mcq_interval_increment = await frappe.db.get_single_value('Metrack Settings', 'per_mcq_interval_increment');
    },

    refresh(frm) {
        frm.add_custom_button(__('Open All URLs'), () => {
            (frm.doc.urls || []).forEach(row => {
                if (row.url) {
                    window.open(row.url, '_blank');
                }
            });
        }, __('Actions'));

        frm.events.get_durations(frm).then(() => {
            timerDuration = frm.per_mcq_interval;
            setupTimer(frm, timerDuration);
        });

    }
});

function setupTimer(frm, duration) {
    // Clear any existing timer interval
    if (globalTimerInterval) {
        clearInterval(globalTimerInterval);
    }

    // Clear any existing timer section
    const oldTimerSection = document.getElementById('mcq-timer');
    if (oldTimerSection) {
        oldTimerSection.parentElement.remove(); // Remove the parent element that contains the section
    }

    timerDuration = duration;

    // Add new timer section
    frm.dashboard.clear_headline();
    frm.dashboard.add_section(`
        <div style="display: flex; justify-content: space-between; align-items: center; font-weight: bold; color: red;">
            <div id="mcq-timer">Time left: ${formatTime(timerDuration)}</div>
            <div>${__('MCQ Done Today')} ${frm.doc.__onload.mcq_done}</div>
        </div>
    `);   

    // Set up the interval to update the timer
    globalTimerInterval = setInterval(() => {
        timerDuration--;
        const timerDisplay = document.getElementById('mcq-timer');
        if (timerDisplay) {
            timerDisplay.textContent = `Time left: ${formatTime(timerDuration)}`;
        }

        if (timerDuration <= 0) {
            clearInterval(globalTimerInterval);
            triggerNextQuestion(frm);
        }
    }, 1000);
}

function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

function triggerNextQuestion(frm) {
    frappe.confirm(
        __('Are you sure you want to move to the next question?'),
        () => {
            // Simulate clicking the next document button if available
            const nextDocButton = document.querySelector('.next-doc');
            if (nextDocButton) {
                nextDocButton.click();
            } else {
                frappe.msgprint(__('Next document button not found.'));
            }
        },
        () => {
            // Reset the timer with an increment if user cancels
            resetTimer(frm, frm.per_mcq_interval_increment);
        }
    );
}

function resetTimer(frm, increment) {
    const newDuration = timerDuration + increment;
    setupTimer(frm, newDuration);
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