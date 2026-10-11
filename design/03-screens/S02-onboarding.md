# S02 Onboarding

Frames: `S02-onboarding.html`. Generator: `tools/generators/S02-onboarding.py`. Drag physics:
`01-foundations/motion.md` §2 (live in `04-prototype/swipe-demo.html`). Card visuals: S25.

## 1. Purpose and requirements

Teach the one idea of the product in under 30 seconds: one card at a time, three gestures. The person
learns by doing on neutral sample cards (a desk, a lamp, two places), then lands in an empty Lists tab
without being asked for an account.

Covers: SCR-02, SRT-02, SRT-03, SRT-04 (snap back below the threshold), SRT-05, SRT-15 (first teaching
moment; S25 coach marks repeat it in context), PLT-05, PLT-06, PLT-16, PLT-17, PLT-18, PLT-19, PLT-21,
PLT-23, ACC-01, GOAL-01, GOAL-02, SUC-04, SUC-06, SUC-08, VIS-03, VIS-08, VIS-09, VIS-11, DEL-22 (flow 1).

## 2. Entry points and exits

| From | How |
| --- | --- |
| S01 | First launch on this device |
| S06 › Help and feedback | "Replay the introduction" (opens `S02-default`: the welcome with Close instead of Skip; "Try the gestures" opens the demo; Close and "Done" return to S06 › Help) |

| To | How |
| --- | --- |
| `S02-demo` | "Get started" (`data-action="next"`) |
| S03 `S03-default` | "I have an account" (`data-action="sign-in"`) on welcome and recap |
| S08 `S08-first-run` | "Skip" (`data-action="skip"`) on welcome or demo; "Get started" on the recap (`data-action="get-started"`) |
| `S02-demo-done` | Automatically 700 ms after the third different gesture (prototype: clicking the card in `S02-demo` has `data-action="next"`; the decision buttons step through `S02-demo-step-2`, `-step-3` and the recap) |

Onboarding is shown once per device. Completing or skipping it sets `onboardingDone`; S01 then routes to
S08. Back on the demo returns to welcome; system back on welcome leaves the app (Android) as usual.

## 3. Layout and components

**Welcome** (`S02-welcome`): app bar with a trailing text button "Skip"; hero illustration made of real
sample cards (no drawing): two cards fanned behind (photo `ph09`, product `p05`, rotated ±6°, `rounded-hero`,
`shadow-raised`) and a top SwipeCard (`p02`, rotated 3°, `shadow-hero`) carrying an Accept stamp. Below:
`text-title-1` headline (centered, balanced wrap), `text-body-lg` sentence, bottom stack: primary Button lg
"Get started", ghost "I have an account", reassurance line with `smartphone` icon.

**Demo** (`S02-demo…`): app bar (back, "Skip"); instruction block: `text-title-2` instruction that always
names the next untried gesture, one `text-body` line, and the **GestureChecklist** (Proposed: three chips in
Reject, Maybe, Accept order; untried = dashed outline muted; tried = soft decision fill + `circle-check`;
"1 of 3" counter). CardStack: SwipeCard (S25 styling, inset 32 so the side hint fits) with the next card
behind; a hint bubble (56 round `bg-popover shadow-overlay`, arrow icon) at the edge the card should move
to. DecisionBar: Reject, Maybe, Accept (64 round buttons with labels; no counts, no Undo, no Note:
those are taught by the S25 coach marks).

**Recap** (`S02-demo-done`): app bar (back to demo), `text-title-1` title, one sentence, a ListGroup of
the three sample decisions (thumbnail 40, title, "Swiped left" with arrow icon, DecisionBadge), bottom stack
like welcome.

