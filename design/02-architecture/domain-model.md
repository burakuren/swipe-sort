# Domain model

The entities the UI shows, their fields and statuses. Names match the UI glossary. This is a UI model,
not a storage schema (storage and sync are out of scope); field names are suggestions for TypeScript
types. Sample records: `02-data/sample-data.json`.

## Overview

```
User ──< Membership >── List ──< Item ──< FieldValue
                         │  │      ├──< Decision (one per member per round)
                         │  │      ├──< Note
                         │  │      └──< Edit (working-copy change, revertible)
                         │  ├──< Field (schema of the list)
                         │  ├──< Source (where items came from)
                         │  ├──< Round
                         │  └──  CardTemplate (one active)
                         └──< ActivityEvent
```

## User

| Field | Type | Notes |
| --- | --- | --- |
| id | string | |
| name | string | From Google/Apple or entered at email sign-up |
| email | string | |
| avatar | image? | Initials fallback |
| authProviders | ('google' \| 'apple' \| 'email')[] | Shown in S07 connected accounts |
| isGuest | boolean | Guest = no account; lists exist only on this device |

Guest mode: the app works fully for solo lists. Share and backup require an account (S05). On sign-in,
all device lists move to the account (`List.backedUp` becomes true).

## List

| Field | Type | Notes |
| --- | --- | --- |
| id, name | string | Name 1–80 chars |
| templateId | CardTemplate id | Changeable any time (S22 change mode) |
| fields | Field[] | Union of mapped fields from all sources |
| sources | Source[] | A list can combine several sources |
| itemCount | number | |
| shared | boolean | true when it has more than one member or pending invites |
| ownerId | User id | |
| conflictRule | 'everyone' \| 'majority' \| 'decisionMaker' | Shared only. Default when a list is first shared: `decisionMaker`, with the Owner as Decision Maker (see assumptions) |
| currentRoundId | Round id? | |
| backedUp | boolean | false for guest lists → "Not backed up" indicator |
| archived | boolean | Archived lists are read-only until restored |
| updatedAt | datetime | |
| showOthersDecisions | boolean (per member) | Sorting preference on shared lists; default false |

## Field

| Field | Type | Notes |
| --- | --- | --- |
| key | string | Stable key from mapping |
| label | string | Renamable in S19 |
| type | 'text' \| 'number' \| 'phone' \| 'email' \| 'date' \| 'link' \| 'image' | Set in S19 |
| hidden | boolean | Hidden fields are kept in the working copy and export but never shown on cards |
| isTitle | boolean | Exactly one title field per list |
| multi | boolean | Multi-value (several phone numbers). Card shows the first value + "+2"; detail shows all |

## Source

| Field | Type | Notes |
| --- | --- | --- |
| type | 'contacts' \| 'csv' \| 'xlsx' \| 'text' \| 'manual' \| 'googleSheets' \| 'photos' | Extensible: a new type adds one tile in S11 and implements the same steps |
| label | string | e.g. "mert-family.csv", "Flat hunt 2026 › Kadıköy" |
| itemCount | number | |
| importedAt | datetime | |
| googleSheet? | { spreadsheetId, tabName } | Needed for writing back on export |

Source definition (for adding new sources): `{ id, name, icon, availableOn: ('android'|'ios'|'web')[],
needsPermission?: 'contacts'|'photos', selectStep: component, hasFieldMapping: boolean }`. All sources
share steps: Select → Map fields (optional) → Review duplicates (automatic) → Finish.

## Item

| Field | Type | Notes |
| --- | --- | --- |
| id | string | |
| values | Record<fieldKey, value \| value[]> | Working copy |
| originalValues | Record<fieldKey, value> | As imported; never changed |
| sourceId | Source id | |
| position | number | Original order |
| addedInRoundId? | Round id | Items added mid-round join the current round |

Derived per item:
- **My decision**: the current user's Decision in the current round (or none).
- **List status** (shared): Pending / Agreed / Conflict (see below).
- **Final decision**: solo = my decision; shared = the agreed or resolved decision.

## Decision

| Field | Type | Notes |
| --- | --- | --- |
| itemId, memberId, roundId | ids | One per member per item per round |
| value | 'accept' \| 'reject' \| 'maybe' | |
| decidedAt | datetime | |
| syncState | 'synced' \| 'pending' | Offline decisions are 'pending' until synced |

Undo removes the member's latest decision in this round (stack per member per round, unlimited depth
within the session; after leaving, undo history persists for the round). Changing a decision from Results
replaces the value.

## List status (shared lists)

Computed per item in the current round:

| Status | Rule |
| --- | --- |
| **Pending** | Not every member has decided, and no two members disagree yet |
| **Agreed** | Every member chose the same decision → final decision |
| **Conflict** | At least two members chose differently (Maybe vs. Accept counts) — shown as soon as a disagreement exists, even if others have not decided yet |
| **Resolved** | A conflict closed by the conflict rule; shows the final decision with "Resolved by Mert" or "Majority" |

Conflict rules:

| Rule | Final decision |
| --- | --- |
| Everyone must agree (`everyone`) | Only Agreed. Conflicts stay open until members change decisions to match. Every member can open S36 and see others' decisions and notes. |
| Majority decides (`majority`) | When every member has decided: the decision with most votes. Ties → the Decision Maker's decision; with no Decision Maker the tie stays a Conflict. Before everyone has decided, a disagreement shows as Conflict ("Waiting for 1 member"). |
| Decision Maker decides (`decisionMaker`) | Every conflict is resolved by the Decision Maker in S36 (one by one) or S37 (bulk). Resolution is final; members see "Resolved by Mert". |

