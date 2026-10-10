# S04 Forgot password

Frames: `S04-forgot-password.html`. Generator: `tools/generators/S04-forgot-password.py`.

## 1. Purpose and requirements

Let someone who signs in with email set a new password, without revealing whether an address has an
account.

Covers: SCR-04, ACC-07, ACC-09, PLT-02, PLT-03, PLT-04, PLT-13, PLT-14, PLT-15, PLT-16, PLT-21, PLT-23,
VIS-11, VIS-12 (Send reset link → Sending… → sent; Save password → Saving… → Password changed), VIS-13.

## 2. Entry points and exits

| From | How |
| --- | --- |
| S03 `S03-email` | "Forgot password?" (email prefilled) |
| S03 `S03-error-locked` | "Reset password" |
| S07 change password | "Forgot your current password?" |
| Reset email | Link `https://swipesort.app/reset?token=…` opens `S04-new-password` in the app (App Link / Universal Link) or `S04-web-desktop` in a browser |

| To | How |
| --- | --- |
| S03 `S03-email` | Back / "Back to sign in" / "Sign in" after success |
| Mail app | "Open email app" |
| `S04-default` | "Send a new link" from `S04-expired` |

## 3. Layout and components

- **Request** (`S04-default`): back AppBar; `text-title-1` "Reset your password"; one `text-body-lg`
  sentence; Email Input; primary lg "Send reset link".
- **Sent** (`S04-sent`): close AppBar; status icon (56 circle, `primary-soft`, `mail-check`); title; body
  with the address in `foreground`; help sentence; "Send again" link (disabled with a countdown); bottom stack:
  primary "Open email app", ghost "Back to sign in".
- **New password** (`S04-new-password`): close AppBar; title; "For {email}"; New password Input (shown as
  text while focused) + PasswordRules (S03); primary "Save password".
- **Result** (`S04-success`, `S04-expired`): status icon (secondary or muted), title, one sentence, bottom
  actions.
- Desktop web: brand header (mark + wordmark) instead of an app bar.

## 4. States

| Frame | Trigger |
| --- | --- |
| `S04-default` | Opened from S03 |
| `S04-sending` | "Send reset link" pressed |
| `S04-invalid-email` | Malformed address on submit |
| `S04-offline` | Offline (banner, button disabled) |
| `S04-send-failed` | Request failed (connection lost) |
| `S04-sent` | Request accepted (always, whether or not the account exists) |
| `S04-resent` | "Send again" after the 60 s cooldown; countdown restarts |
| `S04-new-password` | Valid link opened |
| `S04-new-password-weak` | Submitted with unmet rules |
| `S04-saving` | "Save password" pressed |
| `S04-new-password-offline` | Offline on the new-password step |
| `S04-success` | Password saved |
| `S04-expired` | Link older than 1 hour, already used, or superseded by a newer link |
| `S04-ios`, `S04-ios-new-password` | iOS |
| `S04-web-desktop`, `S04-web-desktop-success` | Link opened in a desktop browser |
| `S04-large-text` | Font scale ≥ 150% (sent) |

## 5. Interactions, gestures and transitions

- "Send reset link": validates format, then requests a link. The response is identical for known and
  unknown addresses (and for Google-only accounts, where the email explains to use Google), so the screen
  can't be used to find out who has an account.
- Cooldown: "Send again in 0:42" counts down from 60 s (disabled control); then it becomes a link. Each
  new link invalidates the previous one.
- "Open email app": Android `Intent.ACTION_MAIN` + `CATEGORY_APP_EMAIL`; iOS `message://`; hidden on web.
- New password: rules live; Save validates; on success all other sessions are signed out; the person signs in
  again with the new password (S03 email, prefilled).
- Transitions: push (shared axis X 300 ms); reduced motion: fade 150 ms.

## 6. Copy

| Element | String |
| --- | --- |
| Back / close labels | "Back to sign in"; "Close"; iOS back "Sign in", iOS "Cancel" |
| Request title | "Reset your password" |
| Request body | "Enter the email you use for SwipeSort. We’ll send a link to set a new password." |
| Field | "Email" |
| Button | "Send reset link" → "Sending…" |
| Invalid email | "Enter a full email address, like name@example.com." |
| Empty email | "Enter your email address." |
| Offline banner | "You're offline. Sending a reset link needs a connection." |
| Send failed | "Couldn't send the link" / "No connection. Check your connection and try again." |
| Sent title | "Check your email" |
| Sent body | "If deniz.yilmaz@example.com has a SwipeSort account, a link to reset its password is on the way. The link works for 1 hour." |
| Sent help | "No email after a few minutes? Check your spam folder, or check that the address is right." |
| Resend | "Send again in 0:42" → "Send again" |
| Resent snackbar | "Sent again. Check your email." |
| Sent buttons | "Open email app", "Back to sign in" |
| New password title | "Set a new password" |
| New password subtitle | "For deniz.yilmaz@example.com" |
| Field | "New password" |
| Rules | "At least 8 characters", "A number or symbol" |
| Weak error | "Use at least 8 characters, with a number or symbol." |
| Button | "Save password" → "Saving…" |
| Offline banner (new) | "You're offline. Saving a new password needs a connection." |
| Success | "Password changed" / "Sign in with your new password. For your security, you’re signed out on your other devices." / "Sign in" |
| Expired | "This link has expired" / "Reset links work for 1 hour and only once. Request a new link to set your password." / "Send a new link" / "Back to sign in" |
| Web success body | "Sign in with your new password here, or in the SwipeSort app on your phone." |
| Reset email (system) | Subject "Reset your SwipeSort password"; body "Use this link to set a new password for deniz.yilmaz@example.com. It works for 1 hour. If you didn’t ask for this, ignore this email; your password stays the same." Button "Set a new password" |
| Google-only email (system) | Subject "Signing in to SwipeSort"; body "This address signs in with Google. Open SwipeSort and choose Continue with Google." |

## 7. Accessibility

- Focus: title first on each step; errors move focus to the field (`aria-invalid`, described by the
  message with icon).
- The countdown is not announced every second; its accessible name is "Send again, available in 42 seconds".
- Status icons are decorative; titles carry the meaning (`S04-sent` title announced as a status).
- Large text: titles wrap; buttons grow; bottom actions stack.
- Buttons ≥ 48; links 48 high.

## 8. iOS and web differences

- **iOS**: back chevron "Sign in"; the new-password step opens as a modal with "Cancel" when the app is
  launched from the link. "Open email app" opens Mail.
- **Web**: the reset link opens `swipesort.app/reset` in the phone column on desktop (`S04-web-desktop`).
  After success the person can sign in in the browser or the app. "Open email app" is hidden on web.
- **Android**: if the link opens while SwipeSort is signed in with another account, the reset still applies
  to the address in the link; the current session is kept.

## 9. Edge cases

- **Google- or Apple-only accounts**: the same "Check your email" screen; the email explains which
  provider to use. A password can be added later in S07.
- **Link opened on another device**: works; the token is single-use.
- **Two links requested**: only the latest works; older ones show `S04-expired`.
- **Typo in the address**: the sent screen repeats the address so the person can notice it.
- **Very long email addresses**: wrap in the body text (no truncation in the confirmation).
- **Offline**: buttons disabled with a banner; nothing is queued.
