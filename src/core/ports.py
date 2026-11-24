"""Shared core types that adapters raise or return (architecture.md, core rule).

Core never imports an adapter. An adapter that needs to tell the core something
specific imports the type from here instead.
"""


class DuplicateUpdate(Exception):
    """This Telegram update_id was already processed. Nothing was saved (C-1, T-30)."""
