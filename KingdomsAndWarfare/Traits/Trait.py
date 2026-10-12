"""Traits: named special abilities or weaknesses that can be attached to a unit."""

from datetime import datetime


class Trait:
    """A named special ability or weakness that can be attached to a unit.

    Attributes:
        name: Display name of the trait, e.g. "Magic Resistant".
        description: Rules text explaining what the trait does.
        created: Timestamp string recording when the trait was created.
        homebrew: True if the trait is user-made rather than from the official rules.
    """

    def __init__(self, name: str, description: str):
        """Create a new homebrew trait stamped with the current time.

        Args:
            name: Display name of the trait.
            description: Rules text explaining what the trait does.
        """
        self.name = name
        self.description = description
        self.created = str(datetime.now())
        self.homebrew = True

    def __eq__(self, __value: "Trait") -> bool:
        """Compare traits by name, description, and homebrew flag.

        The `created` timestamp is ignored, so a trait equals its own
        round-tripped copy from `to_dict` / `from_dict`.
        """
        return (
            self.name == __value.name
            and self.description == __value.description
            and self.homebrew == __value.homebrew
        )

    def to_dict(self) -> dict:
        """Serialize the trait to a JSON-friendly dict that `from_dict` can read back.
            Useful for storing in a flat file or transmitting via AJAX.
        """
        return {
            "name": self.name,
            "description": self.description,
            "created": self.created,
            "homebrew": self.homebrew,
        }

    def from_dict(traitDict: dict) -> "Trait":
        """Build a trait from a dict produced by `to_dict`.

        Call this on the class: `Trait.from_dict(data)`.

        Args:
            traitDict: A dict with "name", "description", "created", and "homebrew" keys.

        Returns:
            A new trait with the stored values, including the original creation time.

        Raises:
            KeyError: If any expected key is missing.
        """
        newTrait = Trait(traitDict["name"], traitDict["description"])
        newTrait.homebrew = traitDict["homebrew"]
        newTrait.created = traitDict["created"]
        return newTrait
