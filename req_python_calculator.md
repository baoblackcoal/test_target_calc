# Python Calculator Product Requirements Document

## 1. Document Overview

- Document title: Python Calculator PRD
- Document file: `req_python_calculator.md`
- Product stage: V1
- Product type: Minimal utility product
- Goal: Deliver a Python calculator that supports non-interactive CLI, interactive CLI, and a Web UI at the same time, based on one shared calculation engine, with CI and a manual-release CD pipeline.

## 2. Goal Decomposition

### 2.1 Top-Level Goal

Build a Python calculator product that:

- Supports non-interactive CLI execution
- Supports interactive CLI REPL execution
- Supports a lightweight enhanced single-page Web interface
- Uses one shared safe expression engine
- Includes basic quality gates and a manual-release CI/CD pipeline

### 2.2 Business Value

- Provide one simple calculator tool for local usage and browser usage
- Keep logic consistent across CLI and Web
- Reduce maintenance cost by sharing one calculation core
- Enable sustainable delivery through test automation and release automation

### 2.3 Success Criteria

The product is considered successful when all of the following are true:

- Users can input expressions in CLI non-interactive mode and get correct results
- Users can continuously calculate in CLI interactive mode without restarting the program
- Users can calculate through a Web page and view session history
- CLI and Web return the same result and error behavior for the same valid or invalid input
- No arbitrary Python code execution is allowed
- CI runs automatically on code changes
- Release pipeline can manually publish both Python package/source artifacts and Web service artifacts

## 3. Target Users

### 3.1 Primary Users

- Developers who need quick command-line calculations
- Students who need a simple calculator for local learning
- General users who prefer a browser input page

### 3.2 Typical Scenarios

- Run one expression in terminal and print one result
- Open a REPL and calculate several expressions in sequence
- Open a Web page, calculate several expressions, and review recent session history

## 4. Product Positioning

### 4.1 Positioning Choice

This product is positioned as a minimal utility product.

### 4.2 Positioning Implications

- Prioritize simple scope and stable delivery
- Prefer low-complexity architecture
- Avoid advanced math functions in V1
- Focus on core usability, consistency, and reliability

## 5. Product Scope

### 5.1 In Scope

- Safe arithmetic expression calculation
- Basic operators: `+`, `-`, `*`, `/`
- Parentheses and operator precedence
- CLI non-interactive mode
- CLI interactive REPL mode
- Single-page Web UI
- Session history in Web UI
- Shared calculation engine
- Unit tests and basic integration tests
- CI pipeline
- Manual-release CD pipeline
- Release targets for both Python package/source artifacts and Web service artifacts

### 5.2 Out of Scope

- Scientific functions such as `sin`, `cos`, `sqrt`, `log`
- Variables and assignment
- Persistent cross-session history
- User accounts
- Multi-page Web application
- Automatic production deployment after merge
- Arbitrary Python expression execution
- Plugin system or extension marketplace

## 6. Functional Requirements

### 6.1 Shared Calculation Engine

The product must contain one independent calculation core used by both CLI and Web.

Requirements:

- Accept numeric arithmetic expressions only
- Support `+`, `-`, `*`, `/`
- Support parentheses
- Respect normal operator precedence
- Reject unsupported syntax
- Return consistent results for the same input in all entry points
- Return structured errors for invalid expressions

### 6.2 Safety Rules

The engine must use safe expression parsing only.

Requirements:

- Do not execute arbitrary Python code
- Do not expose built-in functions or modules
- Only allow safe arithmetic tokens and grammar required by V1
- Reject suspicious or unsupported input with explicit error messages

### 6.3 CLI Non-Interactive Mode

The product must support one-shot command execution.

Requirements:

- User can pass one expression through command arguments or equivalent supported input method
- Program returns the calculation result once and exits
- Invalid input returns clear error output and non-success exit behavior
- Help usage must be available

Example scenario:

- Input: `calc "1 + 2 * 3"`
- Output: `7`

### 6.4 CLI Interactive Mode

The product must support REPL mode.

Requirements:

- User can launch an interactive session
- User can repeatedly input expressions and receive results
- Invalid expressions do not crash the session
- User can exit the session through a clear exit command or standard termination behavior
- Prompt and help text should be simple and explicit

### 6.5 Web UI

The product must provide an enhanced single-page Web interface.

Requirements:

- One input area for expression entry
- One calculate action trigger
- One result display area
- Clear error feedback for invalid expressions
- Session history displayed on the page

Session history rules:

- Show expressions and corresponding results from the current session
- History is not required to persist after page reload or server restart unless implementation chooses to keep it in current session memory
- History display order should prioritize recent entries

### 6.6 Consistency Requirement

For the same expression:

- CLI non-interactive mode, CLI interactive mode, and Web UI must use the same engine
- Result format should be consistent
- Error wording style should be consistent enough for user understanding

## 7. User Experience Requirements

### 7.1 CLI Experience

- Commands must be simple to discover
- Help text must explain both non-interactive and interactive modes
- Error messages must state why input failed
- REPL prompt should clearly indicate readiness for input

### 7.2 Web Experience

