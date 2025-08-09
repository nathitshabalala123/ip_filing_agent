from typing import List
from ..schemas import ConflictItem

DISCLAIMER = (
    "This is a basic, automated name check for identical or highly similar marks. "
    "It is not a comprehensive availability search and does not guarantee registration. "
    "For legal advice, consult a qualified attorney."
)


def basic_conflict_check(mark_text: str, nice_classes: List[int]) -> List[ConflictItem]:
    # Placeholder: In production, perform a real query against CIPC's public database (if permissible)
    # or a reputable third-party dataset. This MVP returns an empty result set with a disclaimer.
    _ = (mark_text, nice_classes)
    return [] 