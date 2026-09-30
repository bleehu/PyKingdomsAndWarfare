import pytest

from ..KingdomsAndWarfare.Traits.Trait import Trait
from ..KingdomsAndWarfare.Units.Aerial import Aerial
from ..KingdomsAndWarfare.Units.Artillery import Artillery
from ..KingdomsAndWarfare.Units.Cavalry import Cavalry
from ..KingdomsAndWarfare.Units.Infantry import Infantry
from ..KingdomsAndWarfare.Units.Unit import Unit
from ..KingdomsAndWarfare.Units.UnitFactory import clone_unit
from ..KingdomsAndWarfare.Units import UnitEnums


@pytest.mark.parametrize("unit_type", [Infantry, Cavalry, Artillery, Aerial])
@pytest.mark.parametrize("experience", list(UnitEnums.Experience))
@pytest.mark.parametrize("equipment", list(UnitEnums.Equipment))
def test_clone_unit(unit_type, experience, equipment):
    original = Unit("Goblin Wolf Riders", unit_type, "Goblins riding very good dogs.",
                    ancestry="Goblin",
                    experience=experience,
                    equipment=equipment,
                    tier=UnitEnums.Tier.III,
                    size=8, attacks=2, damage=2,
                    attack=3, defense=14, power=4, toughness=13,
                    morale=2, command=5,
                    traits=[Trait("Pack Tactics", "Good boys hunt together.")])
    original.casualties = 5

    clone = clone_unit(original)

    # the clone has identical stats but is a separate object
    assert clone == original
    assert clone is not original
    assert clone.unit_type == unit_type
    assert clone.experience == experience
    assert clone.equipment == equipment
    assert clone.battles == Unit.battles_from_xp(experience)
    assert clone.casualties == 5

    # the clone gets its own traits list, so adding a trait doesn't affect the original
    assert clone.traits is not original.traits
    clone.add_trait(Trait("Rabid", "Not such good dogs after all."))
    assert len(clone.traits) == 2
    assert len(original.traits) == 1

    # changes to the clone don't affect the original
    clone.attack = 7
    clone.casualties = 1
    clone.experience = UnitEnums.Experience.LEVIES
    assert original.attack == 3
    assert original.casualties == 5
    assert original.experience == experience
