---
title: ChatPanel
---

← Back to [widgets](index.md)

# ChatPanel

**Source:** [Distributed_Design_Optimizer\postprocess\widgets\ChatPanel.py](ChatPanel_source.md)

Chat panel widget providing an AI-powered analysis interface.

## Classes

### ChatPanel

> **Inherits from:** `QWidget`

> Right panel: AI-powered analysis chat interface.

#### Methods

??? abstract "__init__(self, parent: QWidget | None) → None"
    Initialize the chat panel.


    **Args:**
    > parent: Optional parent widget.  

??? abstract "add_message(self, sender: str, text: str) → None"
    Append a formatted message to the chat history.


    **Args:**
    > sender: Display name of the message author.  
    > text: Plain text content of the message.  

??? abstract "show_thinking(self) → None"
    Display a thinking indicator and record cursor position for removal.

??? abstract "remove_thinking(self) → None"
    Remove the thinking indicator using stored block position.

??? abstract "show_response(self, text: str) → None"
    Remove thinking indicator and show the AI response.


    **Args:**
    > text: The AI response text to display.  

??? abstract "set_context(self, analysis_type: str, filename: str) → None"
    Update the context label at the top.


    **Args:**
    > analysis_type: Type of analysis being viewed.  
    > filename: Name of the loaded data file.  

??? abstract "set_llm_available(self, available: bool) → None"
    Enable or disable chat input based on LLM availability.


    **Args:**
    > available: Whether the LLM API is accessible.  

??? abstract "clear_history(self) → None"
    Clear all chat messages.

??? abstract "get_history_html(self) → str"
    Return the chat history as HTML for persistence.


    **Returns:**
    > The chat history content as an HTML string.  

??? abstract "restore_history(self, html: str) → None"
    Restore chat history from saved HTML.


    **Args:**
    > html: Previously saved HTML content to restore.  

