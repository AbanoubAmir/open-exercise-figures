"""Render the exercise library: one figures/<external_id>.json per exercise.

    python3 build.py                       # every exercise's animation into out/library/
    python3 build.py --ids 0031,0043       # only these
    python3 build.py --muscle-group chest --sheet out/chest.png   # key poses only, for review
    python3 build.py --missing             # list exercises without a figure yet

The highlighted muscle comes from the exercise's target in the data file, so
figure files only describe movement and equipment.
"""

import argparse
import json
from multiprocessing import Pool
from pathlib import Path

import render

DATA = render.ROOT / "exercises.json"


def exercises(path=DATA):
    """The app's data file has external_id; the published library's exercises.json calls it id."""
    rows = json.loads(Path(path).read_text())
    for e in rows:
        e.setdefault("external_id", e.get("id"))
    return rows


def figure_path(ex):
    return render.ROOT / "figures" / f"{ex['external_id']}.json"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", help="comma-separated external ids")
    ap.add_argument("--muscle-group", help="only exercises in this muscle_group")
    ap.add_argument("--target", help="only exercises with this target muscle")
    ap.add_argument("--sheet", help="write a contact sheet of the key poses instead of animations")
    ap.add_argument("--missing", action="store_true", help="list exercises with no figure file")
    ap.add_argument("--check", action="store_true", help="validate only, render nothing")
    ap.add_argument("--data", type=Path, default=DATA, help="exercise list (JSON array with external_id or id, and target)")
    ap.add_argument("--out", type=Path, default=render.ROOT / "out" / "library", help="where animations go")
    args = ap.parse_args()

    chosen = exercises(args.data)
    if args.ids:
        wanted = set(args.ids.split(","))
        chosen = [e for e in chosen if e["external_id"] in wanted]
    if args.muscle_group:
        chosen = [e for e in chosen if e["muscle_group"] == args.muscle_group]
    if args.target:
        chosen = [e for e in chosen if e["target"] == args.target]

    if args.missing:
        missing = [e for e in chosen if not figure_path(e).exists()]
        for e in missing:
            print(f"{e['external_id']}\t{e['name']}\t{e['equipment']}")
        print(f"{len(missing)} of {len(chosen)} missing")
        return

    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    jobs, failures = [], 0
    for e in chosen:
        path = figure_path(e)
        if not path.exists():
            continue
        try:
            fig = render.load(path)
        except Exception as err:  # bad JSON or a broken extends chain
            print(f"{path.name}: {err}")
            failures += 1
            continue
        fig["muscles"] = [e["target"]]
        issues = render.problems(fig)
        for issue in issues:
            print(f"{path.name} ({e['name']}): {issue}")
        failures += bool(issues)
        jobs.append((e, fig))
    if args.check:
        print(f"checked {len(jobs)}, {failures} with problems")
        return
    if args.sheet:
        # Key poses only: fast enough to review while authoring.
        entries = [(f"{e['external_id']} {e['name'][:40]}", render.render(fig, only_keys=True)) for e, fig in jobs]
        if entries:
            render.contact_sheet(entries, Path(args.sheet))
        print(f"sheet of {len(entries)}, {failures} with problems")
        return
    with Pool() as pool:
        pool.starmap(write_animation, [(fig, out / f"{e['external_id']}.webp") for e, fig in jobs])
    print(f"rendered {len(jobs)} into {out}, {failures} with problems")


def write_animation(fig, path):
    render.save(render.render(fig), path)

if __name__ == "__main__":
    main()
