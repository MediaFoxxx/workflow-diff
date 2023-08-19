from dataclasses import dataclass, field


@dataclass(slots=True, unsafe_hash=True)
class Link:
    """Class of link for Workflow."""

    guid: str = field(compare=True)
    src: str = field(compare=False)
    dst: str = field(compare=False)
