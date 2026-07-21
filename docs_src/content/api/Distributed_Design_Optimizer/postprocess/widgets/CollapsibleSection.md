---
title: CollapsibleSection
---

← Back to [widgets](index.md)

# CollapsibleSection

**Source:** [Distributed_Design_Optimizer\postprocess\widgets\CollapsibleSection.py](CollapsibleSection_source.md)

Reusable collapsible section widget for panels with expandable groups.

## Classes

### CollapsibleSection

> **Inherits from:** `QWidget`

> A section with a clickable header that expands/collapses its content.

#### Methods

??? abstract "__init__(self, title: str, parent: QWidget | None, initially_expanded: bool) → None"
    Initialize the collapsible section.


    **Args:**
    > title: Header text displayed on the toggle button.  
    > parent: Optional parent widget.  
    > initially_expanded: Whether the section starts expanded.  

??? abstract "content_layout(self) → QVBoxLayout"
    Return the layout for adding child widgets.


    **Returns:**
    > The vertical box layout that holds the section's content.  

??? abstract "set_expanded(self, expanded: bool) → None"
    Programmatically expand or collapse the section.


    **Args:**
    > expanded: Whether the section should be expanded.  

??? abstract "showEvent(self, event) → None"
    Re-apply header styling when the widget becomes visible.


    **Args:**
    > event: The show event triggered by Qt.  

