# Open Exercise Figures

Animated figures for 1,399 gym and home exercises, with a name, description and step-by-step instructions for each in English and Egyptian Arabic. Everything is free to use for any purpose, including commercial apps, with no credit needed.

Made for the [Fitness Connect](https://github.com/EmammMuhammed/Fitness-Connect) app and shared so nobody else has to rebuild it.

## What is here

| Path | What it is |
| --- | --- |
| `animations/<id>.webp` | A looping animated WebP per exercise, 400×400, about 30 to 80 KB. The target muscle is highlighted. |
| `exercises.json` | One entry per exercise: name, category, difficulty, muscle group, target and secondary muscles, equipment, description and instructions, each in English and Arabic (`_ar`), plus the paths to its animation and figure file. |
| `figures/<id>.json` | The source of each animation: a few key poses of a simple mannequin and the equipment around it. |
| `templates/` | Shared movements that figure files build on. |
| `render.py`, `build.py` | The renderer (Python 3 and Pillow) that turns figure files into animations. |
| `AUTHORING.md` | How figure files work, for changing or adding exercises. |

An entry in `exercises.json`:

```json
{
 "id": "0001",
 "name": "3/4 sit-up",
 "name_ar": "...",
 "muscle_group": "waist",
 "target": "abs",
 "equipment": "body weight",
 "instructions": ["...", "..."],
 "instructions_ar": ["...", "..."],
 "animation": "animations/0001.webp",
 "figure": "figures/0001.json"
}
```

## Using the animations

Load them straight from this repository through jsDelivr, pinned to a commit so they never change under you:

```
https://cdn.jsdelivr.net/gh/AbanoubAmir/open-exercise-figures@<commit>/animations/0001.webp
```

Or copy the files into your own app or storage.

## Changing or adding exercises

```
pip install pillow
python3 build.py --ids 0001 --sheet check.png   # key poses, side by side, to review
python3 build.py --check                        # validate every figure
python3 build.py --out animations               # render everything
```

To add an exercise, add an entry to `exercises.json` and a `figures/<id>.json`, then render. `AUTHORING.md` explains the angles, placement and equipment.

## Where this came from

Every figure was drawn by our own code from poses written for this project: nothing was traced or copied from photos, videos, other figures or other exercise datasets. The descriptions and instructions were written fresh in our own words. Exercise names are the common names of the movements.

Known limits: the mannequin is simple, so twists, grips (palms up or down), and some sideways arm movements seen from the side are approximate. Pull requests are welcome.

## License

You may use, copy, change, share and sell any of this, for any purpose, without asking and without giving credit.

- Animations, figure files, templates and exercise text: [CC0 1.0](LICENSE-CC0.txt), dedicated to the public domain.
- Code (`render.py`, `build.py`): [MIT No Attribution](LICENSE-MIT-0.txt).
