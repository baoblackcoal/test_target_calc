"""Shared safe calculation engine for CLI and web."""

from __future__ import annotations

import re
from ast import (
    Add,
    BinOp,
    Constant,
    Div,
    Expression,
    Mult,
    Sub,
    UAdd,
    UnaryOp,
    USub,
    parse,
)
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

ALLOWED_INPUT_RE = re.compile(r"^[\d\s+\-*/().]+$")


@dataclass(frozen=True)
class CalculationResult:
    expression: str
    value: Decimal | None = None
    error_code: str | None = None
    error_message: str | None = None

    @property
    def ok(self) -> bool:
        return self.error_code is None

    @property
    def value_text(self) -> str | None:
        if self.value is None:
            return None
        return format_decimal(self.value)


def calculate(expression: str) -> CalculationResult:
    normalized = expression.strip()
    if not normalized:
        return CalculationResult(
            expression=expression,
            error_code="empty_input",
            error_message="Expression cannot be empty.",
        )

    if not ALLOWED_INPUT_RE.fullmatch(expression):
        return CalculationResult(
            expression=expression,
            error_code="unsupported_token",
            error_message="Expression contains unsupported characters.",
        )

    try:
        tree = parse(normalized, mode="eval")
    except SyntaxError:
        return CalculationResult(
            expression=expression,
            error_code="invalid_syntax",
            error_message="Expression syntax is invalid.",
        )

    try:
        value = _evaluate_node(tree)
    except ZeroDivisionError:
        return CalculationResult(
            expression=expression,
            error_code="division_by_zero",
            error_message="Division by zero is not allowed.",
        )
    except ValueError as exc:
        return CalculationResult(
            expression=expression,
            error_code="unsupported_syntax",
            error_message=str(exc),
        )
    except InvalidOperation:
        return CalculationResult(
            expression=expression,
            error_code="invalid_number",
            error_message="Expression contains an invalid number.",
        )

    return CalculationResult(expression=expression, value=value)


def format_decimal(value: Decimal) -> str:
    normalized = value.normalize()
    if normalized == normalized.to_integral():
        return format(normalized.quantize(Decimal("1")), "f")
    return format(normalized, "f").rstrip("0").rstrip(".")


def _evaluate_node(node: Expression | BinOp | UnaryOp | Constant) -> Decimal:
    if isinstance(node, Expression):
        return _evaluate_node(node.body)

    if isinstance(node, Constant):
        if isinstance(node.value, bool) or not isinstance(node.value, int | float):
            raise ValueError("Only numeric arithmetic expressions are supported.")
        return Decimal(str(node.value))

    if isinstance(node, UnaryOp):
        operand = _evaluate_node(node.operand)
        if isinstance(node.op, UAdd):
            return operand
        if isinstance(node.op, USub):
            return -operand
        raise ValueError("Only +, -, *, and / operators are supported.")

    if isinstance(node, BinOp):
        left = _evaluate_node(node.left)
        right = _evaluate_node(node.right)

        if isinstance(node.op, Add):
            return left + right
        if isinstance(node.op, Sub):
            return left - right
        if isinstance(node.op, Mult):
            return left * right
        if isinstance(node.op, Div):
            if right == 0:
                raise ZeroDivisionError
            return left / right
        raise ValueError("Only +, -, *, and / operators are supported.")

    raise ValueError("Only numeric arithmetic expressions are supported.")
