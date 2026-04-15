from dataclasses import dataclass


@dataclass(frozen=True)
class CommunityCard:
    title: str
    action: str
    amount: int = 0
    target_position: int | None = None