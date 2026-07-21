# Copyright (C) The DistributedDesignOptimizer Contributors
# SPDX-License-Identifier: MIT
#
# MkDocs hook: repository URL references.
#
# Replaces repo:KEY tokens with URLs derived from the single `repo_url`
# defined in mkdocs.yml, so the repository location has one source of truth.
#
# Usage in markdown:
#   Clone the repository from repo:url.
#   Report bugs on the repo:issues tab.
#   Contribute via the repo:pulls tab.
#
# Configuration in mkdocs.yml:
#   repo_url: https://.../DistributedDesignOptimizer
#   hooks:
#     - hooks/repo_url.py

import logging
import re
from pathlib import Path

log = logging.getLogger("mkdocs.hooks.repo_url")

# Match repo:KEY where KEY is one of the supported sub-paths.
_REPO_REF = re.compile(r"repo:(url|issues|pulls)")

# Root files (outside the docs tree) whose repository URL is kept in sync with
# `repo_url`. Each entry maps a repo-root-relative filename to a regex that
# anchors on the surrounding text and captures it, so the substitution can
# normalise either the `repo:url` token or a previously inserted URL back to the
# current `repo_url`. Anchoring keeps unrelated links (e.g. the documentation
# URL) untouched and makes the rewrite idempotent across builds.
_ROOT_URL_PATTERNS: dict[str, re.Pattern] = {
    # LICENSE: URL on its own line after the request sentence.
    "LICENSE": re.compile(
        r"(pull requests to (?:our|my) GitHub repository:[ \t]*\r?\n)"
        r"(?:repo:url|https?://\S+)"
    ),
    # README.md: URL inside the "this repository" markdown link.
    "README.md": re.compile(
        r"(pull requests to \[this repository\]\()(?:repo:url|https?://[^)]+)(\))"
    ),
}

# Module-level state populated from mkdocs.yml.
_urls: dict[str, str] = {}


def on_config(config):
    """Derive all repository URLs from the single `repo_url` setting."""
    _urls.clear()

    repo_url = (config.get("repo_url") or "").rstrip("/")
    if not repo_url:
        log.warning("repo_url hook: no `repo_url` set in mkdocs.yml")
        return config

    _urls["url"] = repo_url
    _urls["issues"] = f"{repo_url}/issues"
    _urls["pulls"] = f"{repo_url}/pulls"

    _update_root_files(config)
    return config


def _update_root_files(config):
    """Insert the repository URL into root files outside the docs tree.

    Files such as LICENSE and README.md live outside the docs tree, so they are
    not processed by on_page_markdown. This keeps their repository URL in sync
    with the single `repo_url` source of truth. The rewrite is idempotent: each
    anchored pattern normalises either the `repo:url` token or a previously
    inserted URL to the current repo_url.
    """
    url = _urls.get("url")
    config_file = config.get("config_file_path")
    if not url or not config_file:
        return

    # mkdocs.yml lives in docs_src/, so the repo root is its parent's parent.
    root = Path(config_file).resolve().parent.parent

    def _sub(match):
        groups = match.groups()
        return groups[0] + url + (groups[1] if len(groups) > 1 else "")

    for name, pattern in _ROOT_URL_PATTERNS.items():
        path = root / name
        if not path.is_file():
            log.warning("repo_url hook: %s not found at %s", name, path)
            continue
        text = path.read_text(encoding="utf-8")
        new_text, count = pattern.subn(_sub, text)
        if count and new_text != text:
            path.write_text(new_text, encoding="utf-8")
            log.info("repo_url hook: set %s repository URL -> %s", name, url)


def on_page_markdown(markdown, page, config, files):
    """Replace repo:KEY tokens with the corresponding repository URL."""
    if not _urls:
        return markdown

    def _replace(match):
        key = match.group(1)
        url = _urls.get(key)
        if not url:
            log.warning("repo_url hook: unknown token 'repo:%s' on page %s", key, page.url)
            return match.group(0)
        return url

    return _REPO_REF.sub(_replace, markdown)
