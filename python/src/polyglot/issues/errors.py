class LabelNotFoundError(Exception):
    """Raised when a label is not found."""

class AssigneeNotFoundError(Exception):
    """Raised when an assignee is not found."""

class InvalidStatusTransitionError(Exception):
    """Raised when an invalid status transition is attempted."""