import pytest

from ..KingdomsAndWarfare.Units.Aerial import Aerial
from ..KingdomsAndWarfare.Units.Unit import Unit
from ..KingdomsAndWarfare.Units.UnitEnums import Experience as Exp
from ..KingdomsAndWarfare.Units.UnitEnums import Equipment as Eqpmt


def test_aerial():
    splonks_aerial = Unit("splonks aerial", Aerial, "splonks_aerial riding rockinghorses.")
    assert splonks_aerial.name == "splonks aerial"
    assert splonks_aerial.experience == Exp.REGULAR
    assert splonks_aerial.unit_type == Aerial


def test_aerial_level_up():
    teddy_bear_aerial = Unit("Teddy Bear aerial", Aerial, "Teddy Bears riding rockinghorses.")
    teddy_bear_aerial.attack = 0
    teddy_bear_aerial.defense = 10
    teddy_bear_aerial.morale = 0
    teddy_bear_aerial.command = 0
    assert teddy_bear_aerial.experience == Exp.REGULAR
    teddy_bear_aerial.level_up()
    # assert stats were changed by level up correctly
    # magic numbers provided by table from MCDM K&W page 99
    assert teddy_bear_aerial.attacks == 1
    assert teddy_bear_aerial.attack == 1
    assert teddy_bear_aerial.defense == 11
    assert teddy_bear_aerial.morale == 1
    assert teddy_bear_aerial.command == 2
    assert teddy_bear_aerial.experience == Exp.VETERAN
    teddy_bear_aerial.level_up()
    assert teddy_bear_aerial.attacks == 2
    assert teddy_bear_aerial.attack == 2
    assert teddy_bear_aerial.defense == 12
    assert teddy_bear_aerial.morale == 2
    assert teddy_bear_aerial.command == 4
    assert teddy_bear_aerial.experience == Exp.ELITE
    teddy_bear_aerial.level_up()
    assert teddy_bear_aerial.attacks == 2
    assert teddy_bear_aerial.attack == 3
    assert teddy_bear_aerial.defense == 13
    assert teddy_bear_aerial.morale == 3
    assert teddy_bear_aerial.command == 6
    assert teddy_bear_aerial.experience == Exp.SUPER_ELITE


def test_aerial_upgrade():
    test_aerial = Unit("Test", Aerial, "Armed with personality tests.")
    test_aerial.power = 0
    test_aerial.toughness = 10
    assert test_aerial.equipment == Eqpmt.LIGHT
    test_aerial.upgrade()
    assert test_aerial.equipment == Eqpmt.MEDIUM
    assert test_aerial.power == 1
    assert test_aerial.toughness == 11
    assert test_aerial.damage == 1
    test_aerial.upgrade()
    assert test_aerial.equipment == Eqpmt.HEAVY
    assert test_aerial.power == 2
    assert test_aerial.toughness == 12
    assert test_aerial.damage == 1
    test_aerial.upgrade()
    assert test_aerial.equipment == Eqpmt.SUPER_HEAVY
    assert test_aerial.power == 3
    assert test_aerial.toughness == 13
    assert test_aerial.damage == 2


def test_aerial_level_down():
    teddy_bear_aerial = Unit("Ariel", Aerial, "The actual mermaid named Ariel, who can fly now.",
                             experience=Exp.SUPER_ELITE,
                             attacks=2, attack=3, defense=13, morale=3, command=6)
    teddy_bear_aerial.level_down()
    # assert stats were changed by level down correctly
    # magic numbers provided by table from MCDM K&W page 99
    assert teddy_bear_aerial.attacks == 2
    assert teddy_bear_aerial.attack == 2
    assert teddy_bear_aerial.defense == 12
    assert teddy_bear_aerial.morale == 2
    assert teddy_bear_aerial.command == 4
    assert teddy_bear_aerial.experience == Exp.ELITE
    teddy_bear_aerial.level_down()
    assert teddy_bear_aerial.attacks == 1
    assert teddy_bear_aerial.attack == 1
    assert teddy_bear_aerial.defense == 11
    assert teddy_bear_aerial.morale == 1
    assert teddy_bear_aerial.command == 2
    assert teddy_bear_aerial.experience == Exp.VETERAN
    teddy_bear_aerial.level_down()
    assert teddy_bear_aerial.attacks == 1
    assert teddy_bear_aerial.attack == 0
    assert teddy_bear_aerial.defense == 10
    assert teddy_bear_aerial.morale == 0
    assert teddy_bear_aerial.command == 0
    assert teddy_bear_aerial.experience == Exp.REGULAR


def test_aerial_downgrade():
    test_aerial = Unit("Flying Monkeys", Aerial, "Monkeys that remote-control vicious, man-eating flies.",
                       equipment=Eqpmt.SUPER_HEAVY,
                       power=3, toughness=13, damage=2)
    test_aerial.downgrade()
    assert test_aerial.equipment == Eqpmt.HEAVY
    assert test_aerial.power == 2
    assert test_aerial.toughness == 12
    assert test_aerial.damage == 1
    test_aerial.downgrade()
    assert test_aerial.equipment == Eqpmt.MEDIUM
    assert test_aerial.power == 1
    assert test_aerial.toughness == 11
    assert test_aerial.damage == 1
    test_aerial.downgrade()
    assert test_aerial.equipment == Eqpmt.LIGHT
    assert test_aerial.power == 0
    assert test_aerial.toughness == 10
    assert test_aerial.damage == 1
