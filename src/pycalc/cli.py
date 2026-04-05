"""CLI entry point for pycalc."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from pycalc.engine import calculate

EXIT_COMMANDS = {"exit", "quit", ":q"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="calc",
        description="Evaluate arithmetic expressions, start a REPL, or launch the web UI.",
    )
    parser.add_argument("expression", nargs="?", help="Expression to evaluate once and exit.")
    parser.add_argument(
        "--repl",
        action="store_true",
        help="Start an interactive session for repeated calculations.",
    )
    parser.add_argument(
        "--web",
        action="store_true",
        help="Run the Flask web calculator.",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host interface for web mode. Default: 127.0.0.1.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port for web mode. Default: 5000.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.web and args.repl:
        parser.error("--web cannot be used together with --repl.")

    if args.web and args.expression is not None:
        parser.error("expression cannot be provided together with --web.")

    if args.web:
        return run_web_server(host=args.host, port=args.port)

    if args.repl:
        return run_repl()

    if args.expression is None:
        parser.print_help(sys.stderr)
        return 2

    result = calculate(args.expression)
    if result.ok:
        print(result.value_text)
        return 0

    print(result.error_message, file=sys.stderr)
    return 1


def run_repl() -> int:
    print("pycalc REPL. Enter an arithmetic expression. Type 'exit' to quit.")
    while True:
        try:
            raw = input("calc> ")
        except EOFError:
            print()
            return 0
        except KeyboardInterrupt:
            print("\nSession terminated.")
            return 0

        if raw.strip().lower() in EXIT_COMMANDS:
            print("Bye.")
            return 0

        result = calculate(raw)
        if result.ok:
            print(result.value_text)
        else:
            print(result.error_message)


def run_web_server(host: str, port: int) -> int:
    from pycalc.web.app import create_app

    create_app().run(host=host, port=port, debug=False, use_reloader=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
