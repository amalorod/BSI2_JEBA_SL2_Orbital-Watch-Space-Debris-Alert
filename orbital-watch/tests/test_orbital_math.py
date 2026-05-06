from src.orbital_math import dms_to_decimal


def test_dms_to_decimal_north():
    assert dms_to_decimal("11°37'44N") == 11.628889


def test_dms_to_decimal_west():
    assert dms_to_decimal("145°50'21W") == -145.839167


def test_dms_to_decimal_south():
    assert dms_to_decimal("12°30'00S") == -12.5


def test_dms_to_decimal_exact_zero_seconds():
    assert dms_to_decimal("74°00'00W") == -74.0


def test_dms_to_decimal_east():
    assert dms_to_decimal("120°45'30E") == 120.758333


def test_dms_to_decimal_small_value():
    assert dms_to_decimal("00°00'01N") == 0.000278