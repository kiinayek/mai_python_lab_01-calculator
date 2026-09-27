
import pytest

from toolkit.__main__ import main


def test_cli_calc_ok():
    code = main(["calc", "2+3*4"])
    assert code == 0

def test_cli_calc_division_by_zero():
    code = main(["calc", "1/0"])
    assert code == 2

def test_cli_calc_empty():
    code = main(["calc", " "])
    assert code == 2

def test_cli_convert_ok():
    code = main(["convert", "1000", "--from", "mm", "--to", "m"])
    assert code == 0

def test_cli_convert_incompatible():
    code = main(["convert", "1", "--from", "kg", "--to", "m"])
    assert code == 2

def test_cli_convert_unknown_unit():
    code = main(["convert", "1", "--from", "xyz", "--to", "m"])
    assert code == 2

def test_cli_help():
    with pytest.raises(SystemExit) as e:
        main(["--help"])
    assert e.value.code == 0