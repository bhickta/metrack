frappe.provide("metrack");

metrack.NavigationPanel = class NavigationPanel {
    constructor(quizManager) {
        this.quizManager = quizManager;
        this.panelContainer = null;
    }

    render() {
        this.panelContainer = this.createNavigationPanelContainer();

        this.quizManager.filteredItems.forEach((item, index) => {
            const $btn = this.createNavigationButton(item, index);
            this.panelContainer.append($btn);
        });

        $("body").append(this.panelContainer);
        this.quizManager.navigationFilters.renderFilters(this.panelContainer);
    }

    createNavigationPanelContainer() {
        return $("<div>").addClass("quiz-navigation-panel").css({
            position: "fixed",
            right: "20px",       
            top: "50px",         
            width: "180px",      
            padding: "10px",
            background: "#f8f9fa",
            border: "1px solid #ccc",
            borderRadius: "5px",
            boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
            zIndex: 999,
            maxHeight: "calc(100vh - 100px)",
            overflowY: "auto"
        });
    }

    createNavigationButton(item, index) {
        const $btn = $("<button>")
            .addClass("btn question-nav-btn")
            .text(`Q${index + 1}`)
            .data("index", index)
            .css({
                width: "100%",
                marginBottom: "5px",
                textAlign: "left",
                padding: "8px",
                fontSize: "14px",
                backgroundColor: item.answer ? "green" : "blue",  // Color code based on 'answer'
                color: "white",
                border: "none",
                borderRadius: "5px",
            })
            .on("click", () => this.quizManager.navigateQuestion(item, index));

        return $btn;
    }

    refresh() {
        $(".quiz-navigation-panel").remove();  // Remove old panel
        this.render();  // Re-render the panel with filtered items
    }
}