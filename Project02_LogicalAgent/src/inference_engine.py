# inference_engine.py


class InferenceEngine:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base

    def infer_safe_moves(self, position):
        # Infer which moves are safe based on current knowledge
        x, y = position
        moves = []
        if self.kb.query(~self.kb.encode("P", x + 1, y)):
            moves.append((x + 1, y))
        if self.kb.query(~self.kb.encode("P", x - 1, y)):
            moves.append((x - 1, y))
        if self.kb.query(~self.kb.encode("P", x, y + 1)):
            moves.append((x, y + 1))
        if self.kb.query(~self.kb.encode("P", x, y - 1)):
            moves.append((x, y - 1))
        return moves
