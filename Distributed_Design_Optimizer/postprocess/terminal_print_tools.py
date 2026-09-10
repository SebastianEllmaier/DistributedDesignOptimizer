
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""ANSI color constants and print utilities for DDO terminal output."""

import textwrap

DDO_Color = "\033[38;2;3;89;112m" # color #035970 of the Distributed_Design_Optmizer
Reset = "\033[0m" # reset

DDO_BORDER = "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" # 120 chars
DDO_BORDER_WIDTH = len(DDO_BORDER)  # 120


def ddo_print(text: str, indent: int = 0) -> None:
    """Print a DDO-colored line with automatic wrapping at the border width.

    If the line (including the ``%%% `` prefix and any indentation) exceeds
    :data:`DDO_BORDER_WIDTH`, it is wrapped and continuation lines are
    indented to align with the start of the text on the first line.  When the
    text has no leading whitespace, a default 4-space indent is used for
    continuation lines.

    If ``text`` contains newline characters, each resulting line is printed
    separately so that every line receives the ``%%% `` prefix.

    Args:
        text: The message to print **after** the ``%%% `` prefix.
        indent: Number of 4-space indentation levels inside the ``%%% `` prefix.
    """
    # Handle multi-line strings by recursing on each line,
    # preserving the leading whitespace of the first line for all subsequent lines.
    if "\n" in text:
        lines = text.split("\n")
        leading_spaces = " " * (len(lines[0]) - len(lines[0].lstrip()))
        ddo_print(lines[0], indent)
        for line in lines[1:]:
            ddo_print(leading_spaces + line, indent)
        return

    pad = "    " * indent
    prefix = f"%%% {pad}"

    max_width = DDO_BORDER_WIDTH - len(prefix)

    if max_width <= 0:
        # Safety: if indent is so deep that wrapping is impossible, just print as-is
        print(f"{DDO_Color}{prefix}{text}{Reset}")
        return

    # Align continuation lines with the text start of the first line.
    # If the text has leading whitespace (e.g. aligned under a class name),
    # reuse that whitespace; otherwise fall back to a 4-space indent.
    leading = len(text) - len(text.lstrip())
    subsequent = " " * leading if leading > 0 else "    "

    wrapped = textwrap.wrap(text, width=max_width, subsequent_indent=subsequent,
                            break_long_words=False, break_on_hyphens=False)
    if not wrapped:
        print(f"{DDO_Color}{prefix}{Reset}")
        return

    for line in wrapped:
        print(f"{DDO_Color}{prefix}{line}{Reset}")


def ddo_print_border() -> None:
    """Print a full-width DDO-colored border line."""
    print(f"{DDO_Color}{DDO_BORDER}{Reset}")