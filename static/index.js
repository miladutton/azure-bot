const agents = ["professional", "moderate", "friendly"];
let experimentResults = []; // Stores results from all agents

// Event listeners
document.getElementById("start-experiment").addEventListener("click", startExperiment);
console.log("Event listener for Begin Experiment button attached"); // Debug log

document.getElementById("proceed-to-ratings").addEventListener("click", showRatingsPage);
document.getElementById("ratings-form").addEventListener("submit", handleRatingSubmission);

async function startExperiment() {
    console.log("Begin Experiment button clicked"); // Debug log

    document.getElementById("welcome-page").classList.add("hidden");
    document.getElementById("interaction-page").classList.remove("hidden");

    // Set the default title for all agents
    document.getElementById("agent-title").textContent = "Agent Interaction";

    await fetchAgentInteraction();
}

async function fetchAgentInteraction() {
    const proceedButton = document.getElementById("proceed-to-ratings");
    proceedButton.disabled = true; // Disable the button initially

    try {
        const response = await fetch("/bot", {
            method: "POST",
            headers: { "Content-Type": "application/json" }
        });

        if (!response.ok) throw new Error("Failed to fetch interaction data.");

        const data = await response.json();

        // Set the title for all agents
        document.getElementById("agent-title").textContent = "Agent Interaction";

        // Update the conversation display
        const conversationDisplay = document.getElementById("conversation-display");
        conversationDisplay.innerHTML = `<p>${data.message}</p>`;

        // Immediately enable the "Continue" button
        proceedButton.disabled = false;
    } catch (error) {
        console.error("Error fetching agent interaction:", error);
    }
}

function showRatingsPage() {
    document.getElementById("interaction-page").classList.add("hidden");
    document.getElementById("ratings-page").classList.remove("hidden");
    populateRatingsForm();
}

function populateRatingsForm() {
    const container = document.getElementById("ratings-container");
    container.innerHTML = ""; // Clear previous content

    const follow_up_questions = {
        "Engagement and Approachability": [
            "How easy or difficult was it to engage in conversation with this agent? (1 = Very Difficult, 5 = Very Easy)",
            "Did this agent feel friendly and approachable to you? (1 = Strongly Disagree, 5 = Strongly Agree)",
            "How would you rate this agent’s engagement level and friendliness? (1 = Very Low, 5 = Very High)"
        ],
        "Communication Style": [
            "How natural did the conversation feel with this agent overall? (1 = Not Natural, 5 = Very Natural)",
            "Did the agent’s tone or language make you feel comfortable sharing your thoughts? (1 = Strongly Disagree, 5 = Strongly Agree)",
            "Did the timing and pauses in the conversation feel natural, or were they distracting? (1 = Very Distracting, 5 = Very Natural)"
        ],
        "Emotional Connection": [
            "Did you feel this agent was genuinely interested in what you had to say? (1 = Strongly Disagree, 5 = Strongly Agree)",
            "How much did this agent make you feel emotionally connected during the conversation? (1 = Not at all, 5 = Very Much)",
            "Did the agent seem empathetic or understanding toward your responses? (1 = Strongly Disagree, 5 = Strongly Agree)"
        ],
        "Personality": [
            "How would you describe the agent’s tone—did it add to or take away from the experience? (1 = Took Away, 5 = Added a Lot)",
            "Do you think the agent’s personality influenced your experience positively? (1 = Strongly Disagree, 5 = Strongly Agree)",
            "How natural or fitting was the agent's tone and style of humor in this conversation? (1 = Very Inappropriate, 5 = Very Appropriate)"
        ]
    };

    for (const category in follow_up_questions) {
        const categoryHeading = document.createElement("h3");
        categoryHeading.textContent = category;
        container.appendChild(categoryHeading);

        follow_up_questions[category].forEach((question, index) => {
            const questionDiv = document.createElement("div");
            questionDiv.className = "likert-container";

            const questionLabel = document.createElement("p");
            questionLabel.textContent = question;
            questionDiv.appendChild(questionLabel);

            const likertScale = document.createElement("div");
            likertScale.className = "likert-scale";

            // Create a scale of 1 to 5
            for (let i = 1; i <= 5; i++) {
                const label = document.createElement("label");

                const radio = document.createElement("input");
                radio.type = "radio";
                radio.name = `${category}-${index}`;
                radio.value = i;
                radio.required = true;

                const number = document.createElement("span");
                number.textContent = i;

                label.appendChild(radio);
                label.appendChild(number);
                likertScale.appendChild(label);
            }

            questionDiv.appendChild(likertScale);
            container.appendChild(questionDiv);
        });
    }
}

async function handleRatingSubmission(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const ratings = Object.fromEntries(formData.entries());
    experimentResults.push(ratings);

    try {
        const response = await fetch("/submit-follow-up", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(ratings)
        });

        const data = await response.json();

        if (data.message.includes("next agent")) {
            document.getElementById("ratings-page").classList.add("hidden");
            document.getElementById("interaction-page").classList.remove("hidden");
            await fetchAgentInteraction();
        } else {
            document.getElementById("ratings-page").classList.add("hidden");
            document.getElementById("completion-page").classList.remove("hidden");

            // Generic completion text
            const completionPage = document.getElementById("completion-page");
            completionPage.innerHTML = `
                <h1>Experiment Complete</h1>
                <p>Thank you for participating!</p>
            `;
        }
    } catch (error) {
        console.error("Error submitting follow-up responses:", error);
    }
}
