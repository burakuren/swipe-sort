# S07 Profile, connected accounts and account deletion

Frames: `S07-profile.html` (generator: `tools/generators/S07-profile.py`). Components: `01-foundations/components.html`
(ListGroup and rows, Input, AlertDialog, BottomSheet, Snackbar, Alert, OfflineBanner). Sample user: Deniz Yılmaz
(`u-deniz`, deniz.yilmaz@example.com, `images/people/u-deniz.svg`), Owner of `l-wedding` "Wedding guests" (members
`u-mert` Decision Maker, `u-selin` Collaborator) and of the solo lists `l-desk`, `l-photos`, `l-candidates`.

## 1. Purpose and requirements

Lets a signed-in user see and change what other members see (name, photo), manage the ways they sign in, and
delete their account with a clear, honest account of what is deleted and what stays (required by Google Play and
the App Store).

Covers: SET-01, SET-02, SET-12, ACC-06, ACC-07, ACC-08, GOAL-03, DM-15 (ownership hand-over keeps the shared list
running), COL-11 (transfer ownership during deletion), PLT-02, PLT-03, PLT-13–PLT-16, PLT-21, PLT-23, VIS-11–VIS-13,
TERM-01, TERM-02, SCR-07.

## 2. Entry points and exits

| From | How |
| --- | --- |
| S06 Settings (`S06-default`) | Profile row (avatar, name, email) |
| S06 Privacy | "Delete account" link (opens `S07-delete` directly; back returns to Privacy) |

| To | How |
| --- | --- |
| S06 Settings | Back (app bar arrow, system back, iOS edge swipe) |
| Edit name dialog, photo sheet | Pencil button; "Change photo" / "Add photo" |
| System camera / photo picker / browser file picker | Photo sheet (out of scope, OUT-01) |
| Google account chooser (native) | "Connect" on the Google row |
| `S07-add-password`, `S07-change-password` | "Add" / "Change" on the Email and password row |
| S04 Forgot password (`S04-default`) | "Forgot your current password?" |
| S39 Export (`S39-default`) | "Export a list" on the delete page |
| `S07-delete` → `S07-reauth` (when needed) → `S07-delete-confirm` → `S07-delete-dialog` → `S07-deleting` → `S07-deleted` | Delete flow |
| S08 Home first run (`S08-first-run`) | "Done" after deletion (signed out, no lists) |

Pushed in the Settings tab stack (bottom navigation hidden on S07 and its sub-pages, as in every pushed stack
screen). Change password, Add a password, Delete account and Confirm deletion are pushed screens; Edit name and the
final confirmation are dialogs; photo, new Owner and re-authentication are bottom sheets.

## 3. Layout and components

**Profile (`S07-default`)**: AppBar small ("Profile", back). Scrolling column, gutter 20, sections 24 apart:

1. **Photo block** (centered, the only centered element): Avatar 96 (photo or initials "DY" on `muted`) + ghost text
   button with `camera` icon "Change photo" ("Add photo" without a photo).
2. **ListGroup "Personal info"**: Name row (label above value, trailing pencil IconButton 48) and Email row
   (read-only, no trailing control). Footer: "Members of shared lists see your name and photo."
3. **ListGroup "Sign-in methods"** (connected accounts): one row per method with a provider mark, the method name,
   the account address or status, and a trailing text button: Google ("Disconnect" / "Connect"), Apple on iOS
   ("Disconnect"), Email and password ("Change" / "Add"). Footer: "Sign in with any of these. Keep at least one."
4. **ListGroup (single row)**: destructive row "Delete account" with `trash-2` and a description, chevron.

Provider marks: the Google row uses the official multicolor Google "G" mark (24) and the Apple row the Apple logo;
the mockup shows neutral stand-ins (letter G in a circle, Lucide `apple`) because token-only mockups cannot carry
brand colors. The coding agent uses the official assets (see S03 spec §8).

