import pytest

from ..KingdomsAndWarfare.Kingdoms.Kingdom import Kingdom
from ..KingdomsAndWarfare.Units.Artillery import Artillery
from ..KingdomsAndWarfare.Units.Unit import Unit


def test_kingdom():
    kingdom_name = "kingdomName"
    kingdom_description = "blah."
    kingdom = Kingdom(kingdom_name, kingdom_description)

    assert kingdom.name == kingdom_name
    assert kingdom.description == kingdom_description


def test_add_transaction():
    kingdom = Kingdom("kingdomName", "blah.")

    kingdom.add_transaction("Taxes", 5)

    assert len(kingdom.ledger) == 1
    entry = kingdom.ledger[0]
    assert isinstance(entry, Kingdom.LedgerEntry)
    assert entry.description == "Taxes"
    assert entry.change == 5


def test_add_transaction_updates_treasury():
    kingdom = Kingdom("kingdomName", "blah.")

    kingdom.add_transaction("Taxes", 5)
    kingdom.add_transaction("Mercenaries", -3)

    assert kingdom.get_treasury() == 2


def test_add_transaction_overdraw():
    kingdom = Kingdom("kingdomName", "blah.")
    kingdom.add_transaction("Taxes", 5)

    with pytest.raises(Kingdom.TreasuryOverdrawError):
        kingdom.add_transaction("Mercenaries", -6)

    # the rejected transaction is not recorded
    assert len(kingdom.get_ledger()) == 1
    assert kingdom.get_treasury() == 5

    # spending exactly the full treasury is allowed
    kingdom.add_transaction("Siege engines", -5)
    assert kingdom.get_treasury() == 0

    with pytest.raises(Kingdom.TreasuryOverdrawError):
        kingdom.add_transaction("Bribes", -1)
    assert kingdom.get_treasury() == 0


def test_get_ledger_empty():
    kingdom = Kingdom("kingdomName", "blah.")

    assert kingdom.get_ledger() == []


def test_get_ledger():
    kingdom = Kingdom("kingdomName", "blah.")
    kingdom.add_transaction("Taxes", 5)
    kingdom.add_transaction("Mercenaries", -3)

    ledger = kingdom.get_ledger()

    assert [(entry.description, entry.change) for entry in ledger] == [
        ("Taxes", 5),
        ("Mercenaries", -3),
    ]


def test_get_ledger_returns_copy():
    kingdom = Kingdom("kingdomName", "blah.")
    kingdom.add_transaction("Taxes", 5)

    ledger = kingdom.get_ledger()
    ledger.clear()

    assert len(kingdom.get_ledger()) == 1


def test_typicalArmyUse():
    kingdom = Kingdom("Muppetville", "A kingdom of felt and fury.")
    machinegun_muppets = Unit("Machinegun Muppets", Artillery, "Muppets manning a machinegun.")
    
    research_id = kingdom.research_unit(machinegun_muppets, 0)
    assert len(kingdom.availableUnits) == 1
    assert kingdom.availableUnits[research_id] == machinegun_muppets

    army_id = kingdom.muster_unit(research_id, 0)
    assert len(kingdom.armies) == 1
    assert kingdom.armies[army_id] == machinegun_muppets
    assert kingdom.armies[army_id] is not machinegun_muppets

    kingdom.disband_unit(army_id)
    assert kingdom.armies == {}

    kingdom.forget_unit_research(research_id, 0)
    assert kingdom.availableUnits == {}
