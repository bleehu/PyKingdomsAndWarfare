"""A player-run kingdom: its domain stats, treasury, researched unit types, and mustered armies."""

from uuid import uuid4, UUID

from ..Units.Unit import Unit
from ..Units.UnitFactory import clone_unit


class Kingdom:
    """A domain that researches unit types, musters armies from them, and pays for it all in gold.
    Kingdoms face each other in Intrigues and Battles. Generally, a Kingdom or Domain is either
    controlled by one or more human players, or is a "Realm" controlled by NPCs. 

    Gold is never stored directly. Every change is recorded as a
    `Kingdom.LedgerEntry`, and the treasury balance is the sum of the ledger.

    Attributes:
        name: Display name of the kingdom.
        description: Flavor text describing the kingdom.
        recruitableUnitTypes: Researched unit prefabrications, keyed by research UUID.
        armies: Mustered units, keyed by army ID. These should be named instances of a unit type.
        diplomacy: Diplomacy skill bonus.
        espionage: Espionage skill bonus.
        lore: Lore skill bonus.
        operations: Operations skill bonus.
        communications: Communications defense score.
        resolve: Resolve defense score.
        resources: Resources defense score.
        ledger: Every gold transaction the kingdom has made, oldest first.
    """

    def __init__(self, name, description):
        """Create a kingdom with default domain stats and an empty treasury.

        Args:
            name: Display name of the kingdom.
            description: Flavor text describing the kingdom.
        """
        self.name = name
        self.description = description
        self.recruitableUnitTypes = {}
        self.armies = {}
        self.diplomacy = 0
        self.espionage = 0
        self.lore = 0
        self.operations = 0
        self.communications = 10
        self.resolve = 10
        self.resources = 10
        self.ledger = []

    def add_transaction(self, description: str, goldAdded: int) -> None:
        """Record a gold deposit or withdrawal in the ledger.

        Args:
            description: Human-readable reason for the transaction.
            goldAdded: Gold to add to the treasury. Use a negative value to spend gold.

        Raises:
            Kingdom.TreasuryOverdrawError: If the transaction would leave the
                treasury below zero. Nothing is recorded in that case.
        """
        if self.get_treasury() + goldAdded < 0:
            raise self.TreasuryOverdrawError(f"Kingdom {self.name} Cannot afford transaction {description} for {goldAdded}. Current Balance: {self.get_treasury()} ")
        self.ledger.append(Kingdom.LedgerEntry(description, goldAdded))

    def read_ledger(self) -> list["Kingdom.LedgerEntry"]:
        """Return a copy of the ledger, oldest transaction first.

        The returned list can be modified without affecting the kingdom.
        """
        return list(self.ledger)

    def get_treasury(self) -> int:
        """Return the kingdom's current gold balance, the sum of every ledger entry."""
        total = 0
        for transaction in self.ledger:
            total = total + transaction.change
        return total

    def research_unit(self, new_unit_type: Unit, research_cost_gold: int) -> UUID:
        """Make a unit template available to muster, paying its research cost.

        Args:
            new_unit_type: The unit to use as a template for future musters.
            research_cost_gold: Gold to spend. Zero or negative values are free.

        Returns:
            The research ID to pass to `muster_unit` or `forget_unit_research`.

        Raises:
            ValueError: If `new_unit_type` is None.
            Kingdom.TreasuryOverdrawError: If the kingdom cannot afford the research.
        """
        if new_unit_type is None:
            raise ValueError("Cannot research null unit type!")
        if research_cost_gold > 0:
            self.add_transaction(f"Researched {new_unit_type.name}.", -research_cost_gold)
        unit_research_id = uuid4()
        self.recruitableUnitTypes[unit_research_id] = new_unit_type
        return unit_research_id

    def forget_unit_research(self, unit_research_id: UUID, research_refund_gold: int) -> bool:
        """Remove a researched unit template, optionally refunding gold.

        Units already mustered from the template are unaffected.

        Args:
            unit_research_id: The ID returned by `research_unit`.
            research_refund_gold: Gold to return to the treasury. Zero or
                negative values give no refund.

        Returns:
            True once the research has been forgotten.

        Raises:
            Kingdom.UnitNotFoundError: If no research exists with that ID.
        """
        if unit_research_id not in self.recruitableUnitTypes.keys():
            raise self.UnitNotFoundError(f"Could not find unit in available units with ID to forget research: {unit_research_id}")
        forgotten_unit = self.recruitableUnitTypes.pop(unit_research_id)
        if research_refund_gold > 0:
            self.add_transaction(f"Refunded research of {forgotten_unit.name} for Kingdom {self.name}.", research_refund_gold)
        return True

    def muster_unit(self, unit_research_id: UUID, muster_cost_gold :int) -> UUID:
        """Raise a new unit from a researched template and add it to the kingdom's armies.

        The new unit is an independent copy of the template, so later changes
        to either one do not affect the other.

        Args:
            unit_research_id: The ID returned by `research_unit`.
            muster_cost_gold: Gold to spend. Must not be negative.

        Returns:
            The army ID of the new unit, for use with `disband_unit`.

        Raises:
            Kingdom.UnitNotFoundError: If no research exists with that ID.
            ValueError: If `muster_cost_gold` is negative.
            Kingdom.TreasuryOverdrawError: If the kingdom cannot afford the unit.
        """
        if unit_research_id not in self.recruitableUnitTypes.keys():
            raise self.UnitNotFoundError(f"Could not find unit in available units with ID to muster: {unit_research_id}")
        if muster_cost_gold < 0:
            raise ValueError(f"Cannot pay a kingdom {self.name} to raise armies; potential infinite money glitch.")
        new_unit_type = self.recruitableUnitTypes[unit_research_id]
        self.add_transaction(f"Mustered a unit of {new_unit_type.name}.", -muster_cost_gold)
        new_unit = clone_unit(new_unit_type)
        new_unit_id = uuid4()
        self.armies[new_unit_id] = new_unit

        return new_unit_id

    def disband_unit(self, army_id: UUID) -> bool:
        """Remove a mustered unit from the kingdom's armies. No gold is refunded.

        Args:
            army_id: The ID returned by `muster_unit`.

        Returns:
            True once the unit has been disbanded.

        Raises:
            Kingdom.UnitNotFoundError: If no army exists with that ID.
        """
        if army_id not in self.armies.keys():
            raise self.UnitNotFoundError(f"Could not find army with ID {army_id} in {self.name}'s mustered armies to disband. Already disbanded?")
        self.armies.pop(army_id)
        return True

    class LedgerEntry:
        """A single transaction in a kingdom's ledger, measured in gold.

        Attributes:
            description: Human-readable reason for the transaction.
            change: Gold added to the treasury. Negative for spending.
        """

        def __init__(self, description: str, goldAdded: int) -> None:
            """Create a ledger entry.

            Args:
                description: Human-readable reason for the transaction.
                goldAdded: Gold added to the treasury. Negative for spending.
            """
            self.description = description
            self.change = goldAdded

    class UnitNotFoundError(Exception):
        """Raised when a research ID or army ID does not belong to this kingdom."""
        pass

    class TreasuryOverdrawError(Exception):
        """Raised when a transaction would drop the treasury below zero."""
        pass
