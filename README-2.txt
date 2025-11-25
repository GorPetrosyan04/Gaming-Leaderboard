COMP 282 – Project: Gaming Leaderboard
Author: Gor Petrosyan
Date: November 5, 2025


Node and Link Design:
---------------------
Each player and score are represented using linked structures:

- ScoreNode
  - value (int): player’s score
  - next (reference): next most-recent score

- Player
  - name (string): player’s name (no spaces, no quotes)
  - best (int or None): highest score so far
  - head (ScoreNode): head of linked list of scores (most recent first)
  - next (Player): next player in the registry

Players are stored in a singly linked list registry, and each player’s score history is a linked list of ScoreNodes.

Invariant: Every player name is unique, and each player’s history is stored most-recent-first.


Vector and Heap Design:
-----------------------
- Vector: Custom dynamic array with manual 2× growth.
  Provides push_back, get, set, and swap. Used for leaderboard snapshots only (does not change player data).
- Heap Sort: Custom max-heap built on the Vector.
  Orders players by best (descending), breaking ties by name (ascending).
  Players with no scores appear at the end (best = NONE).


How to Run:
-----------
> python3 main.py commands.txt
If the file is missing or cannot be opened:
USAGE: python3 main.py <commands_file>


Commands Implemented:
---------------------
ADD_PLAYER name        - Adds a new player. Prints DUPLICATE if name already exists.
ADD_SCORE name score   - Adds an integer score to player’s history; updates best if higher.
CURRENT name           - Shows the player’s most recent and best scores.
BEST name              - Displays only the player’s best score.
HISTORY name k         - Prints up to the last k scores, most-recent first.
TOP_K k                - Displays top k players by best score using heap sort.
PRINT_ALL              - Shows all players sorted by best (descending), name (ascending).
REMOVE_PLAYER name     - Removes the player and all scores.
LEN                    - Prints number of players currently registered.
CLEAR                  - Deletes all players and histories.
QUIT                   - Terminates immediately.


Data-Structure Summary:
-----------------------
- Linked List for player registry and score history (O(1) add, O(k) traversal).
- Vector for dynamic snapshots and heap operations.
- Heap Sort for ranked output (O(p log p)).
- All data structures are self-implemented—no Python built-ins such as list, dict, or set.


Notes:
------
- Player names contain no spaces or quotes (use underscores if needed).
- Scores must be integers; invalid input prints ERROR: ... .
- Commands are case-insensitive; arguments are case-sensitive.
- Players with no scores appear last with best=NONE.
- Player histories are never modified during sorting.
