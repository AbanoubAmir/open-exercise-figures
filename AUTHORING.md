# Exercise figures

Animated figures for every exercise in the Fitness Connect library, drawn by our own code from a few key poses per exercise. Nothing here is traced or copied from photos, videos or other datasets.

- `render.py` draws a figure file to a looping animated WebP (Python 3 and Pillow).
- `build.py` renders the whole library: one `figures/<external_id>.json` per exercise in `../data/shared_exercises_ar.json`, written to `out/library/<external_id>.webp`. The highlighted muscle comes from the exercise's `target`.
- `templates/` holds shared movements that figures extend.

```
python3 build.py --missing                               # what still needs a figure
python3 build.py --ids 0031,0043 --sheet out/check.png   # key poses of some, side by side, for review
python3 build.py --check                                 # validate everything without rendering
python3 render.py templates/barbell-curl.json            # render loose files into out/
```

## Figure files

A figure is a mannequin seen from the side (facing right) or from the front, a list of key poses, and the equipment around it. The animation eases from each pose to the next, holds briefly, and loops back to the first. The first pose is also the still image shown in lists, so make it the clear start position.

```json
{
  "view": "side",
  "anchor": ["nearAnkle", [0, 0.09]],
  "equipment": [{ "type": "barbell" }],
  "poses": [
    { "torso": 0, "arms": [178, 172], "legs": [180, 180, 95] },
    { "torso": -3, "arms": [172, 25], "legs": [180, 180, 95] }
  ]
}
```

### Angles

Every angle is the absolute direction a body segment points, in degrees, measured in the picture:

