# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Chat panel widget providing an AI-powered analysis interface."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextBrowser,
    QLineEdit, QPushButton, QLabel, QMenu,
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QTextCursor, QAction
from html import escape as html_escape

from ..styles.Theme import PRIMARY, PRIMARY_DARK


class ChatPanel(QWidget):
    """Right panel: AI-powered analysis chat interface."""

    message_sent = Signal(str)  # user message text

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the chat panel.

        Args:
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self.setMinimumWidth(280)
        self.setMinimumHeight(300)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        # Context indicator
        self._context_label = QLabel("No analysis context loaded")
        self._context_label.setWordWrap(True)
        self._context_label.setStyleSheet("font-size: 10pt; color: gray;")
        layout.addWidget(self._context_label)

        # Chat history (rich text)
        self._chat_history = QTextBrowser()
        self._chat_history.setOpenExternalLinks(True)
        self._chat_history.setReadOnly(True)
        self._chat_history.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._chat_history.customContextMenuRequested.connect(self._show_context_menu)
        layout.addWidget(self._chat_history, stretch=1)

        # Input row
        input_row = QHBoxLayout()
        self._input_field = QLineEdit()
        self._input_field.setPlaceholderText("Ask about the current visualization...")
        self._input_field.returnPressed.connect(self._on_send)
        input_row.addWidget(self._input_field)

        self._send_btn = QPushButton("Send")
        self._send_btn.setMinimumWidth(60)
        self._send_btn.clicked.connect(self._on_send)
        self._send_btn.setStyleSheet(
            f"QPushButton {{ background-color: {PRIMARY}; color: white; "
            f"font-weight: bold; padding: 5px 12px; border-radius: 3px; }}"
            f"QPushButton:hover {{ background-color: {PRIMARY_DARK}; }}"
        )
        input_row.addWidget(self._send_btn)
        layout.addLayout(input_row)

        # Initial message
        self.add_message("AI Assistant", "Hello! Launch a visualization from the Topology Analysis controls, then ask me anything about it.")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    _THINKING_MARKER = '<!--THINKING-->'

    def add_message(self, sender: str, text: str) -> None:
        """Append a formatted message to the chat history.

        Args:
            sender: Display name of the message author.
            text: Plain text content of the message.
        """
        safe_text = html_escape(text)
        if sender == "You":
            html = f'<p><b style="color: #4fc3f7;">You:</b> {safe_text}</p>'
        else:
            html = f'<p><b style="color: #81c784;">AI Assistant:</b> {safe_text}</p>'
        self._chat_history.append(html)
        self._scroll_to_bottom()

    def show_thinking(self) -> None:
        """Display a thinking indicator and record cursor position for removal."""
        self._thinking_block_start = self._chat_history.document().blockCount()
        self._chat_history.append(f'{self._THINKING_MARKER}<p><i style="color: gray;">Thinking...</i></p>')
        self._set_input_enabled(False)

    def remove_thinking(self) -> None:
        """Remove the thinking indicator using stored block position."""
        if not hasattr(self, '_thinking_block_start'):
            return
        doc = self._chat_history.document()
        start_block = self._thinking_block_start
        end_block = doc.blockCount()
        if start_block >= end_block:
            return
        cursor = QTextCursor(doc.findBlockByNumber(start_block))
        cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.MoveAnchor)
        # Select from start of the thinking block to end of document
        cursor.setPosition(doc.findBlockByNumber(start_block).position(), QTextCursor.MoveMode.MoveAnchor)
        cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.KeepAnchor)
        cursor.removeSelectedText()
        # Clean up any trailing empty block
        if cursor.block().text().strip() == '':
            cursor.select(QTextCursor.SelectionType.BlockUnderCursor)
            cursor.removeSelectedText()
        del self._thinking_block_start
        self._scroll_to_bottom()

    def show_response(self, text: str) -> None:
        """Remove thinking indicator and show the AI response.

        Args:
            text: The AI response text to display.
        """
        self.remove_thinking()
        self.add_message("AI Assistant", text)
        self._set_input_enabled(True)
        self._input_field.setFocus()

    def set_context(self, analysis_type: str, filename: str) -> None:
        """Update the context label at the top.

        Args:
            analysis_type: Type of analysis being viewed.
            filename: Name of the loaded data file.
        """
        self._context_label.setText(f"Context: {analysis_type}\nFile: {filename}")

    def set_llm_available(self, available: bool) -> None:
        """Enable or disable chat input based on LLM availability.

        Args:
            available: Whether the LLM API is accessible.
        """
        self._set_input_enabled(available)
        if not available:
            self._input_field.setToolTip("LLM API is not available. Install llm_api to enable chat.")
            self._send_btn.setToolTip("LLM API is not available.")
        else:
            self._input_field.setToolTip("")
            self._send_btn.setToolTip("")

    def clear_history(self) -> None:
        """Clear all chat messages."""
        self._chat_history.clear()

    def get_history_html(self) -> str:
        """Return the chat history as HTML for persistence.

        Returns:
            The chat history content as an HTML string.
        """
        return self._chat_history.toHtml()

    def restore_history(self, html: str) -> None:
        """Restore chat history from saved HTML.

        Args:
            html: Previously saved HTML content to restore.
        """
        if html:
            self._chat_history.setHtml(html)

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    def _on_send(self) -> None:
        text = self._input_field.text().strip()
        if not text:
            return
        self._input_field.clear()
        self.add_message("You", text)
        self.show_thinking()
        self.message_sent.emit(text)

    def _set_input_enabled(self, enabled: bool) -> None:
        self._input_field.setEnabled(enabled)
        self._send_btn.setEnabled(enabled)

    def _scroll_to_bottom(self) -> None:
        """Scroll chat history to the bottom."""
        cursor = self._chat_history.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self._chat_history.setTextCursor(cursor)

    def _show_context_menu(self, pos) -> None:
        """Right-click context menu for chat history."""
        menu = QMenu(self)

        copy_action = QAction("Copy Selected Text", self)
        copy_action.triggered.connect(self._chat_history.copy)
        copy_action.setEnabled(self._chat_history.textCursor().hasSelection())
        menu.addAction(copy_action)

        clear_action = QAction("Clear History", self)
        clear_action.triggered.connect(self.clear_history)
        menu.addAction(clear_action)

        menu.exec(self._chat_history.viewport().mapToGlobal(pos))
