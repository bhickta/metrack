metrack.TimerUtility = class TimerUtility {
    constructor(frm) {
        this.frm = frm;
        this.duration = frm.initial;
        this.increment = frm.increment;
        this.target = frm.target;
        this.done_today = this.frm.doc.__onload?.done_today
        this.timerInterval = null;
    }

    setupTimer() {
        // Clear any existing timer interval
        this.clearTimer();

        // Clear any existing timer section
        this.clearTimerSection();

        this.frm.dashboard.clear_headline();
        this.frm.dashboard.add_section(this.getTimerHTML());

        // Start the timer
        this.startTimer();
    }

    startTimer() {
        this.timerInterval = setInterval(() => {
            this.duration--;
            this.updateTimerDisplay();

            if (this.duration <= 0) {
                this.clearTimer();
                this.triggerNextQuestion();
            }
        }, 1000);
    }

    clearTimer() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
    }

    clearTimerSection() {
        const oldTimerSection = document.getElementById('question-timer');
        if (oldTimerSection) {
            oldTimerSection.parentElement.remove();
        }
    }

    updateTimerDisplay() {
        const timerDisplay = document.getElementById('question-timer');
        if (timerDisplay) {
            timerDisplay.textContent = `Time left: ${this.formatTime(this.duration)}`;
        }
    }

    getTimerHTML() {
        return `
            <div style="display: flex; justify-content: space-between; align-items: center; font-weight: bold; color: red;">
                <div id="question-timer">Time left: ${this.formatTime(this.duration)}</div>
                <div>${__('Target')} ${this.target || 0} | Done: ${this.done_today || 0} | Left: ${this.target - this.done_today}</div>
            </div>
        `;
    }

    formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    }

    resetTimer() {
        this.duration += this.increment;
        this.setupTimer();
    }

    triggerNextQuestion() {
        frappe.confirm(
            __('Are you sure you want to move to the next question?'),
            () => {
                const nextDocButton = document.querySelector('.next-doc');
                if (nextDocButton) {
                    nextDocButton.click();
                } else {
                    frappe.msgprint(__('Next document button not found.'));
                }
            },
            () => {
                this.resetTimer();
            }
        );
    }
}

metrack.get_durations = async function (frm) {
    try {
        const response = await frappe.call({
            method: 'frappe.client.get',
            args: {
                doctype: 'Metrack Settings',
                name: 'Metrack Settings',
            },
        });

        if (response.message) {
            const settings = response.message;

            // Filter timers for the current doctype
            let timer = settings.timers.find((x) => x.doc === frm.doc.doctype);

            if (!timer) {
                console.log('No timer found for the current doctype.');
                return;
            }

            if (timer.is_disabled) {
                console.log('Timer is disabled.');
                return;
            }

            // Assign timer properties to the form
            frm.initial = timer.initial;
            frm.incremental = timer.incremental;
            frm.target = timer.target;
        }
    } catch (error) {
        console.error('Error fetching durations:', error);
    }
};