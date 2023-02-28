import enum


class StatusCode(enum.Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    ERROR = 'error'
    FINISHED = 'finished'
