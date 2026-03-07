"""Aesthetic mapping dataclass."""

from __future__ import annotations

from dataclasses import dataclass, fields, replace


# Every method returns a new object — the original is never modified. This enables safe branching.
@dataclass(frozen=True, slots=True)
class Aes:
    """Maps DataFrame column names to visual properties.

    All fields are optional. When merging, non-None fields from the
    override take precedence.
    """

    x: str | None = None
    y: str | None = None
    color: str | None = None
    fill: str | None = None
    size: str | None = None
    shape: str | None = None
    alpha: str | None = None
    group: str | None = None
    label: str | None = None
    weight: str | None = None

    def merge(self, other: Aes) -> Aes:
        """Merge with another Aes. Non-None fields from `other` win.

        Args:
            other: The override Aes whose non-None fields take precedence.

        Returns:
            A new Aes with merged fields.
        """
        updates = {f.name: getattr(other, f.name) for f in fields(other) if getattr(other, f.name) is not None}
        return replace(self, **updates)

    def resolve_fill(self) -> Aes:
        """Default fill to color if fill is unset.

        Returns:
            A new Aes with fill resolved.
        """
        if self.fill is None and self.color is not None:
            return replace(self, fill=self.color)
        return self
