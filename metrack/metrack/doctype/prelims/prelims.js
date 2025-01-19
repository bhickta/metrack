frappe.ui.form.on("Prelims", {
    refresh(frm) {
        const quizManager = new QuizManager(frm);
        quizManager.startQuiz()
    },
});

class QuizManager {
    constructor(frm) {
        this.frm = frm;
        this.items = frm.doc.items;
        this.currentQuestionIndex = 0;
    }

    startQuiz() {
        this.currentQuestionIndex = 0;
        this.fetchAndDisplayQuestion(this.currentQuestionIndex);
    }

    fetchAndDisplayQuestion(questionIndex) {
        const questionName = this.items[questionIndex].question;
        this.fetchQuestionData(questionName, (question) => {
            this.currentQuestionIndex = questionIndex;
            this.renderQuestion(question, questionIndex);
        });
    }

    fetchQuestionData(questionName, callback) {
        frappe.call({
            method: "metrack.metrack.doctype.prelims.prelims.get_question",
            args: { question_name: questionName },
            callback: function (r) {
                if (r.message) {
                    callback(r.message);
                } else {
                    frappe.msgprint("Question not found.");
                }
            },
        });
    }

    renderQuestion(question, questionIndex) {
        const totalQuestions = this.items.length;
        const $container = this.frm.fields_dict.question_container.wrapper;
        $container.innerHTML = this.getQuestionHTML(question, questionIndex, totalQuestions);
        this.attachNavigationListeners(question, questionIndex, totalQuestions);
    }

    getQuestionHTML(question, questionIndex, totalQuestions) {
        return `
            <div>
                <h4>Question ${questionIndex + 1}/${totalQuestions}</h4>
                <p>Question ID: ${question.name} | ${question.subject}</p>
                <p>${question.question}</p>
                <div>
                    <label><input type="radio" name="answer" value="A"> A: ${question.a}</label><br>
                    <label><input type="radio" name="answer" value="B"> B: ${question.b}</label><br>
                    <label><input type="radio" name="answer" value="C"> C: ${question.c}</label><br>
                    <label><input type="radio" name="answer" value="D"> D: ${question.d}</label>
                </div>
                <button class="btn btn-secondary show-explanation-btn">Show Explanation</button>
                <button class="btn btn-secondary prev-btn" ${questionIndex === 0 ? "disabled" : ""}>Previous</button>
                <button class="btn btn-primary next-btn" ${questionIndex === totalQuestions - 1 ? "disabled" : ""}>Next</button>
                <button class="btn btn-success submit-btn">Submit</button>
            </div>
        `;
    }

    attachNavigationListeners(question, questionIndex, totalQuestions) {
        const $wrapper = $(this.frm.fields_dict.question_container.wrapper);

        $wrapper.find(".show-explanation-btn").off("click").on("click", () => {
            this.showExplanation(question);
        });
        $wrapper.find(".prev-btn").off("click").on("click", () => this.navigateQuestion(question, questionIndex - 1));
        $wrapper.find(".next-btn").off("click").on("click", () => this.navigateQuestion(question, questionIndex + 1));
        $wrapper.find(".submit-btn").off("click").on("click", () => this.submitQuestion());
    }

    navigateQuestion(question, newIndex) {
        const selectedAnswer = $("input[name='answer']:checked").val()?.toLowerCase();
        if (selectedAnswer) {
            const currentQuestion = this.items[this.currentQuestionIndex];
            this.updateItemAnswer(currentQuestion, selectedAnswer);
        }
        this.fetchAndDisplayQuestion(newIndex);
    }

    showExplanation(question) {
        frappe.msgprint(question.explanation);
    }

    updateItemAnswer(question, selectedAnswer) {
        question.answer = selectedAnswer;
        this.frm.refresh_field("items");
    }

    submitQuestion() {
        const selectedAnswer = $("input[name='answer']:checked").val()?.toLowerCase();
        if (selectedAnswer) {
            const currentQuestion = this.items[this.currentQuestionIndex];
            this.updateItemAnswer(currentQuestion, selectedAnswer);
        }
        this.updateQuestionCounter();
        this.frm.refresh_field("items");
        this.frm.doc.__unsaved = true;
        this.frm.save_or_update();
    }

    updateQuestionCounter() {
        const answeredItems = this.frm.doc.items.filter(item => item.answer).length;
        const totalQuestions = this.items.length;
        this.frm.fields_dict.question_container.wrapper.innerHTML += `<div>Answered: ${answeredItems}/${totalQuestions}</div>`;
    }
}