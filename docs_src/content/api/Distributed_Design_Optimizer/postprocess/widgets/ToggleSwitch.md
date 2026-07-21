---
title: ToggleSwitch
---

← Back to [widgets](index.md)

# ToggleSwitch

**Source:** [Distributed_Design_Optimizer\postprocess\widgets\ToggleSwitch.py](ToggleSwitch_source.md)

Custom toggle switch widget — a modern on/off slider control.

## Classes

### _SwitchTrack

> **Inherits from:** `QWidget`

> The sliding toggle track (no label).

#### Methods

??? abstract "__init__(self, parent: QWidget | None) → None"
    Initialize the switch track widget.


    **Args:**
    > parent: Optional parent widget.  

??? abstract "isChecked(self) → bool"
    Return whether the switch is in the on state.


    **Returns:**
    > True if the switch is on, False otherwise.  

??? abstract "setChecked(self, checked: bool) → None"
    Set the checked state and animate the thumb.


    **Args:**
    > checked: ``True`` to turn on, ``False`` to turn off.  

??? abstract "mousePressEvent(self, event) → None"
    Toggle the switch state on mouse press.


    **Args:**
    > event: The mouse press event.  

??? abstract "changeEvent(self, event) → None"
    Repaint when the enabled state changes.


    **Args:**
    > event: The change event triggered by Qt.  

??? abstract "paintEvent(self, event) → None"
    Draw the track and sliding thumb.


    **Args:**
    > event: The paint event triggered by Qt.  

### ToggleSwitch

> **Inherits from:** `QWidget`

> A labelled toggle switch: [label] [=====O].

#### Methods

??? abstract "__init__(self, label: str, parent: QWidget | None) → None"
    Initialize the labelled toggle switch.


    **Args:**
    > label: Text label displayed beside the switch.  
    > parent: Optional parent widget.  

??? abstract "isChecked(self) → bool"
    Return whether the toggle is checked.


    **Returns:**
    > True if the toggle is on, False otherwise.  

??? abstract "setChecked(self, checked: bool) → None"
    Set the toggle checked state.


    **Args:**
    > checked: ``True`` to turn on, ``False`` to turn off.  

??? abstract "setToolTip(self, tip: str) → None"
    Apply the tooltip to the label and switch track.


    **Args:**
    > tip: Tooltip text.  