Demo deck (sample data): `p02` Walnut sit-stand desk, Göreme, Cappadocia (image `ph09`), `p05` Ceramic desk
lamp, Kadıköy, İstanbul (image `ph05`). Product and Photo card templates, so no domain words appear. The two
place cards use the Photo template the way the "Trip ideas" sample does (image link, place as title, "Turkey,
best in spring" / "best in autumn" as the second line); they no longer show gallery file names and dates
(D-32, A-131).

## 4. States

| Frame | Trigger |
| --- | --- |
| `S02-default` | Replay from Settings › Help: the welcome with Close (no Skip, no "I have an account"), "Try the gestures" and "Done". Entry frame for links from other files |
| `S02-welcome` | First launch (flow 1) |
| `S02-demo` | "Get started". 0 of 3 tried; hint bubble on the right edge |
| `S02-demo-drag-accept` | Dragging right past the threshold: tilt, 24% accept tint, Accept stamp, Accept button solid, next card promoting |
| `S02-demo-snap-back` | Released below the threshold: card springs back; the subtitle becomes an inline hint |
| `S02-demo-step-2` | After Accept: chip checked, instruction "Swipe left to reject", hint on the left |
| `S02-demo-drag-reject` | Dragging left, armed |
| `S02-demo-step-3` | After Reject: instruction "Swipe up for maybe", hint above the card |
| `S02-demo-drag-maybe` | Dragging up, armed (stamp bottom-center) |
| `S02-demo-other-order` | The person did another gesture first: it counts; the instruction names the next untried gesture |
| `S02-demo-done` | Third different gesture committed (or the third different button tapped) |
| `S02-demo-reduced-motion` | Reduce motion on: no tilt or scale, static hint |
| `S02-welcome-large-text`, `S02-demo-large-text` | Font scale ≥ 150% |
| `S02-demo-screen-reader` | Screen reader on (annotation of the card actions) |
| `S02-welcome-ios`, `S02-demo-ios` | iOS |
| `S02-web` | Mobile browser (note about the app) |
| `S02-web-desktop` | Desktop browser with keyboard hints |

## 5. Interactions, gestures and transitions

- Drag, thresholds, fling, commit and snap back are exactly S25 (motion.md §2.2–2.6): horizontal
  threshold `max(0.30 × W, 96)`, up `max(0.18 × H, 96)`, fling ≥ 900 dp/s; down-swipes never decide.
- Commit: medium haptic, card exits, next card rises, the matching chip fills (150 ms cross-fade) and the
  counter ticks. Nothing is saved; the deck is local and resets on replay.
- Buttons commit the same way (motion.md §2.7) and count as trying the gesture, so the demo is completable
  without swiping (accessibility).
- Repeating a gesture already tried still sorts the card but does not advance the checklist. If the deck
  runs out before all three are tried, it reshuffles the same four cards.
- Hint bubble: moves 24 dp toward its arrow and back, 800 ms ease-in-out, twice, then rests; it disappears
  as soon as a drag starts. Reduced motion: static.
- Snap-back hint: shown after the second release below the threshold within one card (not on the first, to
  avoid nagging); it replaces the instruction's subtitle (info icon, `role=status`) until the next commit, so
  it never covers the card.
- After the third gesture: success haptic (`notificationAsync(Success)`), 700 ms pause, then the recap
  pushes in (shared axis X, 300 ms; reduced motion: 150 ms fade).
- Skip is always available; it sets `onboardingDone` and opens S08 first run.
- Keyboard (web desktop): → Accept, ← Reject, ↑ Maybe (motion.md §2.9). Enter on the focused card is
  ignored in the demo (there is no detail sheet).

## 6. Copy

| Element | String |
| --- | --- |
| Skip | "Skip" |
| Welcome headline | "Sort any list, one card at a time" |
| Welcome body | "Swipe right to accept, left to reject, up for maybe. Works for people, places, things to buy and ideas, alone or with others." (D-32: "photos" became "places") |
| Welcome buttons | "Get started", "I have an account" |
| Reassurance | "No account needed. Lists stay on this phone." |
| Hero stamp | "Accept" |
| Demo step 1 | "Swipe right to accept" / "Try it on these sample cards. Nothing is saved." |
| Demo step 2 | "Swipe left to reject" / "Accepted. Now send this one the other way." |
| Demo step 3 | "Swipe up for maybe" / "Not sure? Maybe items wait in their own pile so you can sort them again later." |
| Other order (example) | "Swipe right to accept" / "Rejected. You can also accept: swipe right." (pattern: "{Past tense of last}. You can also {verb}: swipe {direction}.") |
| Checklist | "Reject", "Maybe", "Accept"; counter "1 of 3"; screen reader suffix ", tried" / ", not tried yet" |
| Stamps and buttons | "Accept", "Reject", "Maybe" |
| Snap-back hint (inline) | "Drag a little further to decide. Let go early to cancel." |
| Replay (`S02-default`) | Close label "Close the introduction"; buttons "Try the gestures", "Done" |
| Recap title | "You know the three gestures" |
| Recap body | "Right to accept, left to reject, up for maybe. Undo is always one tap away, and you can change any decision later." |
| Recap rows | "Göreme, Cappadocia" / "Swiped left" / "Rejected"; "Ceramic desk lamp" / "Swiped up" / "Maybe"; "Walnut sit-stand desk" / "Swiped right" / "Accepted" |
| Recap buttons | "Get started", "I have an account" |
| Large-text demo | "Or use the buttons below."; "0 of 3 gestures tried"; card rows "Price", "Rating" ("4.7 (532 reviews)"), tag "Desk" pinned at the bottom (A-125: content centered) |
| Web note | "Using SwipeSort in your browser" / "Everything works here. Get the app to import your phone contacts." (D-32: no photo source) / "Get the app" |
| Desktop instruction | "Press → or drag right to accept" (steps 2–3: "Press ← or drag left to reject", "Press ↑ or drag up for maybe") |
| Keyboard hints | "← Reject", "↑ Maybe", "→ Accept" |
| Screen reader instruction | "Try the three decisions on these sample cards. Use the card's actions or the buttons below." |
| Screen reader after action | "Accepted. 1 of 3 tried." |
| Prototype-only link | Card overlay labelled "Finish the demo (prototype: click the card; the app moves on after the third gesture)" (not in the app) |

## 7. Accessibility

- Focus order: Back, Skip, instruction, checklist, card, Reject, Maybe, Accept.
- The card is one focusable element with the template label (e.g. "Walnut sit-stand desk, 140 × 70 cm,
  Oakline, 649 euros, rated 4.7") and custom actions Accept, Reject, Maybe (TalkBack actions menu,
  VoiceOver rotor). With a screen reader on, the instruction text changes to the screen-reader version.
- Every gesture has a visible 64 dp button; the demo can be completed with buttons alone.
- Decisions show icon + label + color on stamps, buttons, chips and recap badges.
- Large text (`S02-*-large-text`): welcome hides the hero, scales the body to `text-title-2` and keeps the
  reassurance line; the demo hides card images, shows more fields (price, rating; content centered, tag pinned, A-125) and uses the S25
  labeled button grid; buttons grow to two lines instead of truncating.
- Reduced motion: drag without rotation or scale; commit cross-fades (150 ms); hint bubble static.
- The hero is decorative (`aria-hidden`).

## 8. iOS and web differences

- **iOS** (`S02-welcome-ios`, `S02-demo-ios`): navigation bar with "Back" chevron and a trailing text
  "Skip"; edge swipe goes back one step. Same deck, haptics via Taptic Engine. The welcome does not show
  Sign in with Apple; "I have an account" opens S03 iOS (Apple first there).
- **Web, mobile** (`S02-web`): no system bars; a neutral note at the top explains what the app adds
  (phone contacts) with "Get the app"; no haptics.
- **Web, desktop** (`S02-web-desktop`): phone column; the instruction mentions the arrow key; kbd hints
  under the buttons (web only, PLT-06); mouse drag works like touch.

## 9. Edge cases

- **Replay from Settings** (`S02-default`): Close and "Done" return to S06 › Help; the demo and recap work as on first
  launch, and the recap's "Get started" also returns to S06 › Help.
- **Person opens the app from an invite link first**: onboarding is skipped (S01 → S32); after joining,
  S25 coach marks teach the gestures in context. S02 can still be replayed from Settings.
- **Already signed in on another device** ("I have an account"): S03; after sign-in, S08 shows the
  account's lists and onboarding is marked done.
- **Long translations** (+40%): instructions wrap to two lines; checklist chips wrap to a second row; the
  card area shrinks (card is flexible height, min 320).
- **Missing sample images**: cards fall back to the `image-off` placeholder; the demo still works.
- **App killed mid-demo**: onboarding restarts at welcome on next launch (nothing to resume).
- **Offline**: everything works; no network needed.
