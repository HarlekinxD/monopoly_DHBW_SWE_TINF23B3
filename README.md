# Monopoly CLI

A text-based Monopoly implementation in Python, built with Clean Architecture in mind.

The game focuses on the core Monopoly loop: roll the dice, move a player, resolve the tile action, and continue with the next turn. The code base is intentionally split into small layers so the rules stay testable, the UI stays simple, and technical details remain isolated from the business logic.

## Project Information

- Developers: Daniel Lohrengel, Vivian Heidt, ~~Tobias Kipping~~
- Instructor: Maurice Müller
- Submission date: 03.05.2026
- Submission: Programmentwurf Monopoly DHBW Karlsruhe

## Highlights

- Command-line interface for playing Monopoly in the terminal
- Clear separation between application logic, domain rules, and infrastructure
- Integer-based money handling to avoid floating-point rounding issues
- JSON persistence for saving and loading games
- Testable ports and use cases for easy maintenance

## Architecture

This project follows Clean Architecture. Dependencies point inward, which means the domain does not depend on the CLI, file system, or random number generation.

```text
Presentation
    -> Application
        -> Domain

Infrastructure implements the interfaces required by Application.
```

### 1. Presentation

The presentation layer contains the CLI entry point and user interaction code. It is responsible for parsing commands, printing the board state, and forwarding player actions into the application layer.

### 2. Application

The application layer contains the use cases of the game. It coordinates game flow and orchestrates the domain model without containing Monopoly rules itself.

It defines ports and interfaces that describe what the application needs from the outside world. These abstractions keep the use cases independent from persistence, randomness, and presentation.

Typical use cases include:

- starting a new game
- playing a turn
- buying a property
- paying rent
- building and selling houses
- drawing chance and community cards
- handling jail actions
- saving and loading a game
- resolving bankruptcy and winner detection

### 3. Domain

The domain layer contains the core Monopoly rules and entities. This is the heart of the game and the most stable part of the system.

It includes concepts such as:

- players
- the board
- tiles and tile types
- properties and ownership
- money and rent logic
- cards and special actions
- jail and turn rules
- houses and hotels

### 4. Infrastructure

The infrastructure layer provides the technical implementations that the application depends on.

Examples in this project:

- JSON game repository for persistence
- in-memory repository implementation for tests and isolated execution
- random number generator adapter
- board factory for assembling the game board
- file and I/O related helpers

## Project Structure

```text
monopoly/
  src/monopoly/
    application/      # Use cases and ports
    domain/           # Game entities and business rules
    infrastructure/   # Persistence, RNG, board setup, I/O
    presentation/     # CLI entry point and user interaction
  tests/              # Unit and integration tests
```

## Game Flow

The software follows the core Monopoly sequence:

1. Roll the dice
2. Move the active player
3. Resolve the tile action
4. Apply any follow-up rules such as rent, jail, or card effects
5. End the turn and continue with the next player

## Design Decisions

- Money is represented as integers only. Monopoly does not require floating-point numbers, and integers prevent rounding problems.
- Use cases are separated from the domain so the rules can be reused and tested without the CLI.
- Ports and interfaces allow fake or in-memory implementations to replace real infrastructure in tests.
- Infrastructure depends on abstractions from the application layer, not the other way around.
- The board and game rules are designed to stay easy to extend and refactor.

## Running the Game

The game requires Python 3.10 or newer.

From the repository root, switch into the Python project directory:

```bash
cd monopoly
```

Then start the game with the included start script:

```bash
./run.sh
```

Alternatively, the game can be started directly with Python:

```bash
python -m monopoly
```

If the package is installed locally, the console entry point can also be used:

```bash
monopoly
```

## Running Tests

```bash
pytest
```

## Intended Audience

This project is a teaching and practice implementation of Monopoly with a focus on software design, domain modeling, and maintainable Python code.
