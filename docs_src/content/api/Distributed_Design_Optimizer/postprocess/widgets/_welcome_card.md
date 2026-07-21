---
title: _welcome_card
---

← Back to [widgets](index.md)

# _welcome_card

**Source:** [Distributed_Design_Optimizer\postprocess\widgets\_welcome_card.py](_welcome_card_source.md)

Welcome card widget shown on startup before any plot is active.

## Classes

### WelcomeCard

> **Inherits from:** `QWidget`

> Start page with quick-start guide shown when no plot is active.

#### Methods

??? abstract "__init__(self, parent: QWidget | None) → None"
    Initialize the welcome card with logo, workflow steps, and accent styling.


    **Args:**
    > parent: Optional parent widget.  

??? abstract "showEvent(self, event) → None"
    Re-apply accent color when the widget becomes visible.


    **Args:**
    > event: The show event.  

