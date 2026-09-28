import pytest

from toolkit.calculator import calculate
from toolkit.errors import (
    ConsecutiveOperatorsError,
    DivisionByZeroError,
    EmptyExpressionError,
    InvalidCharacterError,
    MissingOperandError,
    MissingOperatorError,
    TooManyDotsError,
)


# позитивные тесты
def test_simple_add():
    assert calculate("2+7") == 9

def test_unary_and_add():
    assert calculate("-3.5 + -15") == -18.5

def test_double_minus():
    assert calculate("-100.1 -- 67") == pytest.approx(-33.1)

def test_subtract():
    assert calculate("67 - 78") == -11

def test_unary_mul():
    assert calculate("-1 *78.9") == pytest.approx(-78.9)

def test_priority_with_unary():
    assert calculate("-5 +-3*15") == -50

def test_div_negative():
    assert calculate("15 /-3") == -5.0

def test_div_ints():
    assert calculate("15 / 3") == 5.0

def test_floor_div_ints():
    assert calculate("5 // 3") == 1

def test_mod_ints():
    assert calculate("45 % 9") == 0

def test_parens_complex():
    assert calculate("(2+-7)*(-10//5)") == 10

def test_long_expression():
    assert calculate("(10*-10)/(5*-5)*4") == 16

def test_spaces():
    assert calculate("10 + 2 * 3") == 16

def test_only_unary_number():
    assert calculate("-42") == -42

def test_nested_parens():
    assert calculate("((2+3)*4)") == 20

# негативные
def test_floor_div_float_error():
    with pytest.raises((InvalidCharacterError, MissingOperatorError)):
        calculate("15.7//2.1")

def test_mod_float_error():
    with pytest.raises((InvalidCharacterError, MissingOperatorError)):
        calculate("76.9 % 52")

def test_division_by_zero():
    with pytest.raises(DivisionByZeroError):
        calculate("100 / 0")

def test_empty_expression():
    with pytest.raises(EmptyExpressionError):
        calculate(" ")

def test_empty_string():
    with pytest.raises(EmptyExpressionError):
        calculate("")

def test_invalid_letter():
    with pytest.raises(InvalidCharacterError):
        calculate("54 +-a")

def test_two_dots_in_number():
    with pytest.raises(TooManyDotsError):
        calculate("2.2.0 +-18 ")

def test_two_nums_without_operator():
    with pytest.raises(MissingOperandError):
        calculate("5 6")

def test_consecutive_operators():
    with pytest.raises(ConsecutiveOperatorsError):
        calculate("72 */ 10")

def test_trailing_operator():
    with pytest.raises(MissingOperandError):
        calculate("2+")

def test_leading_mul():
    with pytest.raises((MissingOperandError, 
                       ConsecutiveOperatorsError,
                       InvalidCharacterError)):
        calculate("*5")

def test_unbalanced_paren():
    with pytest.raises((MissingOperandError, InvalidCharacterError)):
        calculate("(2+3")

def test_empty_parens():
    with pytest.raises(InvalidCharacterError):
        calculate("()")