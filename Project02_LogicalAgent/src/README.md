# Project Implementation for Wumpus World Logical Agent

To implement the Wumpus World problem using a Hybrid Logic-Based Agent, we will structure the project to align with the requirements and optimize for clarity and functionality. Here's a breakdown of the proposed structure and code:

## 1. Project Structure

``` graphql
WumpusWorld/
│
├── src/
│   ├── main.py                 # Entry point for the project
│   ├── program.py              # Contains the Program class to manage the game map
│   ├── agent.py                # Contains the Agent class implementing logic
│   ├── knowledge_base.py       # Manages propositional and first-order logic knowledge
│   ├── inference_engine.py     # Performs logical inference based on the knowledge base
│   ├── environment.py          # Simulates the Wumpus World environment
│   └── utilities.py            # Utility functions (e.g., for reading inputs, logging)
│
├── input/
│   ├── map1.txt                # Example input file for the map layout
│   └── ...                     # Additional map files
│
├── output/
│   ├── result1.txt             # Output file for the result of simulation
│   └── ...                     # Additional result files
│
└── docs/
    ├── report.pdf              # Report document detailing the project
    └── ...                     # Additional documentation files
```

## 2. Core Components

- Main.py: The main entry point of the application, orchestrating the initialization and execution of the agent and environment.

- Program Class (program.py): This class initializes and manages the game map, updates percepts based on the agent's actions, and provides information to the agent.

- Agent Class (agent.py): Implements the decision-making logic, using both propositional and first-order logic to navigate the Wumpus World and achieve objectives.

- Knowledge Base (knowledge_base.py): Stores and manages logical rules and facts, using PySAT or similar libraries for propositional logic, and potentially other tools for FOL.

- Inference Engine (inference_engine.py): Responsible for deriving new knowledge from the existing knowledge base using logical inference techniques.

- Environment (environment.py): Simulates the Wumpus World, including grid layout, entity placement (Wumpus, pits, gold), and updating the world state based on the agent's actions.

- Utilities (utilities.py): Includes helper functions for reading input files, logging actions and results, and other common tasks.


To synthesize and present logical information in the form of **Propositional Logic** or **First-Order Logic (FOL)** for the Wumpus World, we can use a combination of the given information and advanced prompting techniques to structure the logical expressions. This will involve defining propositions or predicates to represent the various elements and states within the environment, as well as the agent's knowledge and actions.

### **Propositional Logic Representation**

In Propositional Logic, we use propositions to denote specific facts about the environment:

1. **Pits and Breezes**:
   - \( P(x, y) \): There is a pit in cell \((x, y)\).
   - \( B(x, y) \): There is a breeze in cell \((x, y)\).
   - **Rule**: \( B(x, y) \leftrightarrow (P(x+1, y) \lor P(x-1, y) \lor P(x, y+1) \lor P(x, y-1)) \)
     - This rule indicates that a breeze in a cell \((x, y)\) implies that there is a pit in one of the adjacent cells.

2. **Wumpus and Stench**:
   - \( W(x, y) \): There is a Wumpus in cell \((x, y)\).
   - \( S(x, y) \): There is a stench in cell \((x, y)\).
   - **Rule**: \( S(x, y) \leftrightarrow (W(x+1, y) \lor W(x-1, y) \lor W(x, y+1) \lor W(x, y-1)) \)
     - A stench in a cell \((x, y)\) indicates the presence of a Wumpus in an adjacent cell.

3. **Gold and Glow**:
   - \( G(x, y) \): There is gold in cell \((x, y)\).
   - \( GL(x, y) \): There is a glow in cell \((x, y)\).
   - **Rule**: \( GL(x, y) \leftrightarrow (G(x+1, y) \lor G(x-1, y) \lor G(x, y+1) \lor G(x, y-1)) \)
     - A glow indicates that there is gold in an adjacent cell.