Bulk resolve (Decision Maker only): applies the Decision Maker's own decision to every open conflict in the
current round. Conflicts where the Decision Maker has no decision stay open; the summary reports
"3 conflicts stay open because you haven't decided them".

## Member (membership)

| Field | Type | Notes |
| --- | --- | --- |
| userId, listId | ids | |
| role | 'owner' \| 'collaborator' | Exactly one Owner |
| isDecisionMaker | boolean | Independent switch, at most one per list; the Owner can assign it to anyone including themselves |
| progress | { decided, total, accept, reject, maybe } | Current round |
| joinedAt | datetime | |
| status | 'active' \| 'invited' | Invited = link sent, not yet joined |

Displayed role names: **Owner**, **Decision Maker**, **Collaborator**. A member who is Decision Maker
shows "Decision Maker" (and "Owner, Decision Maker" when both).

Permissions:

| Action | Owner | Decision Maker | Collaborator |
| --- | --- | --- | --- |
| Sort, add notes, edit fields | ✓ | ✓ | ✓ |
| Invite | ✓ | ✓ | ✓ (as Collaborator only) |
| Start a round | ✓ | — | — |
| Change conflict rule | ✓ | — | — |
| Assign Decision Maker, change roles, remove members, transfer ownership | ✓ | — | — |
| Resolve conflicts (decisionMaker rule, majority ties) | — unless also DM | ✓ | — |
| Change template, add items | ✓ | ✓ | ✓ |
| Rename, archive, delete list | ✓ | — | — |
| Leave list | after transferring ownership | ✓ | ✓ |

Removing a member: the Owner chooses "Keep their decisions" (they still count toward statuses) or
"Discard their decisions" (statuses recompute without them).

## Invite

| Field | Type | Notes |
| --- | --- | --- |
| token | string | In `https://swipesort.app/join/<token>` |
| role | 'collaborator' \| 'decisionMaker' | Chosen while inviting; Decision Maker only offered to the Owner |
| createdBy | User id | |
| expiresAt | datetime | 14 days; Owner can reset the link (revokes the old one) |
| maxUses | number? | Unlimited by default ("any number of people") |

## Note

| Field | Type | Notes |
| --- | --- | --- |
| itemId, authorId | ids | |
| text | string | Up to 1,000 chars |
| private | boolean | Default false (visible to all members). Private notes show a `lock` icon, "Only you" label and a dashed outline |
| updatedAt | datetime | |

One note per member per item (editing replaces). On solo lists the private option is hidden.

## Edit

| Field | Type | Notes |
| --- | --- | --- |
| itemId, fieldKey | ids | |
| original | value | From `Item.originalValues` |
| value | value | Current working value |
| editedBy, editedAt | | |

Edited fields show a `pencil-line` marker and "Edited" label; "Revert to original" restores `original`.
The source is never changed automatically (exports write new files or, for Google Sheets, only after an
explicit confirmation).

## CardTemplate

| Field | Type | Notes |
| --- | --- | --- |
| id, name | string | Built-ins: Person, Product, Photo, Task, Candidate, Generic (not editable, can be duplicated) |
| builtIn | boolean | |
| layout.image | 'none' \| 'avatar' \| 'cover' \| 'full' | Image area |
| layout.title | fieldKey | |
| layout.subtitle | fieldKey? | |
| layout.rows | fieldKey[] (0–6) | Label + value rows |
| layout.tags | fieldKey[] (0–3) | Rendered as chips |
| usedBy | List id[] | Deleting a template in use asks to pick a replacement |

Missing values: rows with no value are hidden on the card (shown as "—" in item detail); missing image
shows the initials (avatar) or an `image-off` placeholder (cover/full). Long text: title wraps to 3 lines
then truncates with "…"; rows truncate to 1 line; full text in item detail.

## Round

| Field | Type | Notes |
| --- | --- | --- |
| id, number, name | | "Round 2" |
| include | 'all' \| 'maybe' \| 'accepted' \| 'custom' | Custom = filter by field values or a manual selection |
| filter? | { fieldKey, operator, value }[] | For custom |
| order | 'original' \| 'shuffled' \| { sortBy: fieldKey, direction } | |
| itemIds | string[] | Snapshot at start |
| startedBy, startedAt, completedAt? | | Shared: only the Owner starts rounds; applies to everyone |
| result | { accept, reject, maybe, conflict? } | |

Starting a new round while one is in progress asks to end the current one (S40 dialog). Decisions from
earlier rounds stay in round history (S30); results show the latest decision per item.

## ActivityEvent

| type | Text example | Opens |
| --- | --- | --- |
| memberJoined | "Selin joined Wedding guests" | S34 |
| memberFinished | "Selin finished sorting Wedding guests" | S09 |
| newConflicts | "15 conflicts in Wedding guests" | S36 |
| conflictsResolved | "Mert resolved 12 conflicts" | S28 |
| roundStarted | "Deniz started Round 2 (11 items)" | S25 |
| roleChanged | "Deniz made you the Decision Maker" | S34 |

Each event: `{ id, listId, type, actorId?, targetId?, count?, createdAt, read }`. Push on Android/iOS
(with per-type preferences); in-app only on web.

## Sync and offline (UI only)

- Every change is saved locally first. A list shows "Saved on this phone" while offline and "Synced"
  once uploaded (S40 sync notice). Guest lists are always local.
- Offline: sorting, notes, edits, undo work. Not available offline: import from Google Sheets, invite,
  export to Google Sheets, sign-in; these show the offline state with "Try again when you're online".
