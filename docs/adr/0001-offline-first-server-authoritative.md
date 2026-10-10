# Offline-first, server-authoritative data architecture

SwipeSort is **offline-first and server-authoritative**, not "local-first" in the strict sense (devices
merging peer-to-peer without an authority). Shared lists need an authority for roles, conflict rules,
Decision Maker resolutions and membership, which peers cannot settle alone; and sorting must still work
offline, with guest lists that never leave the device.

Rules:

1. The UI reads only the local database. No screen waits on the network to show data.
2. Offline writes apply locally first and are queued for upload.
3. For account data the server is the authority: it validates every queued write, may reject or adjust it,
   and devices converge to the server's version.
4. An action is online-only if it needs server-only knowledge, changes what other members may do or see,
   or destroys shared data. Everything else is queued and validated by the server on arrival.
5. Guest data is device-authoritative. It moves to the server once, at sign-in (moving lists); rule 3
   applies afterwards.

## Considered Options

- **Strict local-first (CRDTs, server optional):** rejected; group rules need a single authority.
- **Cloud-first with a cache:** rejected; guest mode and offline sorting need a full local replica.

## Consequences

Online-only today (rule 4): bulk resolve, start a round on a shared list, change the conflict rule,
create an invite link, join, roles / Decision Maker / remove / transfer ownership, leave a list, archive
or delete for everyone, account deletion. Queued: decisions, undo, notes, field edits, everything on solo
lists, rename, change card template, add items, resolve a single conflict. The handoff's working proposal
called this "local-first"; the behavior is the same, the name is corrected.
