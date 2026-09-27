from uuid import uuid4

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
    kingdom = Kingdom("Digcrafter's Crater", "Pickaxe-weilding monarch's network of mines and villages.")
    assert kingdom.get_treasury() == 0

    kingdom.add_transaction("Diamond Miner's taxes", 5)
    assert kingdom.get_treasury() == 5

    kingdom.add_transaction("Upgrade spider rider's bows with gold arrows", -3)
    assert kingdom.get_treasury() == 2


def test_add_transaction_overdraw():
    kingdom = Kingdom("kingdomName", "blah.")
    kingdom.add_transaction("Taxes", 5)

    with pytest.raises(Kingdom.TreasuryOverdrawError):
        kingdom.add_transaction("Mercenaries", -6)

    # the rejected transaction is not recorded
    assert len(kingdom.read_ledger()) == 1
    assert kingdom.get_treasury() == 5

    # spending exactly the full treasury is allowed
    kingdom.add_transaction("Siege engines", -5)
    assert kingdom.get_treasury() == 0

    with pytest.raises(Kingdom.TreasuryOverdrawError):
        kingdom.add_transaction("Bribes", -1)
    assert kingdom.get_treasury() == 0
    #transactions that fail due to overdraft don't modify the ledger; they're idempotent
    assert len(kingdom.read_ledger()) == 2


def test_read_ledger_empty():
    kingdom = Kingdom("kingdomName", "blah.")

    assert kingdom.read_ledger() == []


def test_read_ledger():
    kingdom = Kingdom("kingdomName", "blah.")
    assert kingdom.read_ledger() == []
    kingdom.add_transaction("Taxes", 5)
    kingdom.add_transaction("Mercenaries", -3)

    ledger = kingdom.read_ledger()

    assert [(entry.description, entry.change) for entry in ledger] == [
        ("Taxes", 5),
        ("Mercenaries", -3),
    ]


def test_read_ledger_returns_copy():
    kingdom = Kingdom("kingdomName", "blah.")
    kingdom.add_transaction("Taxes", 5)

    ledger = kingdom.read_ledger()
    ledger.clear()

    assert len(kingdom.read_ledger()) == 1


def test_typicalArmyUse():
    kingdom = Kingdom("Muppetville", "A fiefdom of felt and fury.")
    machinegun_muppets = Unit("Machinegun Muppets", Artillery, "Muppets manning a machinegun.")
    
    research_id = kingdom.research_unit(machinegun_muppets, 0)
    assert len(kingdom.recruitableUnitTypes) == 1
    assert kingdom.recruitableUnitTypes[research_id] == machinegun_muppets

    army_id = kingdom.muster_unit(research_id, 0)
    assert len(kingdom.armies) == 1
    assert kingdom.armies[army_id] == machinegun_muppets
    assert kingdom.armies[army_id] is not machinegun_muppets

    kingdom.disband_unit(army_id)
    assert kingdom.armies == {}

    kingdom.forget_unit_research(research_id, 0)
    assert kingdom.recruitableUnitTypes == {}


def test_research_unit():
    kingdom = Kingdom("Muppetville", "A fiefdom of felt and fury.")
    kingdom.add_transaction("Taxes", 10)
    machinegun_muppets = Unit("Machinegun Muppets", Artillery, "Muppets manning a machinegun.")

    research_id = kingdom.research_unit(machinegun_muppets, 4)

    assert kingdom.recruitableUnitTypes == {research_id: machinegun_muppets}
    assert kingdom.get_treasury() == 6
    assert kingdom.read_ledger()[-1].description == "Researched Machinegun Muppets."
    assert kingdom.read_ledger()[-1].change == -4

    # free research doesn't add a ledger entry, and each research gets a unique id
    second_id = kingdom.research_unit(machinegun_muppets, 0)
    assert second_id != research_id
    assert len(kingdom.recruitableUnitTypes) == 2
    assert len(kingdom.read_ledger()) == 2


def test_research_unit_errors():
    kingdom = Kingdom("Muppetville", "A fiefdom of felt and fury.")
    machinegun_muppets = Unit("Machinegun Muppets", Artillery, "Muppets manning a machinegun.")

    with pytest.raises(ValueError):
        kingdom.research_unit(None, 0)
    with pytest.raises(Kingdom.TreasuryOverdrawError):
        kingdom.research_unit(machinegun_muppets, 1)

    assert kingdom.recruitableUnitTypes == {}


def test_forget_unit_research():
    kingdom = Kingdom("Muppetville", "A fiefdom of felt and fury.")
    kingdom.add_transaction("Taxes", 10)
    machinegun_muppets = Unit("Machinegun Muppets", Artillery, "Muppets manning a machinegun.")
    research_id = kingdom.research_unit(machinegun_muppets, 4)

    assert kingdom.forget_unit_research(research_id, 3) is True

    assert kingdom.recruitableUnitTypes == {}
    assert kingdom.get_treasury() == 9
    assert kingdom.read_ledger()[-1].change == 3

    # forgetting research twice is an error
    with pytest.raises(Kingdom.UnitNotFoundError):
        kingdom.forget_unit_research(research_id, 0)


def test_muster_unit():
    kingdom = Kingdom("Muppetville", "A fiefdom of felt and fury.")
    kingdom.add_transaction("Taxes", 10)
    machinegun_muppets = Unit("Machinegun Muppets", Artillery, "Muppets manning a machinegun.")
    research_id = kingdom.research_unit(machinegun_muppets, 0)

    first_army_id = kingdom.muster_unit(research_id, 3)
    second_army_id = kingdom.muster_unit(research_id, 3)

    assert first_army_id != second_army_id
    assert len(kingdom.armies) == 2
    assert kingdom.get_treasury() == 4
    assert kingdom.read_ledger()[-1].description == "Mustered a unit of Machinegun Muppets."
    # each mustered army is a separate copy of the researched unit
    assert kingdom.armies[first_army_id] == machinegun_muppets
    assert kingdom.armies[first_army_id] is not machinegun_muppets
    assert kingdom.armies[first_army_id] is not kingdom.armies[second_army_id]


def test_muster_unit_errors():
    kingdom = Kingdom("Muppetville", "A fiefdom of felt and fury.")
    kingdom.add_transaction("Taxes", 2)
    machinegun_muppets = Unit("Machinegun Muppets", Artillery, "Muppets manning a machinegun.")
    research_id = kingdom.research_unit(machinegun_muppets, 0)

    with pytest.raises(Kingdom.UnitNotFoundError):
        kingdom.muster_unit(uuid4(), 0)
    with pytest.raises(ValueError):
        kingdom.muster_unit(research_id, -1)
    with pytest.raises(Kingdom.TreasuryOverdrawError):
        kingdom.muster_unit(research_id, 3)

    assert kingdom.armies == {}
    assert kingdom.get_treasury() == 2


def test_disband_unit():
    kingdom = Kingdom("Muppetville", "A fiefdom of felt and fury.")
    machinegun_muppets = Unit("Machinegun Muppets", Artillery, "Muppets manning a machinegun.")
    research_id = kingdom.research_unit(machinegun_muppets, 0)
    first_army_id = kingdom.muster_unit(research_id, 0)
    second_army_id = kingdom.muster_unit(research_id, 0)

    assert kingdom.disband_unit(first_army_id) is True

    assert list(kingdom.armies.keys()) == [second_army_id]
    # disbanding doesn't forget the research
    assert research_id in kingdom.recruitableUnitTypes

    # disbanding twice is an error
    with pytest.raises(Kingdom.UnitNotFoundError):
        kingdom.disband_unit(first_army_id)
