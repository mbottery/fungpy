# io_utils/checkpoint.py

import time
from io_utils.saver import save_to_json
from pathlib import Path

class CheckpointSaver:
    def __init__(self, interval_steps=10, output_dir="checkpoints", filename_pattern="mycel_{step:04d}.json"):
        self.interval_steps = interval_steps
        self.last_step = -1
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.filename_pattern = filename_pattern

    def maybe_save(self, mycel, step):
        if step % self.interval_steps == 0 and step != self.last_step:
            filename = self.output_dir / self.filename_pattern.format(step=step)
            save_to_json(mycel, str(filename))
            self.last_step = step
