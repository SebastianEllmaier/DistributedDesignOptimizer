# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Application entry point for the DDO Viewer Qt application."""

import sys
import os
import logging

from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication

from .styles.Theme import apply_light_theme
from .widgets.MainWindow import MainWindow

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


def main() -> int:
    """Application entry point.

    Returns:
        int: The application exit code.
    """
    # Load environment variables
    load_dotenv()

    # Gather LLM config from environment
    llm_config = {
        "CLIENT_ID": os.environ.get("LLM_CLIENT_ID", ""),
        "CLIENT_SECRET": os.environ.get("LLM_CLIENT_SECRET", ""),
    }

    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("DDO Viewer")
    app.setOrganizationName("DDO")

    # Apply light theme
    apply_light_theme(app)

    # Create and show main window
    window = MainWindow(llm_config=llm_config)
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
