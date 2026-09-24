class ConversationMemory:

    def __init__(self, max_turns=5):
        self.history = []
        self.max_turns = max_turns

    def add_turn(self, user_message, assistant_message):
        self.history.append({
            "user": user_message,
            "assistant": assistant_message
        })

        # Keep only the most recent conversations
        if len(self.history) > self.max_turns:
            self.history.pop(0)

    def get_history(self):
        return self.history

    def clear(self):
        self.history = []