# Course alignment and source review

## Conclusion

The project follows the official TPO’s required scope and the engineering guidance visible in the available course material. The clearest correctness defect found during review was that a rook could capture the opposing king. That behavior has been blocked in legal-move generation, move execution, and checkmate move search, and is covered by a regression test. The suite now has 37 passing tests.

The project uses course concepts as design tools. The assignment does not mandate particular patterns, and the class material cautions against adding a pattern without a reason. This review therefore checks behavior and justification instead of treating a named pattern as a requirement.

## Official assignment

Source: TPO_Ingenieria de Software_Dominio Ajedrez.docx (available in the course folder; not copied into this public repository).

Required by the assignment:

- An 8×8 board and the six standard piece types with their movement rules.
- Alternating turns, captures, rejection of invalid moves, and check detection.
- A framework-independent core, unit tests that run without external infrastructure, and a UML diagram that matches the implementation.
- A short design rationale that answers what the choice is, why it was made, and when it could fail or become a poor fit.
- A group presentation and an individual defense. The group must have 3–5 members.

Listed as optional: checkmate, castling, en passant, promotion, draws, AI, undo/redo, and a graphical interface beyond the minimal console. The implementation includes checkmate, but it does not claim the other optional rules.

## Traceability to classes

The dates below refer to the available class decks/notes. The public repository does not redistribute course slides or transcripts; filenames and slide references are provided for traceability.

- **6 Aug — Unit 1, “Ingeniería y Diseño,” slides 10–18.** The deck introduces core/adapters separation, dependency direction, hexagonal architecture, and testability. The project keeps game rules in ajedrez/nucleo/ and terminal interaction in ajedrez/adaptadores/consola.py.
- **13 Aug — class notes, “Clase 2 13-08-26.”** The notes continue the architecture discussion. The implementation keeps I/O out of Partida, so tests can call rules directly.
- **20 Aug — Unit 1, “SOLID, Dependency Injection y Composition,” slides 2, 9–10, 18.** The course discusses SOLID, constructor injection, composition, and choosing patterns only when they solve a real problem. Partida receives an optional Disposicion and CatalogoDePiezas; each Pieza composes movement behaviors. The catalog enables an added piece without changing the existing piece classes. These are design choices, not assignment-mandated patterns.
- **27 Aug — Unit 1, “Patrones y Testing,” slides 12, 15–17.** Command/State are presented as tools, and undo is an optional chess extension. This implementation does not add undo solely to demonstrate a pattern.
- **10 Sep — Unit 1, “Testing, TDD y TPO,” slides 5–9 and 15–20.** The course material supports testing the core without infrastructure, AAA/TDD, and testing chess rules such as rook movement. The king-capture regression was added test-first: it failed because a8 was returned as a legal rook destination, then passed after the rule was fixed.
- **17 Sep — Unit 0.1, “Tipos de Arquitectura…,” slides 3 and 5–10; class note “Clase 6 17-09-2026.”** The available note records the instructor comparing UML with code and asking for tests by module. The included UML is generated from the current project classes and the test suite is organized by behavior. The recording/transcript coverage for that date is incomplete, so this statement is limited to the note and deck.
- **15 Oct — Unit 5 AI bonus.** The available code is explicitly bonus material. AI is not a required core feature and is excluded from this repository; the assignment’s optional AI mention does not make that bonus mandatory.

The course material also mentions using a simulation/copy to check whether a move leaves the current player in check. Partida._deja_en_jaque copies the board, applies the proposed move to the copy, then checks the king’s safety. The course discussion is treated as support for the design, not as a requirement to use this exact implementation.

## Defect found and correction

Before the fix, Partida.movimientos_legales could include a square occupied by the opposing king. Partida.mover then allowed the capture and removed the king, which contradicted the intended check/checkmate model.

The code now filters king captures from legal moves, excludes them when searching for any remaining move, and rejects direct attempts to execute one. A dedicated test asserts that the move is absent, execution raises MovimientoInvalido, the king remains on the board, and turn/history do not change. Checkmate continues to work through es_jaque_mate.

Verification: python -m unittest -v — 37 tests pass on the reviewed copy.

## Design choices worth defending

- **Core and console adapter:** keeps rules usable from tests or another interface. It becomes less useful if the application remains a tiny one-off console tool with no need for isolation.
- **Movement composition:** each piece combines movement behaviors. It becomes harder to read if many pieces require unique interactions that cannot be expressed cleanly as composed rules.
- **Destinations versus attacks:** pawn movement and pawn attacks differ, so the model exposes both. A future variant with unusual pawn rules may need a richer rules object.
- **Piece catalog:** maps names to factories and supports extension. It becomes needless indirection if the game permanently supports only a fixed set and extension is not a real requirement.
- **Injectable setup and board dimensions:** allow alternate positions and sizes, which also makes tests and the individual defense easier. They add cost if every game is guaranteed to use one fixed board and setup.
- **Board-copy safety check:** checks a candidate move without corrupting the real state. It may become expensive if the game grows; an incremental attack model could then be justified.
- **Immutable positions and pieces:** make value objects safer to share. They may be unnecessary if the model evolves toward frequent in-place edits or a different performance profile.

The expanded what/why/when-break explanation is in decisiones-de-diseno.docx.

## Scope boundary and items not claimed

There is no claim that castling, en passant, promotion, draw rules, AI, undo/redo, or a GUI are implemented. Their omission is consistent with the assignment’s optional list. The bonus AI code supplied with the class is not included in this project.

## Evidence limits

The audit used the official assignment, available class decks, notes, source code, and tests in the local course folder. Some recordings did not have a corresponding transcript, and the available transcript for at least one class was incomplete or noisy. The review therefore cannot claim to have verified every spoken sentence from every recording. The class-date mapping above states only what could be tied to available notes/decks. The quoted prior audit itself was not found as a standalone file; the project and cited source materials were located independently.

## Public-copy boundary

This repository excludes personal names, email addresses, group number, local Windows paths, course files, recordings, transcripts, and supplied bonus code. The official assignment requires group identity in the submission context; add the real group roster to a private course-submission copy after the group confirms it. No group member names are published here.
