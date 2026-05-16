from __future__ import annotations

import argparse

from libs.common.workflow import IncidentWorkflow


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("scenario_path")
    parser.add_argument("output_dir")
    args = parser.parse_args()
    IncidentWorkflow().run(args.scenario_path, args.output_dir)
    print(f"Generated incident artifacts in {args.output_dir}")


if __name__ == "__main__":
    main()

