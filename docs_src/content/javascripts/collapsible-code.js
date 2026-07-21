/* Collapsible code blocks: auto-initialise any <div class="collapsible-code"> */
(function () {
  function init() {
    document.querySelectorAll(".collapsible-code").forEach(function (wrapper) {
      if (wrapper.dataset.collapsibleInit) return; // already initialised
      wrapper.dataset.collapsibleInit = "1";

      // Start collapsed
      wrapper.classList.add("collapsed");

      // Create toggle button
      var btn = document.createElement("button");
      btn.className = "collapsible-code-toggle";
      btn.textContent = "\u25bc  Show more";
      wrapper.appendChild(btn);

      btn.addEventListener("click", function () {
        var isCollapsed = wrapper.classList.toggle("collapsed");
        btn.textContent = isCollapsed ? "\u25bc  Show more" : "\u25b2  Show less";
      });
    });
  }

  // Run on initial page load
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  // Re-run on MkDocs Material instant navigation (SPA page switches).
  // document$ is an RxJS observable exposed by Material after its JS loads.
  function subscribeToInstantNav() {
    if (typeof document$ !== "undefined") {
      document$.subscribe(function () { init(); });
    } else {
      // Retry until Material's JS has loaded and exposed document$
      var attempts = 0;
      var interval = setInterval(function () {
        attempts++;
        if (typeof document$ !== "undefined") {
          clearInterval(interval);
          document$.subscribe(function () { init(); });
        } else if (attempts > 50) {
          clearInterval(interval);
        }
      }, 100);
    }
  }
  subscribeToInstantNav();
})();