**Delete account, step 1 (`S07-delete`)**: AppBar "Delete account". Lead sentence, then:
- **Shared list you own** (one block per owned shared list): list icon, name, "100 items, 3 members"; RadioGroup
  "Transfer ownership" (default, with a Select-style trigger showing the new Owner, default = the Decision Maker,
  else the member with the most decisions) / "Delete for everyone". Each option has a one-line consequence.
- **ListGroup "Deleted for good"**: profile and sign-in methods; "3 lists only you use" + their names; decisions and
  notes (including on lists shared with you).
- **ListGroup "Not changed"**: imported files and Google Sheets; exported files.
- Export hint + link "Export a list".
- Bottom action stack (sticky, `border-t`): primary "Continue", ghost "Keep my account".

**Confirm deletion (`S07-delete-confirm`)**: summary card (moves, deletes), Input "To confirm, type delete" with
helper "Lowercase is fine.", destructive lg "Delete account" (disabled until the input equals "delete", trimmed,
case-insensitive) + ghost "Keep my account".

**Deleting / deleted**: full-screen centered status; no app bar (nothing can be cancelled mid-way); deleted screen
has a neutral check in a `muted` circle (not the Accept color) and a bottom "Done".

**Change password / Add a password**: AppBar + form (Input with show/hide toggle, live password rules list from
S03) + sticky bottom "Save password".

## 4. States and triggers

| Frame | Trigger |
| --- | --- |
| `S07-default` | Signed in with Google and a password |
| `S07-edit-name` | Pencil on the Name row: dialog with the current name selected |
| `S07-edit-name-error` | Name emptied (only spaces counts as empty): inline error, Save disabled |
| `S07-change-photo` | "Change photo": sheet with Take photo, Choose from gallery, Remove photo |
| `S07-photo-uploading` | Photo chosen: scrim + spinner over the avatar, "Uploading photo…" |
| `S07-no-photo` | Photo removed: initials, "Add photo", snackbar "Photo removed" with Undo |
| `S07-google-not-connected` | Account created with email (no Google): Google row "Not connected" + "Connect" |
| `S07-disconnect-confirm` | "Disconnect" on Google while another method exists |
| `S07-google-disconnected` | Confirmed: row switches to Connect, snackbar "Google disconnected" |
| `S07-google-only` | Google is the only method: Email and password row shows "No password yet" + "Add" |
| `S07-disconnect-blocked` | "Disconnect" on the only method: dialog asks to add a password first |
| `S07-add-password` | "Add" / "Add a password": email shown read-only, new password with rules |
| `S07-change-password` | "Change": current + new password; Save disabled until rules pass |
| `S07-change-password-error` | Current password wrong: inline error on that field |
| `S07-change-password-saving` | Save pressed: button "Saving…" (busy) |
| `S07-password-changed` | Saved: back on Profile, snackbar "Password changed. Other devices were signed out." |
| `S07-delete` | "Delete account" row |
| `S07-delete-scrolled` | Same page scrolled: "Not changed" and the export hint |
| `S07-delete-everyone` | "Delete for everyone" chosen for Wedding guests |
| `S07-delete-transfer` | New Owner trigger: sheet with members (role and progress) |
| `S07-reauth` | "Continue" when the last sign-in is older than 5 minutes (server returns "recent login required"): sheet to sign in again; also used before Disconnect and Change password when required |
| `S07-delete-confirm` | After Continue (and re-auth when needed); "delete" typed, button enabled |
| `S07-delete-confirm-empty` | Nothing typed yet: Delete account disabled |
| `S07-delete-dialog` | "Delete account" pressed: final AlertDialog |
| `S07-deleting` | Confirmed: full-screen progress, back disabled |
| `S07-deleted` | Server confirmed: local data wiped, signed out |
| `S07-delete-failed` | Request failed or timed out: nothing deleted, "Try again" |
| `S07-offline` | No connection: offline banner; photo, name, method and delete actions disabled with reason |
| `S07-ios` | iOS: Apple + Google + password methods, grouped inset lists, back chevron "Settings" |
| `S07-ios-delete-alert` | iOS final confirmation as a native alert |
| `S07-web-change-photo` | Web: sheet offers "Upload photo" (file input) and Remove photo |
| `S07-large-text` | 200% text: rows stack, trailing actions move below the row text |

