# TODO

- Poisonous Room should have lower priority than other safe nodes.
- If we must travel to a safe unvisited node that must go across Wumpus, just kill it.
- If during the travel, there is a node that can be wumpus then it should be YELLOW
  - If the current node is [S] but know one unkilled Wumpus, but can not detect the YELLOW to be RED.
- During the travel, we priority safe node -> poisonous node / RED -> YELLOW
  - Because with RED node we can just shoot arrow, but YELLOW nodes can be updated later