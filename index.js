const agents = ["professional", "moderate", "friendly"];
let currentAgentIndex = 0; // Tracks the current agent index
let experimentResults = []; // Stores results from all agents

document
  .getElementById("start-experiment")
  .addEventListener("click", startExperiment);
document
  .getElementById("proceed-to-ratings")
  .addEventListener("click", showRatingsPage);
document
  .getElementById("ratings-form")
  .addEventListener("submit", handleRatingSubmission);

async function startExperiment() {
  document.getElementById("welcome-page").classList.add("hidden");
  document.getElementById("interaction-page").classList.remove("hidden");
  await fetchAgentInteraction(); // Start the first agent's interaction
}

async function fetchAgentInteraction() {
  const agentType = agents[currentAgentIndex];
  document.getElementById(
    "agent-title"
  ).textContent = `${agentType.charAt(0).toUpperCase() + agentType.slice(1)} Agent Interaction`;

  const proceedButton = document.getElementById("proceed-to-ratings");
  proceedButton.disabled = true;

  try {
    const response = await fetch("/bot", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ agent_type: agentType }),
    });

    if (!response.ok) {
      throw new Error("Failed to fetch interaction data.");
    }

    const data = await response.json();
    await displayConversationWithQuestionsOnly(data.questions_and_responses);
    proceedButton.disabled = false; // Enable "Continue" after all questions are asked
  } catch (error) {
    console.error("Error fetching agent interaction:", error);
  }
}

async function displayConversationWithQuestionsOnly(interactions) {
  const conversationDisplay = document.getElementById("conversation-display");
  conversationDisplay.innerHTML = ""; // Clear previous content before adding new questions

  for (const interaction of interactions) {
    const questionElement = document.createElement("p");
    questionElement.innerHTML = `<strong>Q:</strong> ${interaction.question}`;
    conversationDisplay.appendChild(questionElement);
    await new Promise((resolve) => setTimeout(resolve, 1000)); // 1-second delay
  }
}

function showRatingsPage() {
  document.getElementById("interaction-page").classList.add("hidden");
  document.getElementById("ratings-page").classList.remove("hidden");

  const ratingsContainer = document.getElementById("ratings-container");
  const agentType = agents[currentAgentIndex];
  document.getElementById(
    "ratings-agent-title"
  ).textContent = `${agentType.charAt(0).toUpperCase() + agentType.slice(1)} Agent Follow-Up Questionnaire`;

  ratingsContainer.innerHTML = "";

  const followUpQuestions = {
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

  Object.entries(followUpQuestions).forEach(([section, questions]) => {
    const sectionDiv = document.createElement("div");
    sectionDiv.classList.add("likert-container");

    const sectionTitle = document.createElement("h3");
    sectionTitle.textContent = section;
    sectionDiv.appendChild(sectionTitle);

    questions.forEach((text, index) => {
      const questionDiv = document.createElement("div");
      questionDiv.classList.add("likert-container");

      const questionText = document.createElement("p");
      questionText.textContent = text;
      questionDiv.appendChild(questionText);

      const scaleDiv = document.createElement("div");
      scaleDiv.classList.add("likert-scale");

      for (let i = 1; i <= 5; i++) {
        const radio = document.createElement("input");
        radio.type = "radio";
        radio.name = `${section.replace(/\s+/g, "_")}_${index}`;
        radio.value = i;
        radio.required = true;

        const label = document.createElement("label");
        label.textContent = i;
        label.classList.add("likert-number");
        label.appendChild(radio);

        scaleDiv.appendChild(label);
      }

      const scaleLabels = document.createElement("div");
      scaleLabels.classList.add("likert-label-container");
      scaleLabels.innerHTML = `<span class="scale-label left">${text.split("(")[1]?.split(",")[0]}</span>
      <span class="scale-label right">${text.split(",")[1]?.split(")")[0]}</span>`;

      questionDiv.appendChild(scaleDiv);
      questionDiv.appendChild(scaleLabels);

      sectionDiv.appendChild(questionDiv);
    });

    ratingsContainer.appendChild(sectionDiv);
  });
}

async function handleRatingSubmission(event) {
  event.preventDefault();

  const formData = new FormData(event.target);
  const ratings = Object.fromEntries(formData.entries());
  experimentResults.push({
    agent: agents[currentAgentIndex],
    ratings: ratings,
  });

  try {
    const response = await fetch("/next-agent", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });

    if (!response.ok) {
      throw new Error("Failed to transition to next agent.");
    }

    currentAgentIndex++;
    if (currentAgentIndex < agents.length) {
      document.getElementById("ratings-page").classList.add("hidden");
      document.getElementById("interaction-page").classList.remove("hidden");
      await fetchAgentInteraction();
    } else {
      showCompletionPage();
    }
  } catch (error) {
    console.error("Error moving to next agent:", error);
  }
}

function showCompletionPage() {
  document.getElementById("ratings-page").classList.add("hidden");
  document.getElementById("completion-page").classList.remove("hidden");
  console.log("Experiment Results:", experimentResults);
}
