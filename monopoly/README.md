
# Monopoly CLI-Version in Python 
== Devs: 
Devs: 
- Daniel Lohrengel
- Vivian Heidt
- ~~Tobias Kipping~~
@@ -8,7 +8,7 @@

## Projektgoals: 

This Project implements a simple text based version of monopoly, which can be played on the command line interface(CLI).  
The Project has been developed using the Python programming language using standard libraries.
Implementation is focused on the core game mechanics.
Complexe rules have been simplified in favor of a clean Architecture.
@@ -22,8 +22,7 @@ The Software infers from the offical rule set:
3. Executing field actions
4. transitioning to another player

Money is in the scope of this project an integer, 
Since there are no floats used in Monopoly and to prevent rounding errors.

##Branch Overview

feature/start-game
Initializes a new game, creates players (2–7), and sets up the initial game state.

feature/play-turn
Handles the core game loop including dice rolling, player movement, and turn progression.

feature/buy-property
Implements the logic for purchasing unowned properties and assigning ownership to players.

feature/rent-payment
Calculates and processes rent payments when a player lands on an owned property.

feature/cli-menu
Provides the command-line interface for user input, game interaction, and basic navigation.

feature/view-toggle
Enables switching between different views (e.g., board view and ownership view).

feature/tests
Contains unit tests for domain logic and application use cases, including mocks and test doubles.

refactor/domain-model
Improves and restructures the domain model without changing its external behavior.