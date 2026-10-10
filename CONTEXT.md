# SwipeSort

SwipeSort turns any list into a deck of cards that people sort one at a time with swipe gestures, alone or
together with others. This glossary is the shared language for the UI, specs and code. Seeded from the
terminology section of `design/00-brief/brief.md`; the brief wins where they disagree.

## Language

### Lists and items

**List**:
A collection of items to sort.
_Avoid_: Deck, collection, project, guest list

**Item**:
A single record in a list (a contact, a spreadsheet row, a photo).
_Avoid_: Card (the card is how an item is shown), entry, row, guest, invitee

**Field**:
A piece of information on an item (name, phone, price…).
_Avoid_: Column, attribute, property

**Source**:
Where items come from (phone contacts, a CSV file, a Google Sheet…). A list can combine several sources.
_Avoid_: Import, data source, origin

**Original**:
An item's field values exactly as they came from its source. Never changed automatically.
_Avoid_: Source data, raw data

**Working copy**:
SwipeSort's own copy of a list's items, where edits and notes live; the original stays untouched.
_Avoid_: Draft, local copy

**Card template**:
Which fields appear on a card and how they are laid out.
_Avoid_: Layout, theme, card style

**Note**:
A member's free-text remark on an item; shared with all members unless marked private.
_Avoid_: Comment

### Sorting

**Round**:
One sorting pass over a set of items.
_Avoid_: Session, pass, iteration

**Decision**:
One of Accept, Reject or Maybe, made by one member on one item in one round.
_Avoid_: Vote, choice, rating

**Accept** / **Reject** / **Maybe**:
The three decisions (swipe right, left, up).
_Avoid_: Yes / No, Like / Dislike, Keep / Discard

**Decided**:
An item that has a decision from the current user in the current round.

**My decision**:
The current user's decision on an item.

**Final decision**:
The list-level decision on an item. On a solo list it is my decision; on a shared list it comes from
agreement or from the conflict rule.
_Avoid_: Result, outcome

### Shared lists

**Solo list** / **Shared list**:
A list with one member, or with more than one member (or pending invites).

**List status**:
The state of an item on a shared list: Pending, Agreed, Conflict, or Resolved.

**Pending**:
Not every member has decided the item yet, and no two members disagree.

**Agreed**:
Every member chose the same decision; it becomes the final decision.

**Conflict**:
An item that members of a shared list decided differently (Maybe vs. Accept counts as different).
_Avoid_: Disagreement, clash

**Resolved**:
A conflict closed by the conflict rule, carrying a final decision.

**Conflict rule**:
The Owner's choice of how conflicts become final: Everyone must agree, Majority decides, or Decision
Maker decides.

**Bulk resolve**:
The Decision Maker applying their own earlier decisions to every open conflict in the current round.
_Avoid_: Resolve all (that is the button label, not the concept)

**Member**:
Anyone on a shared list, whatever their role.
_Avoid_: User (a user may be a member of many lists), participant, collaborator (that is a role)

**Owner**:
The one member who controls a shared list: rounds, conflict rule, roles, membership.

**Decision Maker**:
The at most one member who resolves conflicts; assigned by the Owner, may be the Owner.

**Collaborator**:
A member who is neither Owner nor Decision Maker.

**Invite link**:
A per-member link that lets people join a shared list with a preset role.
_Avoid_: Invitation code, share link

### Accounts

**Guest user**:
Someone using SwipeSort without an account; their lists exist only on their device and are not backed up.
In UI copy this shows as "On this phone only", never as the word "guest".
_Avoid_: Anonymous user, local user, signed-out user

**Backed up**:
A list stored in the user's account rather than only on the device.
_Avoid_: Saved, in the cloud, uploaded

**Synced**:
The state of a member's changes once they have reached the account (as opposed to "Saved on this phone"
while offline). A list is backed up; changes are synced.
_Avoid_: Uploaded, pushed

**Moving lists**:
Bringing a guest user's device lists into their account at sign-in.
_Avoid_: Migration, import, upload

## Flagged ambiguities

- "Guest" means two different things: a person in sample data (an item on a wedding list) and a person
  without an account (guest user). Only the second is a domain term, and neither appears in UI copy.
- "Card" is how an item is displayed; it is not a separate thing from the item.
