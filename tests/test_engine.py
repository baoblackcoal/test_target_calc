from pycalc.engine import calculate


def test_calculates_operator_precedence() -> None:
    result = calculate("1 + 2 * 3")
    assert result.ok is True
    assert result.value_text == "7"


def test_calculates_parentheses_and_decimal_output() -> None:
    result = calculate("(1 + 2) / 4")
    assert result.ok is True
    assert result.value_text == "0.75"


def test_supports_unary_minus() -> None:
    result = calculate("-3 + 5")
    assert result.ok is True
    assert result.value_text == "2"


def test_rejects_empty_input() -> None:
    result = calculate("   ")
    assert result.ok is False
    assert result.error_code == "empty_input"


def test_rejects_invalid_syntax() -> None:
    result = calculate("1 + * 2")
    assert result.ok is False
    assert result.error_code == "invalid_syntax"


def test_rejects_unsupported_characters() -> None:
    result = calculate("__import__('os').system('calc')")
    assert result.ok is False
    assert result.error_code == "unsupported_token"


def test_rejects_unsupported_syntax_even_if_characters_look_safe() -> None:
    result = calculate("1 // 2")
    assert result.ok is False
    assert result.error_code == "unsupported_syntax"


def test_rejects_division_by_zero() -> None:
    result = calculate("10 / 0")
    assert result.ok is False
    assert result.error_code == "division_by_zero"
