"""
Undo/Redo functionality for CompPy
Tracks parameter changes and allows reverting
"""

class UndoRedoManager:
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []
        self.max_stack_size = 50
        
    def push_state(self, state):
        """
        Push a new state onto the undo stack
        state: dict containing {stage_idx, field_name, old_value, new_value}
        """
        self.undo_stack.append(state)
        if len(self.undo_stack) > self.max_stack_size:
            self.undo_stack.pop(0)
        # Clear redo stack when new change is made
        self.redo_stack.clear()
        
    def can_undo(self):
        return len(self.undo_stack) > 0
        
    def can_redo(self):
        return len(self.redo_stack) > 0
        
    def undo(self):
        if not self.can_undo():
            return None
        state = self.undo_stack.pop()
        self.redo_stack.append(state)
        return state
        
    def redo(self):
        if not self.can_redo():
            return None
        state = self.redo_stack.pop()
        self.undo_stack.append(state)
        return state
        
    def clear(self):
        self.undo_stack.clear()
        self.redo_stack.clear()
