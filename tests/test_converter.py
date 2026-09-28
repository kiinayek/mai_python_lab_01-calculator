import pytest

from toolkit.converter import convert
from toolkit.errors import (
    AbsoluteZeroError,
    IncompatibleUnitsError,
    UnknownUnitError,
)


# длина - позитивные
def test_mm_to_m():
    assert convert(1000, "mm", "m") == 1.0

def test_m_to_mm():
    assert convert(1, "m", "mm") == 1000.0

def test_cm_to_m():
    assert convert(100, "cm", "m") == 1.0

def test_m_to_cm():
    assert convert(2.5, "m", "cm") == 250.0

def test_km_to_m():
    assert convert(1, "km", "m") == 1000.0

def test_m_to_km():
    assert convert(500, "m", "km") == 0.5

def test_mm_to_cm():
    assert convert(10, "mm", "cm") == 1.0

def test_cm_to_mm():
    assert convert(3, "cm", "mm") == 30.0

def test_km_to_mm():
    assert convert(0.001, "km", "mm") == 1000.0

def test_same_length_unit():
    assert convert(42, "m", "m") == 42.0

def test_length_upper_case():
    assert convert(1000, "MM", "M") == 1.0

def test_length_mixed_case():
    assert convert(10, "Cm", "MM") == 100.0

# масса - позитивные
def test_kg_to_g():
    assert convert(1.5, "kg", "g") == 1500.0

def test_g_to_kg():
    assert convert(2000, "g", "kg") == 2.0

def test_same_mass_unit():
    assert convert(10, "kg", "kg") == 10.0

def test_mass_upper_case():
    assert convert(1, "KG", "G") == 1000.0

def test_small_mass():
    assert convert(0.5, "g", "kg") == 0.0005

# температура - позитивные
def test_c_to_f_zero():
    assert convert(0, "c", "f") == 32.0

def test_f_to_c_freezing():
    assert convert(32, "f", "c") == 0.0

def test_c_to_k_abs_zero():
    assert convert(-273.15, "c", "k") == pytest.approx(0.0, abs=1e-9)

def test_k_to_c_abs_zero():
    assert convert(0, "k", "c") == pytest.approx(-273.15, abs=1e-9)

def test_c_to_k_water():
    assert convert(100, "c", "k") == pytest.approx(373.15, abs=1e-9)

def test_k_to_c_water():
    assert convert(373.15, "k", "c") == pytest.approx(100.0, abs=1e-9)

def test_c_to_f_boiling():
    assert convert(100, "c", "f") == 212.0

def test_f_to_c_boiling():
    assert convert(212, "f", "c") == pytest.approx(100.0, abs=1e-9)

def test_f_to_k():
    assert convert(32, "f", "k") == pytest.approx(273.15, abs=1e-9)

def test_k_to_f():
    assert convert(273.15, "k", "f") == pytest.approx(32.0, abs=1e-9)

def test_same_temp_unit_c():
    assert convert(25, "c", "c") == 25.0

def test_same_temp_unit_k():
    assert convert(300, "k", "k") == 300.0

def test_temp_upper_case():
    assert convert(0, "C", "F") == 32.0

def test_room_temp_c_to_f():
    assert convert(20, "c", "f") == 68.0

# негативные
def test_unknown_from_unit():
    with pytest.raises(UnknownUnitError):
        convert(1, "xyz", "m")

def test_unknown_to_unit():
    with pytest.raises(UnknownUnitError):
        convert(1, "m", "xyz")

def test_unknown_both_units():
    with pytest.raises(UnknownUnitError):
        convert(1, "foo", "bar")

def test_unknown_temp_unit():
    with pytest.raises(UnknownUnitError):
        convert(0, "c", "rankine")

def test_kg_to_m():
    with pytest.raises(IncompatibleUnitsError):
        convert(1, "kg", "m")

def test_m_to_kg():
    with pytest.raises(IncompatibleUnitsError):
        convert(1, "m", "kg")

def test_c_to_m():
    with pytest.raises(IncompatibleUnitsError):
        convert(0, "c", "m")

def test_g_to_cm():
    with pytest.raises(IncompatibleUnitsError):
        convert(10, "g", "cm")

def test_km_to_f():
    with pytest.raises(IncompatibleUnitsError):
        convert(1, "km", "f")

def test_k_to_g():
    with pytest.raises(IncompatibleUnitsError):
        convert(273, "k", "g")

def test_below_abs_zero_c():
    with pytest.raises(AbsoluteZeroError):
        convert(-300, "c", "k")