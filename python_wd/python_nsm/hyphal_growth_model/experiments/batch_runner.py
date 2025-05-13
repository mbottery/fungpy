# batch_runner.py

import sys
import os
import json
import csv
import shutil
from datetime import datetime

from multiprocessing import Pool
from functools import partial

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import simulate
from config.sim_config import Options


def load_config(config_path):
    with open(config_path, "r") as f:
        return json.load(f)


def run_batch(config_path):
    batch_config = load_config(config_path)

    batch_name = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    batch_folder = os.path.join("batch_outputs", batch_name)
    os.makedirs(batch_folder, exist_ok=True)
    print(f"📦 Launching batch: {batch_name}")

    shutil.copy(config_path, os.path.join(batch_folder, "batch_config_used.json"))
    print(f"🗄 Saved batch config to {batch_folder}/batch_config_used.json")

    summary_data = []

    for i, run_cfg in enumerate(batch_config["runs"]):
        run_name = run_cfg.get("name", f"run_{i+1}")
        opts = Options(**run_cfg["options"])
        steps = run_cfg.get("steps", 120)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sim_folder_name = f"{run_name}_{i+1:03d}_{timestamp}"
        output_dir = os.path.join(batch_folder, sim_folder_name)
        os.makedirs(output_dir, exist_ok=True)

        print(f"▶️ Running: {run_name} (#{i+1}) → {output_dir}")

        try:
            os.environ["BATCH_OUTPUT_DIR"] = output_dir
            simulate(opts, steps)

            summary_data.append({
                "run_name": run_name,
                "steps": steps,
                "status": "✅ Success",
                "output_dir": output_dir
            })

        except Exception as e:
            print(f"❌ Error in {run_name}: {e}")
            summary_data.append({
                "run_name": run_name,
                "steps": steps,
                "status": f"❌ Failed: {e}",
                "output_dir": output_dir
            })

    summary_file = os.path.join(batch_folder, "batch_summary.csv")
    with open(summary_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=summary_data[0].keys())
        writer.writeheader()
        writer.writerows(summary_data)

    print(f"\n✅ All simulations complete. Summary saved to {summary_file}")


# 🆕 PARALLEL BATCH RUNNER
def worker(run_cfg, batch_folder):
    run_name = run_cfg.get("name", "unnamed")
    opts = Options(**run_cfg["options"])
    steps = run_cfg.get("steps", 120)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sim_folder_name = f"{run_name}_{timestamp}"
    output_dir = os.path.join(batch_folder, sim_folder_name)
    os.makedirs(output_dir, exist_ok=True)

    os.environ["BATCH_OUTPUT_DIR"] = output_dir

    try:
        print(f"▶️ [Worker] Running: {run_name} → {output_dir}")
        simulate(opts, steps)
        return {
            "run_name": run_name,
            "steps": steps,
            "status": "✅ Success",
            "output_dir": output_dir
        }
    except Exception as e:
        print(f"❌ Error in {run_name}: {e}")
        return {
            "run_name": run_name,
            "steps": steps,
            "status": f"❌ Failed: {e}",
            "output_dir": output_dir
        }


def run_batch_parallel(config_path):
    num_cores = os.cpu_count()
    processes = max(1, num_cores - 1)
    print(f"🖥️ Detected {num_cores} cores; using {processes} workers.")

    batch_config = load_config(config_path)

    batch_name = f"batch_parallel_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    batch_folder = os.path.join("batch_outputs", batch_name)
    os.makedirs(batch_folder, exist_ok=True)
    print(f"📦 Launching parallel batch: {batch_name}")

    shutil.copy(config_path, os.path.join(batch_folder, "batch_config_used.json"))
    print(f"🗄 Saved batch config to {batch_folder}/batch_config_used.json")

    with Pool(processes=processes) as pool:
        results = pool.map(partial(worker, batch_folder=batch_folder), batch_config["runs"])

    # Save batch summary
    summary_file = os.path.join(batch_folder, "batch_summary.csv")
    with open(summary_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"\n✅ All simulations complete. Summary saved to {summary_file}")


if __name__ == "__main__":
    config_path = "config/batch_config.json"
    # To use parallel: uncomment below and comment out run_batch
    run_batch_parallel(config_path)
    # run_batch(config_path)