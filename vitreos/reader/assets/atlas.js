"use strict";

(() => {
  function openFragment() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    if (!target) return;
    for (let node = target; node; node = node.parentElement) {
      if (node.tagName === "DETAILS") node.open = true;
    }
    target.scrollIntoView();
  }
  window.addEventListener("hashchange", openFragment);
  if (location.hash) openFragment();
  const control = document.querySelector("#theme");
  if (!control) return;

  const key = "vitreos-atlas-theme";
  const choices = new Set(["system", "light", "dark"]);

  function apply(choice) {
    const theme = choices.has(choice) ? choice : "system";
    if (theme === "system") {
      delete document.documentElement.dataset.theme;
    } else {
      document.documentElement.dataset.theme = theme;
    }
    control.value = theme;
  }

  let saved = "system";
  try {
    saved = localStorage.getItem(key) || "system";
  } catch {
  }
  apply(saved);
  control.closest("label").hidden = false;

  control.addEventListener("change", () => {
    apply(control.value);
    try {
      if (control.value === "system") localStorage.removeItem(key);
      else localStorage.setItem(key, control.value);
    } catch {
    }
  });
})();
