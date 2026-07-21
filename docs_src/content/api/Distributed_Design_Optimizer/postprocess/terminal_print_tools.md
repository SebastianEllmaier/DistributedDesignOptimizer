---
title: terminal_print_tools
---

← Back to [postprocess](index.md)

# terminal_print_tools

**Source:** [Distributed_Design_Optimizer\postprocess\terminal_print_tools.py](terminal_print_tools_source.md)

ANSI color constants and print utilities for DDO terminal output.

## Functions

??? abstract "ddo_print(text: str, indent: int) → None"
    Print a DDO-colored line with automatic wrapping at the border width.

    If the line (including the ``%%% `` prefix and any indentation) exceeds
    :data:`DDO_BORDER_WIDTH`, it is wrapped and continuation lines are
    indented to align with the start of the text on the first line.  When the
    text has no leading whitespace, a default 4-space indent is used for
    continuation lines.

    If ``text`` contains newline characters, each resulting line is printed
    separately so that every line receives the ``%%% `` prefix.


    **Args:**
    > text: The message to print **after** the ``%%% `` prefix.  
    > indent: Number of 4-space indentation levels inside the ``%%% `` prefix.  

??? abstract "ddo_print_border() → None"
    Print a full-width DDO-colored border line.

