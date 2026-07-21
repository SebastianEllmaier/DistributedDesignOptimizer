/**
 * Pseudocode-to-Code Traceability: Popup on hover/click
 *
 * Uses event delegation on document — works regardless of DOM replacement
 * by Material for MkDocs instant navigation.
 * 
 * Supports multiple algorithm traceability containers (unified, ALC, etc.)
 */
(function() {
  var pinnedId = null;
  var hideTimeout = null;
  var currentContainer = null;

  // Selector for any pseudocode traceability container
  var CONTAINER_SELECTOR = '.unified-algorithmic-structure-pseudocode-traceability, .alc-pseudocode-traceability, .consensus-alc-pseudocode-traceability, .aladin-pseudocode-traceability, .sbdp-pseudocode-traceability, .subsystem-copyfrom-pseudocode-traceability, .subsystem-copyto-pseudocode-traceability, .subsystem-run-iterative-optimization-pseudocode-traceability';

  function getPopupData(id, container) {
    if (!container) container = document;
    var el = container.querySelector('.impl-data[data-mapping-id="' + id + '"]');
    if (!el) return null;
    return { label: el.dataset.label, html: el.innerHTML };
  }

  function getPopup(container) {
    if (!container) return null;
    return container.querySelector('.impl-popup');
  }

  function getContainer(element) {
    return element.closest(CONTAINER_SELECTOR);
  }

  function showPopup(id, anchorEl, container) {
    var data = getPopupData(id, container);
    if (!data) return;
    var popup = getPopup(container);
    if (!popup) return;

    clearTimeout(hideTimeout);
    currentContainer = container;

    var popupLabel = popup.querySelector('.impl-popup-label');
    var popupBody = popup.querySelector('.impl-popup-body');
    popupLabel.textContent = data.label;

    // Build body: line-level implementations
    var bodyHtml = data.html;

    // Check for math symbol IDs on this element
    var mathSymbolIds = anchorEl.dataset.mathSymbolIds;
    if (mathSymbolIds) {
      var symbolIds = mathSymbolIds.split(',');
      bodyHtml += '<div class="impl-popup-math-section">';
      bodyHtml += '<div class="impl-popup-math-header">Math Notation Reference</div>';
      for (var i = 0; i < symbolIds.length; i++) {
        var symData = getPopupData(symbolIds[i], container);
        if (!symData) continue;
        var symEl = container.querySelector('.impl-data[data-mapping-id="' + symbolIds[i] + '"]');
        var latex = symEl ? (symEl.dataset.symbolLatex || '') : '';
        bodyHtml += '<div class="impl-popup-math-symbol">';
        bodyHtml += '<div class="impl-popup-math-symbol-header">';
        if (latex) {
          bodyHtml += '<span class="impl-popup-math-latex">\\(' + latex + '\\)</span> ';
        }
        bodyHtml += '<span class="impl-popup-math-label">' + symData.label + '</span>';
        bodyHtml += '</div>';
        bodyHtml += '<div class="impl-popup-math-impls">' + symData.html + '</div>';
        bodyHtml += '</div>';
      }
      bodyHtml += '</div>';
    }

    popupBody.innerHTML = bodyHtml;

    // Re-render KaTeX in the popup if available
    if (mathSymbolIds && window.renderMathInElement) {
      try { window.renderMathInElement(popupBody); } catch(e) {}
    } else if (mathSymbolIds && window.katex) {
      // Fallback: manually render \(...\) spans
      popupBody.querySelectorAll('.impl-popup-math-latex').forEach(function(el) {
        var tex = el.textContent.replace(/^\\\(/, '').replace(/\\\)$/, '');
        try {
          el.innerHTML = window.katex.renderToString(tex, { throwOnError: false });
        } catch(e) {}
      });
    }

    popup.style.display = 'block';

    // Position near the anchor element
    var lineRect = anchorEl.getBoundingClientRect();
    var containerRect = container.getBoundingClientRect();

    var top = lineRect.bottom - containerRect.top + 4;
    var left = lineRect.left - containerRect.left + 20;
    popup.style.top = top + 'px';
    popup.style.left = left + 'px';

    requestAnimationFrame(function() {
      var popupRect = popup.getBoundingClientRect();
      if (popupRect.right > containerRect.right - 10) {
        popup.style.left = Math.max(0, containerRect.width - popupRect.width - 10) + 'px';
      }
      if (popupRect.bottom > window.innerHeight - 10) {
        popup.style.top = (lineRect.top - containerRect.top - popupRect.height - 4) + 'px';
      }
    });
  }

  function hidePopup() {
    if (currentContainer) {
      var popup = getPopup(currentContainer);
      if (popup) {
        popup.style.display = 'none';
      }
    }
    currentContainer = null;
  }

  function scheduleHide() {
    clearTimeout(hideTimeout);
    hideTimeout = setTimeout(function() {
      if (!pinnedId) hidePopup();
    }, 250);
  }

  function clearHighlights() {
    document.querySelectorAll('.algo-linked.algo-active, .algo-linked.algo-clicked').forEach(function(el) {
      el.classList.remove('algo-active', 'algo-clicked');
    });
  }

  // --- Event delegation: mouseover/mouseout on document ---
  document.addEventListener('mouseover', function(e) {
    var line = e.target.closest('.algo-linked');
    if (!line) return;
    if (pinnedId) return;
    var container = getContainer(line);
    if (!container) return;
    clearTimeout(hideTimeout);
    var ids = (line.dataset.mappingIds || '').split(',');
    if (ids.length > 0 && ids[0]) {
      clearHighlights();
      line.classList.add('algo-active');
      showPopup(ids[0], line, container);
    }
  });

  document.addEventListener('mouseout', function(e) {
    var line = e.target.closest('.algo-linked');
    if (!line) return;
    if (pinnedId) return;
    // Check if we're moving to another element inside the same line
    var related = e.relatedTarget;
    if (related && line.contains(related)) return;
    line.classList.remove('algo-active');
    scheduleHide();
  });

  // --- Keep popup open when hovering over it ---
  document.addEventListener('mouseover', function(e) {
    if (e.target.closest('.impl-popup')) {
      clearTimeout(hideTimeout);
    }
  });

  document.addEventListener('mouseout', function(e) {
    var popup = e.target.closest('.impl-popup');
    if (!popup) return;
    var related = e.relatedTarget;
    if (related && popup.contains(related)) return;
    if (!pinnedId) {
      clearHighlights();
      scheduleHide();
    }
  });

  // --- Click on pseudocode line: pin/unpin ---
  document.addEventListener('click', function(e) {
    // Close button
    if (e.target.closest('.impl-popup-close')) {
      e.stopPropagation();
      pinnedId = null;
      clearHighlights();
      hidePopup();
      return;
    }

    // Don't interfere with link clicks inside popup
    if (e.target.closest('.impl-popup a')) return;

    var line = e.target.closest('.algo-linked');
    if (line) {
      var container = getContainer(line);
      if (!container) return;
      e.preventDefault();
      e.stopPropagation();
      var ids = (line.dataset.mappingIds || '').split(',');
      if (!ids.length || !ids[0]) return;

      var id = ids[0];
      if (pinnedId === id) {
        pinnedId = null;
        clearHighlights();
        hidePopup();
      } else {
        pinnedId = id;
        clearHighlights();
        line.classList.add('algo-clicked');
        showPopup(id, line, container);
      }
      return;
    }

    // Click outside: dismiss
    if (!e.target.closest(CONTAINER_SELECTOR)) {
      pinnedId = null;
      clearHighlights();
      hidePopup();
    }
  });
})();