- `0` points up.
- `90` points the way the figure faces (to the right in side view; to the figure's own side, outward, in front view).
- `180` points down.
- `270` points backwards.

Values outside 0 to 360 are fine (`-10` = `350`). Animation always turns the short way round. A key a pose leaves out takes its default (standing, no lift, full length, the equipment's own value), not the previous pose's value.

| Key | Meaning | Standing value |
| --- | --- | --- |
| `torso` | hip to shoulders | `0` |
| `head` | which way the head points (defaults to the neck angle); the face is drawn on its forward side | `0` |
| `neck` | shoulders to the base of the skull (defaults to `head`); set both to show a chin tuck or a head push | `0` |
| `arms` | `[upperArm, forearm, hand]`: shoulder to elbow, elbow to wrist, wrist to fingertips (hand defaults to the forearm angle) | `[180, 180]` |
| `legs` | `[thigh, shin, foot]`: hip to knee, knee to ankle, ankle to toe | `[180, 180, 95]` |

`arms` and `legs` apply to both sides. To move them separately use `{"near": [...], "far": [...]}`. In side view, near is the side facing the viewer, drawn darker; far is drawn lighter behind the body. In front view, near is the figure's left (the viewer's right) and far mirrors it. So `"arms": [90, 90]` raises both arms straight out to the sides.

Useful reference angles:

- **Knee forward of the ankle (squat, lunge front leg):** shin about `195` to `210`.
- **Thigh level with the floor:** `90`.
- **Lying face up, head to the left:** torso `270`. Face down, head to the right: torso `90` (then the front of the chest faces the floor).
- **Arm straight overhead:** `0`. Arm reaching forward: `90`. Arm hanging: `180`.
- **Foot flat on the floor:** `95`. On tiptoe: about `140`. Toes pointing at the floor (kneeling, push-up): `180` to `190`. Front view: `120`.

Segment lengths (metres): torso 0.52, upper arm 0.30, forearm 0.25, hand 0.09, thigh 0.44, shin 0.43, foot 0.17. The head is about 0.3 above the shoulders.

Hands flat on the floor or a bench (push-ups, planks, dips on a bench) need the hand angle set, usually `90` (fingers forward), or the hand points through the floor. Wrist movements are the hand angle: a wrist curl keeps the forearm still and moves the hand from about 40 degrees below the forearm line to 40 above it.

`"shorten": {"thigh": 0.35}` shrinks segments in that pose (1 = full length), for limbs pointing at the viewer: thighs of a figure seated in front view, an arm reaching towards the camera. It animates like the angles.

Front view mirrors the far side about the vertical axis of the picture, not the body. That is right for an upright body. For a body lying on its side, give both sides explicitly, e.g. `{"near": [90, 90], "far": [270, 270]}`.

### Placing the body

The figure is built from the hip outward, then moved so one joint sits at a fixed point:

- **`"anchor": ["nearAnkle", [0, 0.09]]`** is the default: feet planted.
- Other useful anchors:
  - `nearToe` for calf raises and push-ups.
  - `nearWrist` at the bar height for hanging moves.
  - `hip` for lying or seated work. Put it at bench top plus about 0.14, or at 0.11 on the floor.
- Joints are `hip`, `shoulder`, `neckTop`, `head`, and `near`/`far` plus `Shoulder`, `Elbow`, `Wrist`, `Hip`, `Knee`, `Ankle`, `Toe`.
- **`"contact": ["nearWrist", 0.03]`** also rotates the whole body about the anchor until that joint sits at that height. Use it when two points must touch (toes and hands for push-ups and planks, shoulders and feet for bridges). The torso angle then only needs to be roughly right. The rotation turns every segment by the same amount, so a limb you wanted vertical ends up tilted by that amount; check the sheet and adjust.

The floor is at height 0, and `build.py` reports any joint below it.

`"lift": 0.3` in a pose raises the whole body (and anything following its joints) by that many metres after placing it, so jumps can leave the ground: give the take-off pose `0` and the airborne pose a lift.

### Equipment

`equipment` is a list. Held items sit on joints (`"on"`, default both hands, `nearHand`/`farHand`; barbells and bars default to the near hand only, since one bar spans both hands):

- `dumbbell` (front view: add `"axis": 90` to draw it side-on, as when pressing)
- `kettlebell`, `barbell` (also EZ bars; side view draws the plate end-on, `r` sets its radius, default 0.21, use about 0.15 when it hides the movement), `bar` (an empty bar or stick), `plate`, `medicineBall`, `handle`
- `hanging`: a weight on a strap or chain hanging straight down from the joint, `chain` (length, default 0.3) and `r`. Use it for head harnesses (`"on": ["head"]`), dip belts (`"on": ["hip"]`) and wrist rollers.

Connectors run from `"from"` (a point `[x, y]`, or a joint name such as `"nearToe"` for a band under the foot) to joints (`"on"`, default `["nearHand"]`):

- `cable` (pulley at `from`)
- `rope`
- `band`
- `lever`: a machine arm. Put the pivot at `from` and the pad or handle at the joint. Use it for any leverage, chest-press, leg-extension or leg-curl machine.

Fixed props sit at `"at": [x, y]`, or at a joint name to follow it (a sled or roller that moves with you):

- `bench`: `length`, and `angle` 90 for flat, about 55 for incline back support. Use two benches for a seat plus backrest. `at` is the centre of the pad, which is 0.09 thick, so its top surface is 0.045 above `at` on a flat bench.
- `box`: `w`, `h`; `at` is the bottom centre.
- `ball`: stability ball, `r` 0.33; `at` is the centre.
- `bosu`, `roller`.
- `pullupBar`, `parallelBars`: `at` is the grip.
- `rails`: Smith machine or rack upright at `at[0]`.
- `wall`.
- `sled`: `w`, `h`.
- `pad`: `w`, `h`, `angle`.

### Equipment that moves

A pose can change any equipment value with `"props"`, a list matching `equipment` by position (use `{}` to leave one alone). Numbers animate between poses. For example, a wrist roller raising its weight, with the first item the roller handle and the second the weight:

```json
"poses": [
  { "arms": [140, 90], "props": [{}, { "chain": 0.8 }] },
  { "arms": [140, 90, 30], "props": [{}, { "chain": 0.3 }] }
]
```

Grips are not drawn: palms up, palms down and neutral look the same. For pronation and supination, animate a front-view dumbbell's `axis` through `props`.

### Sharing movements

`"extends": "templates/barbell-curl.json"` starts from another file; any key you give replaces that key. For example, a dumbbell curl is the barbell curl with different equipment:

```json
{ "extends": "templates/barbell-curl.json", "equipment": [{ "type": "dumbbell" }] }
```

### What good looks like

- One clear movement, two to four poses. Show the range the instructions describe.
- Choose the view that shows the movement best. Use side view for anything moving forwards and back (curls, squats, presses, rows). Use front view for movements out to the sides (lateral raises, jacks, side bends).
- Feet and hands that should stay put do stay put. Use the anchor and contact for that.
- Equipment matches the exercise's `equipment` field.
- Check the contact sheet (one row per figure, every key pose) for every figure before calling it done: limbs bending the wrong way, joints through the floor or bench, a bar floating away from the hands.

## License

Code: MIT-0. Figure files, rendered animations and exercise text: CC0 1.0 (public domain). Anyone may use, change or sell them without asking or giving credit.
