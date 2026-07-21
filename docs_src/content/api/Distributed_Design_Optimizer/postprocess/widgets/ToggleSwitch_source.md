---
title: ToggleSwitch (Source)
---

← Back to [ToggleSwitch documentation](ToggleSwitch.md)

# ToggleSwitch - Source Code

**File:** `Distributed_Design_Optimizer\postprocess\widgets\ToggleSwitch.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Custom toggle switch widget — a modern on/off slider control."""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import Signal, Qt, QRect, QPropertyAnimation, Property, QEasingCurve
from PySide6.QtGui import QPainter, QColor, QPen

from ..styles.Theme import PRIMARY


class _SwitchTrack(QWidget):
    """The sliding toggle track (no label)."""

    toggled = Signal(bool)

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the switch track widget.

        Args:
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self.setFixedSize(40, 22)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._checked = False
        self._thumb_x = 3.0

        self._anim = QPropertyAnimation(self, b"thumb_x", self)
        self._anim.setDuration(120)
        self._anim.setEasingCurve(QEasingCurve.Type.InOutQuad)

    def isChecked(self) -> bool:
        """Return whether the switch is in the on state.

        Returns:
            True if the switch is on, False otherwise.
        """
        return self._checked

    def setChecked(self, checked: bool) -> None:
        """Set the checked state and animate the thumb.

        Args:
            checked: ``True`` to turn on, ``False`` to turn off.
        """
        if checked == self._checked:
            return
        self._checked = checked
        target = 21.0 if checked else 3.0
        self._anim.stop()
        self._anim.setStartValue(self._thumb_x)
        self._anim.setEndValue(target)
        self._anim.start()
        self.toggled.emit(checked)

    def _get_thumb_x(self) -> float:
        return self._thumb_x

    def _set_thumb_x(self, val: float) -> None:
        self._thumb_x = val
        self.update()

    thumb_x = Property(float, _get_thumb_x, _set_thumb_x)

    def mousePressEvent(self, event) -> None:
        """Toggle the switch state on mouse press.

        Args:
            event: The mouse press event.
        """
        if self.isEnabled():
            self.setChecked(not self._checked)

    def changeEvent(self, event) -> None:
        """Repaint when the enabled state changes.

        Args:
            event: The change event triggered by Qt.
        """
        super().changeEvent(event)
        if event.type() == event.Type.EnabledChange:
            self.update()

    def paintEvent(self, event) -> None:
        """Draw the track and sliding thumb.

        Args:
            event: The paint event triggered by Qt.
        """
        p = QPainter()
        if not p.begin(self):
            return
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        disabled = not self.isEnabled()

        # Track
        if disabled:
            track_color = QColor("#ddd")
        elif self._checked:
            track_color = QColor(PRIMARY)
        else:
            track_color = QColor("#ccc")
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(track_color)
        p.drawRoundedRect(QRect(0, 0, 40, 22), 11, 11)

        # Thumb
        p.setBrush(QColor("#f0f0f0") if disabled else QColor("white"))
        p.setPen(QPen(QColor("#ccc") if disabled else QColor("#aaa"), 0.5))
        p.drawEllipse(int(self._thumb_x), 3, 16, 16)
        p.end()


class ToggleSwitch(QWidget):
    """A labelled toggle switch: [label] [=====O]."""

    toggled = Signal(bool)

    def __init__(self, label: str = "", parent: QWidget | None = None) -> None:
        """Initialize the labelled toggle switch.

        Args:
            label: Text label displayed beside the switch.
            parent: Optional parent widget.
        """
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 2, 0, 2)
        layout.setSpacing(6)

        self._label = QLabel(label)
        layout.addWidget(self._label)

        self._switch = _SwitchTrack(self)
        self._switch.toggled.connect(self.toggled.emit)
        layout.addWidget(self._switch)

        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)

    def isChecked(self) -> bool:
        """Return whether the toggle is checked.

        Returns:
            True if the toggle is on, False otherwise.
        """
        return self._switch.isChecked()

    def setChecked(self, checked: bool) -> None:
        """Set the toggle checked state.

        Args:
            checked: ``True`` to turn on, ``False`` to turn off.
        """
        self._switch.setChecked(checked)

    def setToolTip(self, tip: str) -> None:
        """Apply the tooltip to the label and switch track.

        Args:
            tip: Tooltip text.
        """
        super().setToolTip(tip)
        self._label.setToolTip(tip)
        self._switch.setToolTip(tip)

```
