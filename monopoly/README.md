# Monopoly CLI Version in Python

## Developers
- Daniel Lohrengel
- Vivian Heidt
- ~~Tobias Kipping~~

## Project Goals
This project implements a simple text-based version of Monopoly that can be played via the command-line interface (CLI).

The project is developed in Python using standard libraries. The implementation focuses on the core game mechanics. Complex rules are intentionally simplified in favor of a clean architecture and maintainability.

The software is derived from the official game rules:
1. Rolling the dice
2. Moving the player
3. Executing the field action
4. Transitioning to the next player

Money is represented as integers only, since Monopoly does not require floating-point values and this avoids rounding errors.

## Branch Overview

- **feature/start-game**  
  Initializes a new game, creates players (2–7), and sets up the initial game state.

- **feature/play-turn**  
  Handles the core game loop including dice rolling, player movement, and turn progression.

- **feature/buy-property**  
  Implements the logic for purchasing unowned properties and assigning ownership to players.

- **feature/rent-payment**  
  Calculates and processes rent payments when a player lands on an owned property.

- **feature/cli-menu**  
  Provides the command-line interface for user input, game interaction, and basic navigation.

- **feature/view-toggle**  
  Enables switching between different views, such as board view and ownership view.

- **feature/tests**  
  Contains unit tests for domain logic and application use cases, including mocks and test doubles.

- **refactor/domain-model**  
  Improves and restructures the domain model without changing its external behavior.