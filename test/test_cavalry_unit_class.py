import pytest

from ..KingdomsAndWarfare.Units.Cavalry import Cavalry
from ..KingdomsAndWarfare.Units.Unit import Unit
from ..KingdomsAndWarfare.Units import UnitEnums


def test_cavalry():
    splonks_cavalry = Unit("splonks cavalry", Cavalry, "splonks_cavalry riding rockinghorses.")
    assert splonks_cavalry.name == "splonks cavalry"
    assert splonks_cavalry.experience == UnitEnums.Experience.REGULAR
    assert splonks_cavalry.unit_type == Cavalry


def test_cavalry_level_up():
    teddy_bear_cavalry = Unit("Teddy Bear cavalry", Cavalry, "Teddy Bears riding rockinghorses.")
    teddy_bear_cavalry.attack = 0
    teddy_bear_cavalry.defense = 10
    teddy_bear_cavalry.morale = 0
    teddy_bear_cavalry.command = 0
    assert teddy_bear_cavalry.experience == UnitEnums.Experience.REGULAR
    teddy_bear_cavalry.level_up()
    # assert stats were changed by level up correctly
    # magic numbers provided by table from MCDM K&W page 99
    assert teddy_bear_cavalry.attacks == 1
    assert teddy_bear_cavalry.attack == 1
    assert teddy_bear_cavalry.defense == 11
    assert teddy_bear_cavalry.morale == 1
    assert teddy_bear_cavalry.command == 2
    assert teddy_bear_cavalry.experience == UnitEnums.Experience.VETERAN
    teddy_bear_cavalry.level_up()
    assert teddy_bear_cavalry.attacks == 2
    assert teddy_bear_cavalry.attack == 2
    assert teddy_bear_cavalry.defense == 12
    assert teddy_bear_cavalry.morale == 2
    assert teddy_bear_cavalry.command == 4
    assert teddy_bear_cavalry.experience == UnitEnums.Experience.ELITE
    teddy_bear_cavalry.level_up()
    assert teddy_bear_cavalry.attacks == 2
    assert teddy_bear_cavalry.attack == 3
    assert teddy_bear_cavalry.defense == 13
    assert teddy_bear_cavalry.morale == 3
    assert teddy_bear_cavalry.command == 6
    assert teddy_bear_cavalry.experience == UnitEnums.Experience.SUPER_ELITE


def test_cavalry_upgrade():
    test_cavalry = Unit("Test", Cavalry, "Armed with personality tests.")
    test_cavalry.power = 0
    test_cavalry.toughness = 10
    assert test_cavalry.equipment == UnitEnums.Equipment.LIGHT
    test_cavalry.upgrade()
    assert test_cavalry.equipment == UnitEnums.Equipment.MEDIUM
    assert test_cavalry.power == 1
    assert test_cavalry.toughness == 11
    assert test_cavalry.damage == 1
    test_cavalry.upgrade()
    assert test_cavalry.equipment == UnitEnums.Equipment.HEAVY
    assert test_cavalry.power == 2
    assert test_cavalry.toughness == 12
    assert test_cavalry.damage == 1
    test_cavalry.upgrade()
    assert test_cavalry.equipment == UnitEnums.Equipment.SUPER_HEAVY
    assert test_cavalry.power == 3
    assert test_cavalry.toughness == 13
    assert test_cavalry.damage == 2
