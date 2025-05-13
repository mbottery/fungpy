# control/runtime_mutator.py

class Mutation:
    """Defines a single parameter change scheduled at a given step."""
    def __init__(self, step: int, option: str, value):
        """
        Args:
            step: When to apply this mutation
            option: Name of the option in the Options object
            value: New value or a function(old_value) -> new_value
        """
        self.step = step
        self.option = option
        self.value = value

class RuntimeMutator:
    """Applies scheduled parameter mutations during simulation."""
    
    def __init__(self):
        self.mutations = []

    def schedule(self, step: int, option: str, value):
        """Add a mutation to change 'option' at 'step'."""
        self.mutations.append(Mutation(step, option, value))

    def apply(self, step: int, options):
        """Check and apply all mutations at this step."""
        for mut in self.mutations:
            if mut.step == step:
                current = getattr(options, mut.option, None)
                new_value = mut.value(current) if callable(mut.value) else mut.value
                setattr(options, mut.option, new_value)
                print(f"🔧 Mutation at step {step}: {mut.option} changed from {current} → {new_value}")
