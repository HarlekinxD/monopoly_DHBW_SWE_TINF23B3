import pytest

from monopoly.domain.value_objects.money import Money


def test_money_adds_correctly() -> None:
    assert Money(100).add(Money(50)) == Money(150)


def test_money_subtracts_correctly() -> None:
    assert Money(100).subtract(Money(40)) == Money(60)


def test_money_cannot_be_negative() -> None:
    with pytest.raises(ValueError):
        Money(-1)