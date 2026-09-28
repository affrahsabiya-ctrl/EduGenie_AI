async function postJSON(url, data) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    let result;

    try {
        result = await response.json();
    } catch {
        throw new Error(
            `Server returned HTTP ${response.status}`
        );
    }

    if (!response.ok) {
        throw new Error(
            result.detail ||
            result.error ||
            "Something went wrong."
        );
    }

    return result;
}


function setLoading(element, message = "Thinking...") {
    element.className = "result loading";
    element.textContent = message;
}


function setError(element, message) {
    element.className = "result error";
    element.textContent = message;
}


function setResult(element, content) {
    element.className = "result";
    element.textContent = content;
}


/* =========================
   Q&A
========================= */

async function askQuestion() {

    const input =
        document.getElementById("qa-input");

    const result =
        document.getElementById("qa-result");

    const question =
        input.value.trim();

    if (!question) {
        setError(
            result,
            "Please enter a question."
        );

        return;
    }

    setLoading(
        result,
        "EduGenie is preparing your answer..."
    );

    try {

        const data = await postJSON(
            "/qa",
            {
                question: question
            }
        );

        setResult(
            result,
            data.answer || "No answer returned."
        );

    } catch (error) {

        setError(
            result,
            error.message
        );
    }
}


/* =========================
   Explanation
========================= */

async function explainTopic() {

    const input =
        document.getElementById(
            "explain-input"
        );

    const result =
        document.getElementById(
            "explain-result"
        );

    const topic =
        input.value.trim();

    if (!topic) {

        setError(
            result,
            "Please enter a topic."
        );

        return;
    }

    setLoading(
        result,
        "Creating a simple explanation..."
    );

    try {

        const data = await postJSON(
            "/explain",
            {
                topic: topic
            }
        );

        setResult(
            result,
            data.explanation ||
            "No explanation returned."
        );

    } catch (error) {

        setError(
            result,
            error.message
        );
    }
}


/* =========================
   Quiz
========================= */

async function generateQuiz() {

    const input =
        document.getElementById(
            "quiz-input"
        );

    const result =
        document.getElementById(
            "quiz-result"
        );

    const text =
        input.value.trim();

    if (!text) {

        setError(
            result,
            "Please enter study material."
        );

        return;
    }

    setLoading(
        result,
        "Generating your quiz..."
    );

    try {

        const data = await postJSON(
            "/quiz",
            {
                text: text
            }
        );

        renderQuiz(
            result,
            data
        );

    } catch (error) {

        setError(
            result,
            error.message
        );
    }
}


function renderQuiz(container, quiz) {

    container.className = "result";

    container.innerHTML = "";

    const title =
        document.createElement("h3");

    title.textContent =
        quiz.title ||
        "EduGenie Quiz";

    container.appendChild(title);

    const questions =
        quiz.questions || [];

    if (!questions.length) {

        setError(
            container,
            "No quiz questions were returned."
        );

        return;
    }

    questions.forEach(
        (question, questionIndex) => {

            const questionDiv =
                document.createElement(
                    "div"
                );

            questionDiv.className =
                "quiz-question";

            const heading =
                document.createElement(
                    "h4"
                );

            heading.textContent =
                `${questionIndex + 1}. ${question.question
                }`;

            questionDiv.appendChild(
                heading
            );

            const options =
                question.options || [];

            options.forEach(
                (option, optionIndex) => {

                    const button =
                        document.createElement(
                            "button"
                        );

                    button.className =
                        "quiz-option";

                    button.textContent =
                        option;

                    button.type =
                        "button";

                    button.addEventListener(
                        "click",
                        () => {

                            handleQuizAnswer(
                                questionDiv,
                                button,
                                optionIndex,
                                question.answer,
                                question.explanation
                            );
                        }
                    );

                    questionDiv.appendChild(
                        button
                    );
                }
            );

            container.appendChild(
                questionDiv
            );
        }
    );
}


function handleQuizAnswer(
    questionDiv,
    selectedButton,
    selectedIndex,
    correctIndex,
    explanation
) {

    const buttons =
        questionDiv.querySelectorAll(
            ".quiz-option"
        );

    buttons.forEach(
        (button, index) => {

            button.disabled = true;

            if (index === correctIndex) {
                button.classList.add(
                    "correct"
                );
            }

            if (
                index === selectedIndex &&
                selectedIndex !== correctIndex
            ) {
                button.classList.add(
                    "incorrect"
                );
            }
        }
    );

    const explanationDiv =
        document.createElement(
            "div"
        );

    explanationDiv.className =
        "quiz-explanation";

    const isCorrect =
        selectedIndex === correctIndex;

    explanationDiv.textContent =
        isCorrect
            ? `Correct! ${explanation || ""
            }`
            : `Incorrect. ${explanation || "Review the explanation."
            }`;

    questionDiv.appendChild(
        explanationDiv
    );
}


/* =========================
   Summarization
========================= */

async function summarizeText() {

    const input =
        document.getElementById(
            "summary-input"
        );

    const result =
        document.getElementById(
            "summary-result"
        );

    const text =
        input.value.trim();

    if (!text) {

        setError(
            result,
            "Please enter text to summarize."
        );

        return;
    }

    setLoading(
        result,
        "Creating revision notes..."
    );

    try {

        const data = await postJSON(
            "/summarize",
            {
                text: text
            }
        );

        setResult(
            result,
            data.summary ||
            "No summary returned."
        );

    } catch (error) {

        setError(
            result,
            error.message
        );
    }
}


/* =========================
   Learning Path
========================= */

async function buildLearningPath() {

    const input =
        document.getElementById(
            "learning-input"
        );

    const result =
        document.getElementById(
            "learning-result"
        );

    const subject =
        input.value.trim();

    if (!subject) {

        setError(
            result,
            "Please enter a subject."
        );

        return;
    }

    setLoading(
        result,
        "Building your learning path..."
    );

    try {

        const data = await postJSON(
            "/learn/recommendations",
            {
                text: subject
            }
        );

        setResult(
            result,
            data.recommendations ||
            "No learning path returned."
        );

    } catch (error) {

        setError(
            result,
            error.message
        );
    }
}


/* =========================
   Keyboard shortcuts
========================= */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        const qaInput =
            document.getElementById(
                "qa-input"
            );

        if (qaInput) {

            qaInput.addEventListener(
                "keydown",
                (event) => {

                    if (
                        event.ctrlKey &&
                        event.key === "Enter"
                    ) {
                        askQuestion();
                    }
                }
            );
        }
    }
);