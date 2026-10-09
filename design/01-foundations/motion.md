# Motion spec

Values are in dp, dp/s and ms. Constants live in `tokens.json › motion` (generated into `tokens.ts` as
`motion`). Built with **react-native-gesture-handler** (`Gesture.Pan()`) and **Reanimated 3**
(`useSharedValue`, `withSpring`, `withTiming`, `Easing.bezier`). `04-prototype/swipe-demo.html`
implements this spec on the web (pointer and keyboard events) and is the reference to match.

## 1. Durations and easing (Material 3)

| Token | ms | Use |
| --- | --- | --- |
| short2 | 100 | Press feedback, chip state |
| short3 | 150 | Fades, reduced-motion cross-fades, tint release |
| short4 | 200 | Small expansions, snackbar exit |
| medium1 | 250 | Next card promote, snackbar enter, count tick |
| medium2 | 300 | Sheets enter, page transitions, undo return |
| medium4 | 400 | Coach-mark demo moves |
| long2 | 500 | Round-complete summary entrance (once) |

| Easing | cubic-bezier | Use |
| --- | --- | --- |
| standard | 0.2, 0, 0, 1 | Most transitions |
| emphasizedDecelerate | 0.05, 0.7, 0.1, 1 | Things entering (sheets, next card, undo return) |
| emphasizedAccelerate | 0.3, 0, 0.8, 0.15 | Things leaving (card exit, sheet dismiss) |
| standardDecelerate / standardAccelerate | 0,0,0,1 / 0.3,0,1,1 | Fades in / out |

Reanimated: `Easing.bezier(0.05, 0.7, 0.1, 1)` etc.

## 2. The swipe

Definitions: `W` = card width (372 max; 412 − 2×20 gutter), `H` = card height. `dx`, `dy` = translation
from the gesture start; `vx`, `vy` = release velocity (dp/s, from `event.velocityX/Y`).

### 2.1 Gesture setup

```ts
Gesture.Pan()
  .activeOffsetX([-8, 8]).activeOffsetY([-8, 8])   // activeOffset: 8 — taps still reach the card
  .onUpdate(e => { x.value = e.translationX; y.value = e.translationY; })
  .onEnd(e => commitOrSnap(e))
```

A tap (no movement beyond 8 dp, < 250 ms) opens item detail (S26). Down-swipes are ignored for decisions
(the card follows with 0.35 resistance and snaps back) so a downward scroll intent never decides.

### 2.2 Which decision (direction)

```
up    if  -dy > |dx| × 1.2  and dy < 0          (upDominance 1.2)
right if  dx > 0  and not up
left  if  dx < 0  and not up
none  if  |dx| < 8 and |dy| < 8
```

### 2.3 Progress and thresholds

```
thresholdX  = max(W × 0.30, 96)        // commitRatioX 0.30, commitMinX 96   → ≈112 dp on a 372 card
thresholdUp = max(H × 0.18, 96)        // commitRatioUp 0.18, commitMinUp 96 → ≈100 dp on a 560 card
progress    = clamp(|dx| / thresholdX, 0, 1)   (left/right)
            = clamp(-dy / thresholdUp, 0, 1)   (up)
armed       = progress == 1
```

Commit on release when **either**:
- `armed` (distance past the threshold), **or**
- a fling: velocity in the decision direction ≥ **900 dp/s** (`flingVelocity`) **and** distance in that
  direction ≥ **32 dp** (`flingMinDistance`).

Otherwise snap back.

### 2.4 Feedback while dragging (all interpolated from `progress`, no timers)

| Property | Value |
| --- | --- |
| Rotation | `rotate = clamp(dx / W, -1, 1) × 12°` (`maxRotateDeg` 12). Pivot: card center shifted down by H/2 (bottom center), so the top of the card leads like a held playing card. Up-swipes do not rotate beyond the dx component. |
| Lift | shadow switches from `shadow-hero` to `shadow-hero-drag` when the drag starts (150 ms), scale 1 → 1.02 |
| Tint | A full-card overlay in the decision color: `bg-accept` / `bg-reject` / `bg-maybe`, opacity `progress × 0.18`, rising to **0.24** when armed. The card content stays readable. |
| Decision stamp | Pill with icon + label ("Accept", "Reject", "Maybe") in the solid decision color, positioned at the leading edge of the movement: Accept top-left, Reject top-right, Maybe bottom-center. Opacity `interpolate(progress, [0.15, 0.6], [0, 1])`, scale `interpolate(progress, [0, 1], [0.85, 1])`. When armed the stamp scales to 1.06 for 100 ms then 1 (a "click"). |
| Decision button | The matching button below the card fills with its soft color proportional to progress and fills solid when armed, so gesture and button stay linked. |
| Next card | Behind the top card at `scale 0.95, translateY 14, opacity 1`. Promotes with progress: `scale = 0.95 + 0.05 × progress`, `translateY = 14 × (1 − progress)`. |
| Haptic: arm | `Haptics.selectionAsync()` when crossing into armed, and again when crossing back out (lets users feel the threshold). |

### 2.5 Commit

1. Haptic: `Haptics.impactAsync(ImpactFeedbackStyle.Medium)` (same for all decisions: calm and equal).
2. Card exits along its direction: target `x = sign(dx) × W × 1.6` (left/right) or `y = −H × 1.6` (up),
   keeping the current rotation and adding up to 6° more.
