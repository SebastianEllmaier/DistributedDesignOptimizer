document$.subscribe(({ body }) => {
  // KaTeX options with trust enabled for \href links
  const katexOptions = {
    throwOnError: false,
    trust: true,  // Enable \href and \url commands
  };

  // 1. Render math inside arithmatex spans (from pymdownx.arithmatex)
  body.querySelectorAll(".arithmatex:not(.math-rendered)").forEach((el) => {
    const text = el.textContent;
    const display = text.startsWith("\\[");
    const math = text
      .replace(/^\\\(/, "").replace(/\\\)$/, "")
      .replace(/^\\\[/, "").replace(/\\\]$/, "")
      .trim();
    try {
      katex.render(math, el, { ...katexOptions, displayMode: display });
    } catch (e) { /* skip invalid math */ }
    el.classList.add("math-rendered");
  });

  // 2. Render raw \(...\) / \[...\] in non-arithmatex content (e.g. pseudocode)
  renderMathInElement(body, {
    delimiters: [
      { left: "\\[", right: "\\]", display: true },
      { left: "\\(", right: "\\)", display: false },
    ],
    ignoredTags: [
      "script", "noscript", "style", "textarea", "pre", "code",
      "annotation", "annotation-xml",
    ],
    ignoredClasses: ["arithmatex", "katex", "katex-display", "math-rendered"],
    ...katexOptions,
  });

  // 3. Render $...$ / $$...$$ math inside .doc-table cells.
  //    pymdownx.arithmatex does not run inside md_in_html/raw HTML tables,
  //    so dollar-delimited math would otherwise appear literally.
  body.querySelectorAll(".doc-table").forEach((table) => {
    renderMathInElement(table, {
      delimiters: [
        { left: "$$", right: "$$", display: true },
        { left: "$", right: "$", display: false },
      ],
      ignoredTags: [
        "script", "noscript", "style", "textarea", "pre", "code",
        "annotation", "annotation-xml",
      ],
      ignoredClasses: ["katex", "katex-display", "math-rendered"],
      ...katexOptions,
    });
  });
})
