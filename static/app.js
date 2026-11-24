const form = document.getElementById("topic-form");
const topicInput = document.getElementById("topic");
const runBtn = document.getElementById("run-btn");
const errorBox = document.getElementById("error");
const statusBox = document.getElementById("status");
const pipeline = document.getElementById("pipeline");
const timelineCard = document.getElementById("timeline-card");
const timeline = document.getElementById("timeline");
const resultCard = document.getElementById("result-card");
const badge = document.getElementById("badge");
const meta = document.getElementById("meta");
const finalAnswer = document.getElementById("final-answer");

const LABELS = {
  writer: "✏️ Writer Agent",
  reviewer: "🔍 Reviewer Agent",
  reviser: "🔄 Reviser Agent",
};

function setStage(agent, running = false) {
  pipeline.querySelectorAll("li").forEach((li) => {
    li.classList.remove("active", "running");
    if (li.dataset.agent === agent) {
      li.classList.add("active");
      if (running) li.classList.add("running");
    }
  });
}

function showError(message) {
  errorBox.textContent = message;
  errorBox.hidden = false;
}

function renderEvent(event, index) {
  const step = document.createElement("div");
  step.className = `step ${event.agent}`;

  const head = document.createElement("div");
  head.className = "step-head";
  const title = document.createElement("span");
  title.textContent = `${index + 1}. ${LABELS[event.agent] || event.agent}`;
  const info = document.createElement("small");
  info.textContent = event.agent === "reviewer"
    ? `Decision: ${event.decision}`
    : `Revision ${event.revision_count}`;
  head.append(title, info);
  step.append(head);

  if (event.draft) {
    const body = document.createElement("div");
    body.className = "body";
    body.textContent = event.draft;
    step.append(body);
  }
  if (event.feedback) {
    const fb = document.createElement("div");
    fb.className = "feedback";
    fb.textContent = `Feedback: ${event.feedback}`;
    step.append(fb);
  }
  return step;
}

function renderResult(data) {
  timeline.replaceChildren(...data.events.map(renderEvent));
  timelineCard.hidden = false;

  const passed = data.final_decision === "PASS";
  badge.textContent = passed ? "PASS" : "Max revisions reached";
  badge.className = `badge ${passed ? "pass" : "revise"}`;
  meta.textContent =
    `Revisions: ${data.final_revision_count} · ${data.provider} · ${data.model}`;
  finalAnswer.textContent = data.final_answer;
  resultCard.hidden = false;

  setStage("done");
  statusBox.textContent = passed
    ? "Reviewer approved the answer."
    : "Stopped: maximum revisions limit reached.";
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const topic = topicInput.value.trim();
  if (!topic) return;

  errorBox.hidden = true;
  timelineCard.hidden = true;
  resultCard.hidden = true;
  runBtn.disabled = true;
  runBtn.textContent = "Running…";
  setStage("writer", true);
  statusBox.textContent = "Writer, Reviewer and Reviser agents are working…";

  try {
    const response = await fetch("/api/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Request failed.");
    }
    renderResult(data);
  } catch (err) {
    setStage(null);
    statusBox.textContent = "Workflow failed.";
    showError(err.message);
  } finally {
    runBtn.disabled = false;
    runBtn.textContent = "Run workflow";
  }
});