3. Duration: `clamp(remainingDistance / max(|v|, 1800) × 1000, 160, 260)` ms, `emphasizedAccelerate`.
   A fast fling leaves fast; a slow drag-past-threshold still leaves briskly.
4. Next card completes its promote with `withSpring(promote)` (damping 22, stiffness 260).
5. The count in the decision button ticks up: number slides up 8 dp and fades in (250 ms, emphasized
   decelerate); the progress bar advances (250 ms, standard).
6. Decision is written immediately (local first), undo stack pushes `{ itemId, decision }`.
7. Screen reader announcement: "Accepted Ayşe Demir. 77 of 100 decided."

### 2.6 Snap back

`x, y → 0` with `withSpring(snapBack)` (damping 18, stiffness 220, mass 1; settles ≈350 ms, slight
overshoot ≤ 4 dp). Tint and stamp fade with progress; rotation follows x.

### 2.7 Buttons (equivalent to gestures)

Tapping Reject / Maybe / Accept runs the same commit as a gesture: the card first moves 24 dp in the
direction with the stamp at full opacity (100 ms, standard), then exits (`buttonExitDuration` 240 ms,
emphasizedAccelerate). Same haptic. Buttons are disabled for the 240 ms exit to prevent double commits;
a second tap during the exit is queued and applies to the next card (fast sorting stays fast).

### 2.8 Undo

The last decided card returns from the side it left (reverse of its exit path): `withTiming` 300 ms,
`emphasizedDecelerate`, rotation from exit angle to 0, then sits on top of the stack. The current card
demotes to the "next" position (scale 0.95, translateY 14) at the same time. Haptic `ImpactFeedbackStyle
.Light`. The decision count decrements with the reverse tick. Snackbar: "Undid Accept on Ayşe Demir". Undo
is available while the undo stack is non-empty; multiple undos step back in order.

### 2.9 Keyboard (web desktop)

→ Accept, ← Reject, ↑ Maybe, Z Undo; Enter opens item detail, N opens the note. A key press runs the
button sequence (2.7). Holding a key does not repeat (ignore `event.repeat`).

### 2.10 Screen readers

The card exposes custom actions: "Accept", "Reject", "Maybe", "Undo", "Add note", "Open details"
(`accessibilityActions` in RN; `aria-*` + buttons on web). Swipe gestures are not required. On commit,
announce the result and progress (2.5 step 7).

## 3. Other motion

| Element | Enter | Exit |
| --- | --- | --- |
| Bottom sheet (note, filters, actions) | translateY 100% → 0, 300 ms emphasizedDecelerate; scrim 0 → 50% opacity 300 ms | 200 ms emphasizedAccelerate; drag-to-dismiss past 30% height or 800 dp/s |
| Dialog | scale 0.96 → 1 + fade, 250 ms emphasizedDecelerate | fade 150 ms |
| Snackbar | translateY 16 → 0 + fade, 250 ms emphasizedDecelerate; auto-dismiss 4 s (with action: 6 s; never under 10 s with a screen reader running) | fade 200 ms |
| Push screen (Android) | M3 shared axis X: slide 30 dp + fade, 300 ms | reverse |
| Push screen (iOS) | native stack slide | native |
| Coach marks | Hand cursor demo: card moves 72 dp right/left/up with the stamp, 400 ms emphasized, then returns with spring; loops twice per step, then waits | fade 150 ms |
| Onboarding gesture demo (S02) | Same as sorting, live | — |
| Round summary | Counts tick from 0 to value over 500 ms (standardDecelerate), once | — |
| Progress bar | width 250 ms standard | — |
| Skeleton loading | opacity pulse 0.5 ↔ 1, 1,000 ms ease-in-out, infinite | — |
| Sync notice | icon rotation 1,000 ms linear while syncing | — |

## 4. Reduced motion

Detect with `AccessibilityInfo.isReduceMotionEnabled()` / Reanimated `useReducedMotion()`; on web
`prefers-reduced-motion: reduce`.

| Animation | Reduced-motion alternative |
| --- | --- |
| Card drag | Card follows the finger **without rotation or scale**; tint and stamp still appear (they carry meaning). |
| Commit (gesture or button) | No fly-out: the top card fades out (150 ms) while the next card fades in in place (150 ms). |
| Snap back | Instant return (no spring). |
| Undo | Previous card fades in on top (150 ms). |
| Next card promote | No scale/translate; next card stays still behind, then cross-fades. |
| Count tick | Number changes instantly. |
| Sheets and dialogs | Fade only, 150 ms. |
| Screen transitions | Fade only, 150 ms. |
| Coach marks | Static illustrations with arrows; no looping hand. |
| Skeleton pulse | Static muted blocks. |
| Round summary count-up | Final numbers shown immediately. |
| Sync spinner | Static `refresh-cw` icon with "Syncing…" text. |

## 5. Haptics

| Moment | Android/iOS (expo-haptics) | Web |
| --- | --- | --- |
| Crossing the decision threshold (in or out) | `selectionAsync()` | none |
| Commit (any decision, gesture or button) | `impactAsync(Medium)` | none |
| Undo | `impactAsync(Light)` | none |
| Round complete | `notificationAsync(Success)` | none |
| Error (import failed, export failed) | `notificationAsync(Error)` | none |

Haptics respect the Settings › Haptics switch (S06). On web the switch is shown disabled with "Haptics
need the Android or iOS app."
