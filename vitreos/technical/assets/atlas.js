"use strict";

(() => {
  const control = document.querySelector("#theme");
  if (!control) return;

  const key = "Vitreos-atlas-theme";
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