## 5. Interactions, gestures and transitions

- **Edit name**: dialog (scale 0.96 → 1 + fade 250 ms; reduced motion: fade 150 ms). Save trims the value
  (1–60 characters); the new name syncs to every shared list. Save is disabled while empty. Offline: pencil disabled.
- **Photo**: Take photo / Choose from gallery open the system camera or picker (permission prompts are system UI);
  the image is center-cropped square, resized to 512 px and uploaded; the avatar shows a spinner overlay. Remove
  photo is instant with an Undo snackbar (6 s). Upload failure: snackbar "Photo didn't upload. Check your connection
  and try again." with "Try again"; the previous photo stays.
- **Connect Google**: opens the native Google account chooser. If the Google account is already used by another
  SwipeSort account: snackbar error "This Google account is already linked to another SwipeSort account." If the
  user cancels the chooser: nothing changes, no message.
- **Disconnect** (Google or Apple): allowed only while at least one other method remains; otherwise
  `S07-disconnect-blocked` → "Add a password" opens `S07-add-password`, and after saving returns to Profile where
  Disconnect now works.
- **Change password**: rules update live; Save enabled when both rules pass and the current password is filled.
  On success, other sessions are signed out (this device stays signed in) and Profile shows the snackbar.
  "Forgot your current password?" opens S04 with the email prefilled.
- **Delete flow**: Continue → re-auth sheet if required (Continue with Google re-runs the chooser; password +
  Confirm checks the password) → Confirm deletion → type "delete" → Delete account → final dialog → Deleting →
  Deleted → Done. Back from step 2 returns to step 1 keeping the transfer choice. System back is ignored on
  Deleting. The new Owner is notified ("Deniz made you the Owner of Wedding guests", S38 role changed event) and
  the list keeps its rounds, decisions of other members, conflict rule and Decision Maker.
- **After deletion**: local database and caches are wiped, the session is cleared, notifications are unregistered;
  S08 opens in its first-run state.
- Snackbars: 4 s, with action 6 s (motion.md §3). Sheets: 300 ms enter, drag down or back to close.

## 6. Copy

