from uuid import uuid4, UUID

from ..Units.Unit import Unit
from ..Units.UnitFactory import clone_unit


class Kingdom:
    def __init__(self, name, description):
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
        if self.get_treasury() + goldAdded < 0:
            raise self.TreasuryOverdrawError(f"Kingdom {self.name} Cannot afford transaction {description} for {goldAdded}. Current Balance: {self.get_treasury()} ")
        self.ledger.append(Kingdom.LedgerEntry(description, goldAdded))

    def read_ledger(self) -> list["Kingdom.LedgerEntry"]:
        return list(self.ledger)

    def get_treasury(self) -> int:
        total = 0
        for transaction in self.ledger:
            total = total + transaction.change
        return total

    def research_unit(self, new_unit_type: Unit, research_cost_gold: int) -> UUID:
        if new_unit_type is None:
            raise ValueError("Cannot research null unit type!")
        if research_cost_gold > 0:
            self.add_transaction(f"Researched {new_unit_type.name}.", -research_cost_gold)
        unit_research_id = uuid4()
        self.recruitableUnitTypes[unit_research_id] = new_unit_type
        return unit_research_id

    def forget_unit_research(self, unit_research_id: UUID, research_refund_gold: int) -> bool:
        if unit_research_id not in self.recruitableUnitTypes.keys():
            raise self.UnitNotFoundError(f"Could not find unit in available units with ID to forget research: {unit_research_id}")
        forgotten_unit = self.recruitableUnitTypes.pop(unit_research_id)
        if research_refund_gold > 0:
            self.add_transaction(f"Refunded research of {forgotten_unit.name} for Kingdom {self.name}.", research_refund_gold)
        return True

    def muster_unit(self, unit_research_id: UUID, muster_cost_gold :int) -> UUID:
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
        if army_id not in self.armies.keys():
            raise self.UnitNotFoundError(f"Could not find army with ID {army_id} in {self.name}'s mustered armies to disband. Already disbanded?")
        self.armies.pop(army_id)
        return True

    class LedgerEntry:
        def __init__(self, description: str, goldAdded: int) -> None:
            self.description = description
            self.change = goldAdded

    class UnitNotFoundError(Exception):
        pass

    class TreasuryOverdrawError(Exception):
        pass
 