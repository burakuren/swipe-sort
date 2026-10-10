# Least-privilege permissions and OAuth scopes

When a designed feature needs a sensitive or restricted permission or OAuth scope, we first look for a
workaround that needs less (a system picker, a narrower scope, a user-driven flow); requesting the broader
permission is the last resort. First application: Google Sheets uses only the non-sensitive `drive.file`
scope with Google's Picker, instead of the design's `drive.metadata.readonly` (restricted: yearly CASA
security assessment) and `spreadsheets` / `spreadsheets.readonly` (sensitive: verification, 100-user cap
until verified). Picked files can be read and written, which covers import, tab choice, new columns or a
new tab in the original sheet, and new spreadsheets.

## Consequences

- The in-app "Recent spreadsheets" list and Drive search in S15 are replaced by Google's Picker (web: JS
  Picker; Android: the documented system-browser Picker flow; iOS: same flow, to be verified).
- No Google scope verification lead time, so Google Sheets does not constrain release dates.
- The same rule applies to phone contacts (Android 17 Contact Picker vs `READ_CONTACTS`) and photos (system
  Photo Picker, no `READ_MEDIA_IMAGES`).