| Element | String |
| --- | --- |
| App bar | "Profile"; back label "Back to Settings" |
| Photo | "Change photo"; "Add photo"; alt "Profile photo of Deniz Yılmaz"; no photo label "Deniz Yılmaz, no profile photo"; "Uploading photo…" |
| Photo sheet | "Profile photo"; "Take photo"; "Choose from gallery"; "Remove photo"; web: "Upload photo", "JPG or PNG, up to 10 MB" |
| Photo snackbars | "Photo removed" + "Undo"; "Photo didn't upload. Check your connection and try again." + "Try again" |
| Personal info | Header "Personal info"; "Name"; "Email"; edit button label "Edit name"; footer "Members of shared lists see your name and photo." |
| Edit name dialog | "Edit name"; "Use the name your partner, family or team will recognize."; field "Name"; helper "Members of shared lists see this name."; error "Enter a name. Members see it on shared lists."; "Cancel"; "Save" |
| Sign-in methods | Header "Sign-in methods"; "Google"; "Apple"; "Email and password"; "Not connected"; "Password set"; "No password yet"; actions "Connect", "Disconnect", "Change", "Add"; accessible names "Connect Google", "Disconnect Google", "Disconnect Apple", "Change password", "Add a password"; footer "Sign in with any of these. Keep at least one." |
| Disconnect dialog | "Disconnect Google?"; "You'll sign in with deniz.yilmaz@example.com and your password instead. Your lists aren't affected."; "Cancel"; "Disconnect" (Apple: "Disconnect Apple?" with the same body) |
| Disconnected | "Google disconnected" |
| Blocked dialog | "Add a password first"; "Google is your only way to sign in. Add a password so you can still sign in after disconnecting Google."; "Cancel"; "Add a password" |
| Connect error | "This Google account is already linked to another SwipeSort account." |
| Add a password | Title "Add a password"; "Add a password to sign in with your email address as well as with Google."; "Email"; "New password"; rules "At least 8 characters", "A number or a symbol"; "Save password" |
| Change password | Title "Change password"; "Current password"; "Forgot your current password?"; "New password"; rules as above; "After you change it, other phones and browsers signed in to your account are signed out."; "Save password"; "Saving…"; error "That password isn't right. Try again or reset it." |
| Password toggle | "Show password"; "Hide password" |
| Password changed | "Password changed. Other devices were signed out." |
| Delete row | "Delete account"; "Delete your account, your lists and your notes"; offline: "Connect to the internet to delete your account." |
| Delete step 1 | Title "Delete account"; "Deleting your account can't be undone. Here's what happens."; "Shared list you own"; "{List name}"; "100 items, 3 members"; "Transfer ownership"; "Mert and Selin keep the list. Your decisions and notes on it are removed."; new Owner trigger label "New Owner: Mert Aydın. Change"; "Delete for everyone"; "Mert and Selin lose access to the list." |
| Deleted for good | Header "Deleted for good"; "Your profile and sign-in methods"; "3 lists only you use"; "Desk setup, March photos clean-up, Frontend hiring, Q4"; "Your decisions and notes"; "Including those on lists other people share with you" |
| Not changed | Header "Not changed"; "Files and Google Sheets you imported from"; "SwipeSort never changed them"; "Files you exported" |
| Export hint | "Want a copy first? Export a list before you delete your account."; link "Export a list" |
| Step 1 actions | "Continue"; "Keep my account" |
| New Owner sheet | "New Owner of Wedding guests"; "The new Owner can start rounds, manage members and change the conflict rule."; "Mert Aydın", "Decision Maker, 85 / 100 decided"; "Selin Yılmaz", "Collaborator, 43 / 100 decided"; "Choose Mert Aydın" |
| Re-authentication | "Confirm it's you"; "For your security, sign in again before you delete your account." (Change password / disconnect: "…before you change your password." / "…before you disconnect Google."); "Continue with Google"; "or"; "Password"; placeholder "Your SwipeSort password"; "Confirm"; error "That password isn't right. Try again or reset it." |
| Confirm deletion | Title "Confirm deletion"; "This is the last step. After this, your account can't be restored."; "Wedding guests moves to Mert Aydın"; "Desk setup, March photos clean-up and Frontend hiring, Q4 are deleted"; "Your profile, decisions and notes are deleted"; field "To confirm, type delete"; helper "Lowercase is fine."; "Delete account"; "Keep my account" (with Delete for everyone: "Wedding guests is deleted for all 3 members") |
| Final dialog | "Delete your account?"; "This can't be undone. Wedding guests moves to Mert Aydın. Your other 3 lists, your decisions and your notes are deleted."; "Cancel"; "Delete account" |
| Deleting | "Deleting your account…"; "Keep SwipeSort open. This takes a few seconds." |
| Deleted | "Your account is deleted"; "Mert Aydın now owns Wedding guests. You can keep using SwipeSort without an account."; "Done" (without a transfer: "Your lists and notes are gone from SwipeSort. You can keep using SwipeSort without an account.") |
| Delete failed | "Couldn't delete your account"; "Nothing was deleted. Check your connection and try again."; "Try again"; "Keep my account" |
| Offline | "You're offline. Profile changes need a connection." |
| Large text | Same strings |

## 7. Accessibility

- Focus order: Back, photo, Change photo, Name (Edit name), Email, each sign-in method and its action, Delete
  account. Section headers are headings (`h2`).
