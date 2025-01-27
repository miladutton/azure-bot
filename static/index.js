const agents = [
    { 
        type: "professional", 
        style: { rate: 0.9, pitch: 1.0 }
    },
    { 
        type: "moderate", 
        style: { rate: 1.0, pitch: 1.02 }
    },
    { 
        type: "friendly", 
        style: { rate: 1.2, pitch: 1.05 }
    }
];

let currentAgentIndex = 0;
let currentQuestionIndex = 0;
let experimentResults = [];
let synth = window.speechSynthesis;
let recognition = null;

if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
}

// Event listeners
document.getElementById("start-experiment").addEventListener("click", startExperiment);
document.getElementById("proceed-to-ratings").addEventListener("click", showRatingsPage);
document.getElementById("ratings-form").addEventListener("submit", handleRatingSubmission);

async function startExperiment() {
    console.log("Starting experiment with agent:", agents[currentAgentIndex].type);
    document.getElementById("welcome-page").classList.add("hidden");
    document.getElementById("interaction-page").classList.remove("hidden");
    document.getElementById("agent-title").textContent = `${capitalizeFirstLetter(agents[currentAgentIndex].type)} Agent`;
    await runAgentInteraction();
}

async function runAgentInteraction() {
    const proceedButton = document.getElementById("proceed-to-ratings");
    proceedButton.disabled = true;
    const conversationDisplay = document.getElementById("conversation-display");
    
    try {
        // Fetch questions from server
        const response = await fetch("/bot", {
            method: "POST",
            headers: { "Content-Type": "application/json" }
        });

        if (!response.ok) throw new Error("Failed to fetch interaction data.");
        const data = await response.json();
        
        // Speak welcome message
        await speakText(
            `Hello, I'm the ${agents[currentAgentIndex].type} agent. I'll be asking you a few questions.`,
            agents[currentAgentIndex].style
        );

        // Ask each question and wait for response
        for (const question of data.questions) {
            // Display and speak the question
            const questionElement = document.createElement("p");
            questionElement.className = "agent-message";
            questionElement.textContent = `Agent: ${question}`;
            conversationDisplay.appendChild(questionElement);
            
            await speakText(question, agents[currentAgentIndex].style);
            
            // Get user's response
            const response = await getUserResponse();
            
            // Display user's response
            const responseElement = document.createElement("p");
            responseElement.className = "user-message";
            responseElement.textContent = `You: ${response}`;
            conversationDisplay.appendChild(responseElement);
        }

        // Speak thank you message
        await speakText(
            `Thank you for your responses. Let's move on to the follow-up questions.`,
            agents[currentAgentIndex].style
        );

        proceedButton.disabled = false;
        
    } catch (error) {
        console.error("Error in agent interaction:", error);
        conversationDisplay.innerHTML += `<p class="error">An error occurred. Please try again.</p>`;
    }
}

function speakText(text, style) {
    return new Promise((resolve) => {
        // Cancel any ongoing speech
        synth.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = style.rate;
        utterance.pitch = style.pitch;
        
        utterance.onend = () => {
            resolve();
        };

        synth.speak(utterance);
    });
}

function getUserResponse() {
    return new Promise((resolve) => {
        if (recognition) {
            recognition.onresult = (event) => {
                const response = event.results[0][0].transcript;
                resolve(response);
            };
            
            recognition.onerror = () => {
                resolve("No response recorded");
            };
            
            recognition.start();
        } else {
            // Simulate response for testing
            setTimeout(() => {
                resolve("Simulated user response");
            }, 2000);
        }
    });
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
    experimentResults.push({
        agentType: agents[currentAgentIndex].type,
        ratings: ratings
    });

    try {
        const response = await fetch("/submit-follow-up", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                agentType: agents[currentAgentIndex].type,
                ratings: ratings
            })
        });

        const data = await response.json();
        
        // Move to next agent or complete experiment
        currentAgentIndex++;
        if (currentAgentIndex < agents.length) {
            // Reset conversation display for next agent
            document.getElementById("conversation-display").innerHTML = "";
            document.getElementById("ratings-page").classList.add("hidden");
            document.getElementById("interaction-page").classList.remove("hidden");
            document.getElementById("agent-title").textContent = 
                `${capitalizeFirstLetter(agents[currentAgentIndex].type)} Agent`;
            await runAgentInteraction();
        } else {
            // Show completion page
            document.getElementById("ratings-page").classList.add("hidden");
            document.getElementById("completion-page").classList.remove("hidden");
        }
    } catch (error) {
        console.error("Error submitting ratings:", error);
    }
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}