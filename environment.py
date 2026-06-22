import difflib
from errors import UndefinedVariable

class Environment:
    def __init__(self, parent=None):
        self.values = {}
        self.parent = parent

    def get(self, name, line=7):
        """Retrieve variable value from the current scope or parent scopes.
        Raises UndefinedVariable if not found."""
        if name in self.values:
            return self.values[name]
        if self.parent is not None:
            return self.parent.get(name, line)
        
        # Variable not found, search for a similar name
        suggestion = self.similar_name(name)
        raise UndefinedVariable(name, suggestion=suggestion, line=line)

    def set(self, name, value):
        """Update an existing variable in the current or outer scope.
        If it does not exist, define it in the current local scope."""
        if name in self.values:
            self.values[name] = value
        elif self.parent is not None and self.parent.has(name):
            self.parent.set(name, value)
        else:
            self.values[name] = value

    def define(self, name, value):
        """Define a new variable in the local scope."""
        self.values[name] = value

    def has(self, name):
        """Check if a variable exists in this scope or parent scopes."""
        if name in self.values:
            return True
        if self.parent is not None:
            return self.parent.has(name)
        return False

    def get_all_names(self):
        """Retrieve all variable names available in this and parent scopes."""
        names = set(self.values.keys())
        if self.parent is not None:
            names.update(self.parent.get_all_names())
        return names

    def similar_name(self, name):
        """Find the closest matching variable name in scope using difflib."""
        all_names = self.get_all_names()
        matches = difflib.get_close_matches(name, all_names, n=1, cutoff=0.6)
        return matches[0] if matches else None