- Trailing text buttons carry full accessible names ("Disconnect Google", "Change password") because "Change" alone
  is ambiguous. The pencil button is "Edit name".
- Avatar: photo alt "Profile photo of Deniz Yılmaz"; initials fallback is an image with "Deniz Yılmaz, no profile
  photo". Uploading announces "Uploading photo…" (polite).
- Dialogs: `alertdialog` for Disconnect, blocked and final delete; `dialog` for Edit name. Focus moves to the dialog;
  initial focus on Cancel for destructive dialogs (never on the destructive button).
- Delete step 1 options are a radiogroup with consequences in the option description; the new Owner trigger reads
  "New Owner: Mert Aydın. Change".
- Typed confirmation: the disabled Delete account button is announced as disabled ("Type delete to enable").
  Deleting is a live region; Deleted moves focus to the heading.
- Errors: icon + text, `aria-invalid` and `aria-describedby` on the field. Password rules are a labeled list with
  "done" / "missing" suffixes for screen readers.
- Offline: disabled controls keep their names; reasons are full-contrast text (never opacity-dimmed).
- Large text (`S07-large-text`): rows stack name and address, trailing actions move below as full-width-tappable
  text buttons ≥ 48; email wraps (break-all) instead of truncating.
- Touch targets ≥ 48 everywhere (text buttons `h-12`, icon buttons `size-12`).

## 8. iOS and web differences

- **iOS** (`S07-ios`, `S07-ios-delete-alert`): back chevron with "Settings" and edge-swipe back; grouped inset lists
  (12 radius) without group footers to keep the compact rhythm; Sign in with Apple appears as a sign-in method
  (Connect / Disconnect; Apple accounts may show a private relay address). Photo sheet becomes an action sheet with
  the same items. Final confirmation is a native alert with the same copy; "Delete account" is the destructive
  action, "Cancel" the bold default. **Account deletion must revoke the Sign in with Apple token** (Apple REST
  `auth/revoke`) as App Store guideline 5.1.1(v) requires; the server does this during `S07-deleting`.
- **Android**: Material 3 dialogs and bottom sheets as shown; system back closes sheet/dialog first. Google Play
  also requires a web route to request deletion: the same flow is reachable on the web at
  `swipesort.app/account/delete` after sign-in.
- **Web** (`S07-web-change-photo`): photo uses a file input ("Upload photo", JPG or PNG up to 10 MB); no camera or
  gallery items. Apple is not offered on web (it stays listed if already connected on an iPhone, with Disconnect).
  Desktop uses the centered phone column (S40) with no other changes. Everything else is identical.

## 9. Edge cases

- **Only one sign-in method**: Disconnect is blocked (`S07-disconnect-blocked`); there is never a state with zero
  methods.
- **Several shared lists owned**: step 1 shows one block per list, each with its own transfer/delete choice;
  Continue is enabled once every list has a choice (transfer is preselected, so it always is).
- **Shared list where the user is the only remaining member** (others left): treated as a solo list and listed under
  "Deleted for good".
- **Member of shared lists owned by others**: they keep the list; the user's decisions and notes are removed and
  statuses recompute without them (as when a member is removed with "Discard their decisions", DM-17).
- **Unsynced changes on this phone**: deletion discards them; step 1 adds nothing extra because everything is being
  deleted anyway; the server deletion is authoritative.
- **Deletion interrupted** (app killed during `S07-deleting`): on next start the app retries the request silently;
  if the account is already deleted, S08 first run opens.
- **Long names** (40+ chars): name wraps to 2 lines in the row; app bar never shows the name.
- **Long email / Apple relay address**: truncates with ellipsis in rows (full value in the accessible name); wraps
  in large text.
- **Offline**: everything readable; changes disabled with the banner reason; delete row explains it needs a
  connection.
- **Re-auth cancelled**: returns to step 1 with nothing changed.
- **Google token expired** (Google row): row shows "Sign in again" instead of the address; tapping re-runs the chooser.
