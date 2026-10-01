class ProjectArchiveError(Exception):
    """Raised when the status of an archived project is changed."""


class DuplicateProjectKeyError(Exception):
    """Raised when a project key already exists."""
