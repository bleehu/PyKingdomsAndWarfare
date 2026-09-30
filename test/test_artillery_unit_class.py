import pytest

from ..KingdomsAndWarfare.Units.Artillery import Artillery
from ..KingdomsAndWarfare.Units.Unit import Unit
from ..KingdomsAndWarfare.Units import UnitEnums


def test_artillery():
    splonks_artillery = Unit(
        "splonks_artillery artillery", Artillery, "splonks_artillery with bottle rockets"
    )
    assert splonks_artillery.name == "splonks_artillery artillery"
    assert splonks_artillery.experience == UnitEnums.Experience.REGULAR
    assert splonks_artillery.unit_type == Artillery


def test_artillery_level_up():
    teddy_bear_artillery = Unit("Teddy Bear artillery", Artillery, "Teddy Bears with nerf guns.")
    teddy_bear_artillery.attack = 0
    teddy_bear_artillery.defense = 10
    teddy_bear_artillery.morale = 0
    teddy_bear_artillery.command = 0
    assert teddy_bear_artillery.experience == UnitEnums.Experience.REGULAR
    teddy_bear_artillery.level_up()
    # assert stats were changed by level up correctly
    # magic numbers provided by table from MCDM K&W page 99
    assert teddy_bear_artillery.attacks == 2
    assert teddy_bear_artillery.attack == 2
    assert teddy_bear_artillery.defense == 11
    assert teddy_bear_artillery.morale == 1
    assert teddy_bear_artillery.command == 1
    assert teddy_bear_artillery.experience == UnitEnums.Experience.VETERAN
    teddy_bear_artillery.level_up()
    assert teddy_bear_artillery.attacks == 2
    assert teddy_bear_artillery.attack == 4
    assert teddy_bear_artillery.defense == 12
    assert teddy_bear_artillery.morale == 2
    assert teddy_bear_artillery.command == 2
    assert teddy_bear_artillery.experience == UnitEnums.Experience.ELITE
    teddy_bear_artillery.level_up()
    assert teddy_bear_artillery.attacks == 2
    assert teddy_bear_artillery.attack == 6
    assert teddy_bear_artillery.defense == 13
    assert teddy_bear_artillery.morale == 3
    assert teddy_bear_artillery.command == 3
    assert teddy_bear_artillery.experience == UnitEnums.Experience.SUPER_ELITE


def test_artillery_upgrade():
    test_artillery = Unit("Test", Artillery, "Armed with personality tests.")
    test_artillery.power = 0
    test_artillery.toughness = 10
    assert test_artillery.equipment == UnitEnums.Equipment.LIGHT
    test_artillery.upgrade()
    assert test_artillery.equipment == UnitEnums.Equipment.MEDIUM
    assert test_artillery.power == 1
    assert test_artillery.toughness == 11
    test_artillery.upgrade()
    assert test_artillery.equipment == UnitEnums.Equipment.HEAVY
    assert test_artillery.power == 2
    assert test_artillery.toughness == 12
    test_artillery.upgrade()
    assert test_artillery.equipment == UnitEnums.Equipment.SUPER_HEAVY
    assert test_artillery.power == 3
    assert test_artillery.toughness == 13


def test_artillery_level_down():
    cory_artillery = Unit("Cory Doctorow's Raygun Brigade", Artillery, "Nerds whose sci-fi shooters keep getting enshitified over time.",
                                experience=UnitEnums.Experience.SUPER_ELITE,
                                attacks=2, attack=6, defense=13, morale=3, command=3)
    cory_artillery.level_down()
    # assert stats were changed by level down correctly
    # magic numbers provided by table from MCDM K&W page 99
    assert cory_artillery.attacks == 2
    assert cory_artillery.attack == 4
    assert cory_artillery.defense == 12
    assert cory_artillery.morale == 2
    assert cory_artillery.command == 2
    assert cory_artillery.experience == UnitEnums.Experience.ELITE
    cory_artillery.level_down()
    assert cory_artillery.attacks == 2
    assert cory_artillery.attack == 2
    assert cory_artillery.defense == 11
    assert cory_artillery.morale == 1
    assert cory_artillery.command == 1
    assert cory_artillery.experience == UnitEnums.Experience.VETERAN
    cory_artillery.level_down()
    assert cory_artillery.attacks == 1
    assert cory_artillery.attack == 0
    assert cory_artillery.defense == 10
    assert cory_artillery.morale == 0
    assert cory_artillery.command == 0
    assert cory_artillery.experience == UnitEnums.Experience.REGULAR


def test_artillery_downgrade():
    test_artillery = Unit("Art Tillery", Artillery, "Over-caffienated painters throwing paintings of tilled earth.",
                          equipment=UnitEnums.Equipment.SUPER_HEAVY,
                          power=3, toughness=13, damage=1)
    test_artillery.downgrade()
    assert test_artillery.equipment == UnitEnums.Equipment.HEAVY
    assert test_artillery.power == 2
    assert test_artillery.toughness == 12
    assert test_artillery.damage == 1
    test_artillery.downgrade()
    assert test_artillery.equipment == UnitEnums.Equipment.MEDIUM
    assert test_artillery.power == 1
    assert test_artillery.toughness == 11
    assert test_artillery.damage == 1
    test_artillery.downgrade()
    assert test_artillery.equipment == UnitEnums.Equipment.LIGHT
    assert test_artillery.power == 0
    assert test_artillery.toughness == 10
    assert test_artillery.damage == 1
