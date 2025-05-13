# config/sim_config.py

import json
from core.options import Options
from argparse import ArgumentParser

def load_options_from_json(path: str) -> Options:
    with open(path, "r") as f:
        data = json.load(f)
    return Options(**data)

def load_options_from_cli() -> Options:
    parser = ArgumentParser(description="Run hyphal growth simulation with custom parameters.")
    parser.add_argument("--config", type=str, help="Path to JSON config file")
    parser.add_argument("--steps", type=int, help="Override number of simulation steps")
    args = parser.parse_args()

    if args.config:
        opts = load_options_from_json(args.config)
    else:
        opts = Options()  # defaults

    return opts, args.steps
