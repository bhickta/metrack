frappe.provide("metrack");

metrack.NavigationFilters = class NavigationFilters {
    constructor(frm, quizManager) {
        this.frm = frm;
        this.quizManager = quizManager;
        this.filters = {};
    }
    renderFilters($panelContainer) {
        const $filterContainer = $("<div>").css({
            marginBottom: "15px",
            fontSize: "14px"
        });

        // Filter for attempted questions
        const $attemptedFilter = $("<button>")
            .addClass("btn btn-outline-success filter-btn")
            .text("Attempted")
            .on("click", () => this.filterQuestions("attempted"));

        // Filter for not attempted questions
        const $notAttemptedFilter = $("<button>")
            .addClass("btn btn-outline-danger filter-btn")
            .text("Not Attempted")
            .on("click", () => this.filterQuestions("not_attempted"));

        // Filter for right answers
        const $rightFilter = $("<button>")
            .addClass("btn btn-outline-success filter-btn")
            .text("Right")
            .on("click", () => this.filterQuestions("right"));

        // Filter for wrong answers
        const $wrongFilter = $("<button>")
            .addClass("btn btn-outline-danger filter-btn")
            .text("Wrong")
            .on("click", () => this.filterQuestions("wrong"));

        // Filter for skipped answers
        const $skipFilter = $("<button>")
            .addClass("btn btn-outline-secondary filter-btn")
            .text("Skipped")
            .on("click", () => this.filterQuestions("skip"));

        // Add filters to filter container
        $filterContainer.append($attemptedFilter, $notAttemptedFilter, $rightFilter, $wrongFilter, $skipFilter);
        $panelContainer.prepend($filterContainer);
    }

    filterQuestions(type) {
        if (type === "attempted") {
            this.quizManager.filteredItems = this.quizManager.items.filter(item => item.answer);
        } else if (type === "not_attempted") {
            this.quizManager.filteredItems = this.quizManager.items.filter(item => !item.answer);
        } else if (type === "right") {
            this.quizManager.filteredItems = this.quizManager.items.filter(item => item.check === "Right");
        } else if (type === "wrong") {
            this.quizManager.filteredItems = this.quizManager.items.filter(item => item.check === "Wrong");
        } else if (type === "skip") {
            this.quizManager.filteredItems = this.quizManager.items.filter(item => item.check === "Skip");
        } else {
            this.quizManager.filteredItems = this.quizManager.items;
        }

        // Refresh the navigation panel to reflect the filtered items
        this.quizManager.refreshNavigationPanel();
        this.quizManager.fetchAndDisplayQuestion(0);  // Display the first question of the filtered list
    }
}