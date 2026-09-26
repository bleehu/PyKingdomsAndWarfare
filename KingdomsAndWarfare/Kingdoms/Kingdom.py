from uuid import uuid4, UUID

from ..Units.Unit import Unit
from ..Units.UnitFactory import clone_unit


class Kingdom:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.availableUnits = {}
        self.armies = {}
        self.diplomacy = 0
        self.espionage = 0
        self.lore = 0
        self.operations = 0
        self.communications = 10
        self.resolve = 10
        self.resources = 10
        self.ledger = []

    def add_transaction(self, description: str, goldAdded: int):
        if self.get_treasury() + goldAdded < 0:
            raise self.TreasuryOverdrawError(f"Kingdom {self.name} Cannot afford transaction {description} for {goldAdded}. Current Balance: {self.get_treasury()} ")
        self.ledger.append(Kingdom.LedgerEntry(description, goldAdded))

    def get_ledger(self) -> list["Kingdom.LedgerEntry"]:
        return list(self.ledger)

    def get_treasury(self) -> int:
        total = 0
        for transaction in self.ledger:
            total = total + transaction.change
        return total

    def research_unit(self, new_unit_type: Unit, research_cost_gold: int):
        if new_unit_type is None:
            raise ValueError("Cannot research null unit type!")
        if research_cost_gold > 0:
            self.add_transaction(f"Researched {new_unit_type.name}.", -research_cost_gold)
        new_unit_id = uuid4()
        self.availableUnits[new_unit_id] = new_unit_type
        return new_unit_id

    def forget_unit_research(self, unit_research_id: UUID, research_refund: int):
        if unit_research_id not in self.availableUnits.keys():
            raise self.UnitNotFoundError(f"Could not find unit in available units with ID to forget research: {unit_research_id}")
        forgotten_unit = self.availableUnits.pop(unit_research_id)
        if research_refund > 0:
            self.add_transaction(f"Refunded research of {forgotten_unit.name} for Kingdom {self.name}.", research_refund)
        return True

    def muster_unit(self, unit_type_id: UUID, muster_cost_gold :int):
        if unit_type_id not in self.availableUnits.keys():
            raise self.UnitNotFoundError(f"Could not find unit in available units with ID to muster: {unit_type_id}")
        if muster_cost_gold < 0:
            raise ValueError(f"Cannot pay a kingdom {self.name} to raise armies; potential infinite money glitch.")
        new_unit_type = self.availableUnits[unit_type_id]
        self.add_transaction(f"Mustered a unit of {new_unit_type.name}.", -muster_cost_gold)
        new_unit = clone_unit(new_unit_type)
        new_unit_id = uuid4()
        self.armies[new_unit_id] = new_unit
        
        return new_unit_id

    def disband_unit(self, army_id: UUID):
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
 