frappe.ui.form.on("Prelims", {
    refresh(frm) {
        const quizManager = new metrack.QuizManager(frm);
        quizManager.startQuiz();
    },
});