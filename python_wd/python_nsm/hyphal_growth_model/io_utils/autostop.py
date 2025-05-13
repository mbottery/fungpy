# io_utils/autostop.py

class AutoStop:
    """Stops simulation if all tips are dead or no longer growing."""
    
    def __init__(self, enabled=True, print_reason=True):
        self.enabled = enabled
        self.print_reason = print_reason

    def check(self, mycel, step):
        if not self.enabled:
            return False
        
        active_tips = mycel.get_tips()
        if len(active_tips) == 0:
            if self.print_reason:
                print(f"🛑 AutoStop triggered: no active tips at step {step}")
            return True
        return False