- Page should load quickly
- Layout should be simple and readable
- Error feedback should appear near the result area or input area
- History should be easy to scan

### 7.3 Usability Principle

V1 should optimize for:

- Fast start
- Low learning cost
- Predictable results

## 8. Technical Requirements

### 8.1 Architecture

Recommended layers:

- Calculation core
- CLI interface layer
- Web interface layer
- Test layer
- CI/CD configuration layer

Architecture principle:

- Business logic must not be duplicated between CLI and Web

### 8.2 Web Framework Strategy

Use a lightweight Web framework.

Rationale:

- Fits minimal utility positioning
- Keeps implementation cost low
- Supports quick testing and release

### 8.3 Error Handling

- Invalid syntax must not crash the process
- Division by zero must return explicit failure information
- CLI and Web should surface user-facing error messages
- Internal exceptions should be controlled and testable

## 9. Quality Requirements

### 9.1 Quality Level

V1 quality target is basic quality gate.

### 9.2 Required Test Coverage Scope

Must include:

- Core calculation unit tests
- CLI basic behavior tests
- Web basic page or endpoint tests
- Main error scenarios

Main error scenarios include:

- Empty input
- Invalid expression syntax
- Unsupported characters or tokens
- Division by zero

### 9.3 Minimum Acceptance Quality

- Main happy paths pass
- Main failure paths pass
- No known security hole caused by direct expression execution

## 10. CI Requirements

### 10.1 CI Objective

Automatically validate code quality on code changes.

### 10.2 Minimum CI Flow

CI must automatically perform:

- Dependency installation
- Code format check
- Test execution

Optional but recommended if the stack supports it cleanly:

- Lint
- Type checking

### 10.3 CI Gate

- Changes should not be considered releasable unless CI passes

## 11. CD and Release Requirements

### 11.1 Release Strategy

V1 requires CI plus release pipeline.

### 11.2 Trigger Strategy

Release must be manually triggered.

Reason:

- Better control for V1
- Lower accidental release risk
- Matches minimal utility phase

### 11.3 Release Targets

The manual-release pipeline must support both:

- Python package/source artifact release
- Web service artifact release

### 11.4 Release Expectations

Python release target:

- Produce installable or distributable package/source artifacts

Web release target:

- Produce a deployable Web service artifact or equivalent deliverable defined by the implementation

## 12. Acceptance Criteria

### 12.1 CLI Non-Interactive Acceptance

- Given a valid arithmetic expression, the command returns the correct result and exits successfully
- Given an invalid expression, the command returns a clear error and exits with failure semantics

### 12.2 CLI Interactive Acceptance

- User can start REPL successfully
- User can enter multiple valid expressions in sequence
- User receives correct result after each valid expression
- Invalid input does not terminate the REPL unexpectedly

### 12.3 Web Acceptance

- User can open the page
- User can enter a valid expression and get the correct result
- User can enter an invalid expression and receive a clear error
- User can see session history after multiple calculations

### 12.4 Consistency Acceptance

- For the same valid input, CLI and Web show the same numerical result
- For the same invalid input, CLI and Web both reject it

### 12.5 CI Acceptance

- CI automatically runs on code changes
- CI fails when tests or checks fail
- CI passes when required checks pass

### 12.6 Release Acceptance

- Manual trigger can start the release pipeline
- Python artifact release can be produced
- Web release artifact can be produced

## 13. Milestone Breakdown

### 13.1 Milestone 1: Core Definition

- Define expression grammar
- Define result and error model
- Confirm CLI and Web shared engine contract

### 13.2 Milestone 2: Core Implementation

- Implement safe parser/evaluator
- Implement error handling
- Add unit tests

### 13.3 Milestone 3: CLI Delivery

- Implement non-interactive mode
- Implement interactive REPL mode
- Add CLI tests

### 13.4 Milestone 4: Web Delivery

- Implement single-page interface
- Add result area and error handling
- Add session history
- Add Web tests

### 13.5 Milestone 5: CI/CD Delivery

- Add formatting and test automation
- Add CI workflow
- Add manual-release workflow
- Validate both release targets

## 14. Execution Checklist

- Define supported expression grammar
- Define CLI command format
- Define REPL input and exit behavior
- Define Web page fields and history display
- Implement shared core
- Implement CLI adapters
- Implement Web adapter
- Write tests
- Configure CI
- Configure manual-release pipeline
- Validate acceptance criteria

## 15. Risks and Constraints

### 15.1 Main Risks

- Unsafe expression parsing introduces code execution risk
- CLI and Web may diverge if logic is duplicated
- Release scope may expand too early because both Python and Web artifacts are required

### 15.2 Control Measures

- Enforce one shared engine
- Keep V1 grammar minimal
- Use manual release instead of automatic deployment
- Test core logic before interface layers

## 16. Final Requirement Summary

V1 must deliver a minimal Python calculator product with:

- Safe arithmetic calculation
- CLI non-interactive mode
- CLI interactive REPL mode
- Enhanced single-page Web UI with session history
- Shared core logic
- Basic testing quality gate
- Automatic CI
- Manual-release pipeline for both Python artifacts and Web release artifacts
