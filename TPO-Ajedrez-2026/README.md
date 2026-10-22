# Chess TPO — Software Engineering

A small, testable chess implementation built for the Software Engineering course project. The code separates game rules from the console adapter, supports an 8×8 classic setup, validates turns and legal moves, records captures, and detects check. Checkmate is implemented as an additional feature.

## Run

Requires Python 3.10 or newer. The project uses only the Python standard library.

    python jugar.py
    python -m unittest -v

The test suite covers piece movement, blocked paths, turns, captures, check, checkmate, console behavior, configurable board size, and registering a new piece. It currently contains 37 tests.

## Project map

- ajedrez/nucleo/: board, pieces, movement rules, and match state.
- ajedrez/adaptadores/consola.py: terminal input/output.
- tests/: tests that run without a UI or external service.
- docs/diagrama_clases.svg: generated UML view of the current code.
- docs/decisiones-de-diseno.docx: concise design rationale.
- docs/alineacion-con-la-cursada.md: traceability to the assignment and class material.
- docs/presentacion-tpo.pptx: project presentation.

## Scope

The assignment requires six chess pieces, an 8×8 board, alternating turns, captures, rejection of invalid moves, and check detection. This project also implements checkmate. Castling, en passant, promotion, draw rules, AI, undo/redo, and a graphical interface are outside the implemented scope; the assignment lists these as optional extensions.

The king cannot be captured. A game ends through checkmate, so the king remains on the board. This rule is covered by a regression test.

## Course alignment

The implementation reflects the course’s core/adapters separation, inward dependency direction, composition of movement rules, dependency injection at the match setup, and tests of the core without infrastructure. The assignment does not require specific design patterns; the choices are justified in the design note. See the traceability review.

## Privacy and attribution

This public copy omits personal names, group identifiers, private class recordings, transcripts, and teacher slide files. Add group details only in a private submission copy if the course requires them.

## Status

This is a student project and a public study artifact. Its course alignment was checked against the available official assignment and class materials. See the traceability review for source coverage and limitations.
