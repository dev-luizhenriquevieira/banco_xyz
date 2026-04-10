from dataclasses import dataclass


@dataclass
class OperationResult:
    success: bool
    message: str
    data: object = None
