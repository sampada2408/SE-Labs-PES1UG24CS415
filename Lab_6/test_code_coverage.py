import pytest
from calculator import classify_number, final_price, grade


def test_classify_all_paths():
    assert classify_number(5) == "positive"
    assert classify_number(-5) == "negative"
    assert classify_number(0) == "zero"


def test_final_price_member_bulk():
    assert final_price(100, 10, True) == 855.0


def test_final_price_invalid():
    with pytest.raises(ValueError):
        final_price(-1, 1, False)


def test_grade_all_levels():
    assert grade(95) == "A"
    assert grade(80) == "B"
    assert grade(60) == "C"
    assert grade(10) == "F"


def test_grade_invalid():
    with pytest.raises(ValueError):
        grade(101)