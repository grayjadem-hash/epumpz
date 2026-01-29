const personalityForm = document.getElementById("personalityForm");
const automationStatus = document.getElementById("automationStatus");
const automationHint = document.getElementById("automationHint");
const timeline = document.getElementById("timeline");
const sendOnceButton = document.getElementById("sendOnce");
const startAutomationButton = document.getElementById("startAutomation");
const stopAutomationButton = document.getElementById("stopAutomation");

const recipientList = document.getElementById("recipientList");
const messagePurpose = document.getElementById("messagePurpose");
const startTime = document.getElementById("startTime");
const interval = document.getElementById("interval");

const defaults = {
  personaName: "Alex the Optimist",
  tone: "Warm & supportive",
  mission: "Help people stay consistent and encouraged throughout their day.",
  phrases: "You've got this,Let's make today count,Small steps matter",
  style: "Gentle nudges",
};

let automationTimer = null;
let personality = { ...defaults };

function hydrateForm() {
  const saved = JSON.parse(localStorage.getItem("pulseTextPersonality"));
  personality = saved || defaults;

  Object.entries(personality).forEach(([key, value]) => {
    const field = personalityForm.elements[key];
    if (field) {
      field.value = value;
    }
  });
}

function updateStatus(state, hint) {
  automationStatus.textContent = state;
  automationHint.textContent = hint;
}

function formatTime(timestamp = new Date()) {
  return timestamp.toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
}

function buildMessage() {
  const phrases = personality.phrases
    .split(",")
    .map((phrase) => phrase.trim())
    .filter(Boolean);
  const phrase = phrases[Math.floor(Math.random() * phrases.length)] || "You've got this";
  const purpose = messagePurpose.value.trim() || "a friendly reminder";

  return `${personality.personaName} here! ${phrase}. ${personality.style} on ${purpose}.`;
}

function addTimelineEntry({ message, recipients, status }) {
  const item = document.createElement("li");
  item.className = "timeline-card";

  item.innerHTML = `
    <div class="timeline-header">
      <span>${formatTime()}</span>
      <span class="badge">${status}</span>
    </div>
    <p class="timeline-message">${message}</p>
    <p class="timeline-header">To: ${recipients || "No recipients set"}</p>
  `;

  timeline.prepend(item);
}

function handleSend(status = "Sent") {
  const recipients = recipientList.value.trim();
  const message = buildMessage();

  addTimelineEntry({
    message,
    recipients,
    status,
  });
}

personalityForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const formData = new FormData(personalityForm);
  personality = Object.fromEntries(formData.entries());
  localStorage.setItem("pulseTextPersonality", JSON.stringify(personality));
  updateStatus("Personality saved", "Ready to automate your text flow.");
});

sendOnceButton.addEventListener("click", () => {
  handleSend("Test text");
});

startAutomationButton.addEventListener("click", () => {
  const intervalMinutes = Number.parseInt(interval.value, 10) || 30;
  const startValue = startTime.value;

  if (automationTimer) {
    clearInterval(automationTimer);
  }

  updateStatus("Running", `Auto texting every ${intervalMinutes} minutes.`);
  stopAutomationButton.disabled = false;

  if (startValue) {
    const [hour, minute] = startValue.split(":").map(Number);
    const now = new Date();
    const firstRun = new Date();
    firstRun.setHours(hour, minute, 0, 0);
    if (firstRun < now) {
      firstRun.setDate(firstRun.getDate() + 1);
    }
    const delay = firstRun.getTime() - now.getTime();

    updateStatus(
      "Scheduled",
      `First text at ${startValue}, then every ${intervalMinutes} minutes.`
    );

    setTimeout(() => {
      handleSend("Auto text");
      automationTimer = setInterval(() => handleSend("Auto text"), intervalMinutes * 60000);
    }, delay);
  } else {
    handleSend("Auto text");
    automationTimer = setInterval(() => handleSend("Auto text"), intervalMinutes * 60000);
  }
});

stopAutomationButton.addEventListener("click", () => {
  if (automationTimer) {
    clearInterval(automationTimer);
    automationTimer = null;
  }
  updateStatus("Stopped", "Automation paused. Ready when you are.");
  stopAutomationButton.disabled = true;
});

hydrateForm();
updateStatus("Idle", "Build a personality and start your auto-text routine.");
