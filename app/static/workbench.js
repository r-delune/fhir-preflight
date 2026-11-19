"use strict";
function setPipelineStage(name) {
  document.querySelectorAll("[data-pipeline-stage]").forEach((stage) => {
    const active = stage.dataset.pipelineStage === name;
    stage.classList.toggle("current", active);
    if (active) stage.setAttribute("aria-current", "step");
    else stage.removeAttribute("aria-current");
  });
}
const cards = document.querySelectorAll(".issue-card");
cards.forEach((card) => {
  card.addEventListener("click", () => {
    cards.forEach((other) => other.setAttribute("aria-pressed", String(other === card)));
    document.querySelectorAll(".highlighted").forEach((line) => line.classList.remove("highlighted"));
    const start = Number(card.dataset.start);
    const end = Number(card.dataset.end);
    for (let n = start; n > 0 && n <= end; n++) {
      document.getElementById(`line-${n}`)?.classList.add("highlighted");
    }
    const line = document.getElementById(`line-${start}`);
    const viewer = document.getElementById("json-view");
    if (line && viewer) viewer.scrollTo({top: line.offsetTop - viewer.offsetTop - 40, behavior: "smooth"});
    document.getElementById("selected-id").textContent = card.dataset.issueId;
    document.getElementById("selected-message").textContent = card.dataset.message;
    document.getElementById("location-note").textContent = card.dataset.note;
    document.getElementById("selection-detail").hidden = false;
    document.getElementById("review-placeholder").hidden = true;
  });
});
document.getElementById("validation-form")?.addEventListener("submit", () => {
  setPipelineStage("validator");
  document.getElementById("validate-button").disabled = true;
  document.getElementById("validate-label").textContent = "Validating…";
  document.getElementById("busy-message").hidden = false;
  document.getElementById("validation-form").setAttribute("aria-busy", "true");
});
document.getElementById("fixture")?.addEventListener("change", (event) => {
  document.getElementById("validate-button").disabled = true;
  document.getElementById("validate-label").textContent = "Loading example…";
  event.target.form.requestSubmit();
});
// A page restored from the browser's back/forward cache must be runnable again.
window.addEventListener("pageshow", () => {
  const originalStage = document.getElementById("pipeline")?.dataset.currentStage;
  if (originalStage) setPipelineStage(originalStage);
  document.getElementById("validate-button").disabled = false;
  document.getElementById("validate-label").textContent = "Run validation";
  document.getElementById("busy-message").hidden = true;
  document.getElementById("validation-form").removeAttribute("aria-busy");
});