4. **Poisonous Gas and Whiff**:
   - \( PG(x, y) \): There is poisonous gas in cell \((x, y)\).
   - \( WF(x, y) \): There is a whiff in cell \((x, y)\).
   - **Rule**: \( WF(x, y) \leftrightarrow (PG(x+1, y) \lor PG(x-1, y) \lor PG(x, y+1) \lor PG(x, y-1)) \)
     - A whiff indicates the presence of poisonous gas in an adjacent cell.

### **First-Order Logic Representation**

In First-Order Logic, we can use predicates and quantifiers to express more complex relationships:

1. **Pits and Breezes**:
   - \( \text{Pit}(x, y) \): There is a pit in cell \((x, y)\).
   - \( \text{Breeze}(x, y) \): There is a breeze in cell \((x, y)\).
   - **Rule**: \( \forall x, y \, (\text{Breeze}(x, y) \leftrightarrow \exists x', y' \, ( \text{Adjacent}(x, y, x', y') \land \text{Pit}(x', y'))) \)
     - This rule states that a breeze in \((x, y)\) is caused by a pit in an adjacent cell \((x', y')\).

2. **Wumpus and Stench**:
   - \( \text{Wumpus}(x, y) \): There is a Wumpus in cell \((x, y)\).
   - \( \text{Stench}(x, y) \): There is a stench in cell \((x, y)\).
   - **Rule**: \( \forall x, y \, (\text{Stench}(x, y) \leftrightarrow \exists x', y' \, ( \text{Adjacent}(x, y, x', y') \land \text{Wumpus}(x', y'))) \)
     - A stench in \((x, y)\) indicates a Wumpus in an adjacent cell.

3. **Gold and Glow**:
   - \( \text{Gold}(x, y) \): There is gold in cell \((x, y)\).
   - \( \text{Glow}(x, y) \): There is a glow in cell \((x, y)\).
   - **Rule**: \( \forall x, y \, (\text{Glow}(x, y) \leftrightarrow \exists x', y' \, ( \text{Adjacent}(x, y, x', y') \land \text{Gold}(x', y'))) \)
     - A glow indicates the presence of gold in an adjacent cell.

4. **Poisonous Gas and Whiff**:
   - \( \text{PoisonGas}(x, y) \): There is poisonous gas in cell \((x, y)\).
   - \( \text{Whiff}(x, y) \): There is a whiff in cell \((x, y)\).
   - **Rule**: \( \forall x, y \, (\text{Whiff}(x, y) \leftrightarrow \exists x', y' \, ( \text{Adjacent}(x, y, x', y') \land \text{PoisonGas}(x', y'))) \)
     - A whiff indicates poisonous gas in an adjacent cell.

### **Additional Considerations**
- The **agent's knowledge base** must be updated dynamically as new percepts are received.
- **Inference rules** can be applied to deduce the presence or absence of hazards based on the percepts.
- **Search strategies** such as **forward reasoning** and **backward chaining** can be used to navigate the environment and achieve the goal of finding gold while avoiding hazards.

These logical representations can be implemented using **logic programming libraries** like PySAT or specialized tools for knowledge representation and reasoning. This structured approach will aid in the agent's decision-making process, allowing it to infer the safest paths and actions to take based on the available percepts and learned knowledge.

``` python

    if knowledge_base.query(knowledge_base.encode(Percept.BREEZE, 0, 0)):
        print("Breeze at (0, 0) is consistent with the knowledge base.")

    knowledge_base.add_fact([knowledge_base.encode(Percept.BREEZE, 0, 0)])
    if knowledge_base.query(knowledge_base.encode(Percept.BREEZE, 0, 0)):
        print("Breeze at (0, 0) is consistent with the knowledge base.")

    knowledge_base.infer_new_knowledge()

    if knowledge_base.query(knowledge_base.encode(Percept.BREEZE, 0, 0)):
        print("Breeze at (0, 0) is consistent with the knowledge base.")
    # Correct
```

