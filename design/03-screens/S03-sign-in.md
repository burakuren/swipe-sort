# S03 Sign up / sign in

Frames: `S03-sign-in.html`. Generator: `tools/generators/S03-sign-in.py`.

## 1. Purpose and requirements

One place to sign in or create an account with Google, email (and Apple on iOS). It is always optional:
SwipeSort works fully without an account; signing in adds backup, other devices and sharing.

Covers: SCR-03, ACC-01, ACC-03, ACC-04 (context line), ACC-06, ACC-07, ACC-08, ACC-09 (entry to S04),
COL-04 (web sign-in to join), SUC-05, PLT-02, PLT-03, PLT-04, PLT-13, PLT-14, PLT-15, PLT-16, PLT-21,
PLT-23, STK-07, VIS-11, VIS-12, VIS-13, GOAL-03, DEL-24 (flow 3).

## 2. Entry points and exits

| From | How |
| --- | --- |
| S02 welcome / recap | "I have an account" |
| S05 sign-in prompt | "Continue with email" (opens `S03-context-share` or `S03-context-backup`) |
| S06 Settings (not signed in) | Sign-in card |
| S32 web (invite link in a browser) | "Sign in to join" → `S03-web-desktop` / mobile web |

| To | How |
| --- | --- |
| Origin | Close (`x`, Android/web) or Cancel (iOS); system back |
| `S03-email` | "Continue with email" |
| `S03-sign-up` ↔ `S03-email` | "Create an account" / "Sign in" links |
| S04 `S04-default` | "Forgot password?" (email prefilled) |
| Google account chooser / Apple sheet | Native, out of scope; returns to `S03-google-busy` |
| After success, no lists on this device | Back to the origin (S08, S06) signed in; snackbar "Signed in as deniz.yilmaz@example.com" on the origin |
| After success, lists on this device | S05 `S05-moving` (lists move to the account), then the origin action continues |
| After success from an invite (web) | S33 `S33-web-desktop` (`data-action="continue-google"`) |

## 3. Layout and components

Auth modal (full-screen on Android and web, page sheet on iOS).

- **Chooser** (`S03-default`): modal AppBar with close; mark (56); `text-title-1` "Sign in to SwipeSort"
  and one `text-body-lg` line; or, from S05, the heading "Sign in or create an account" with an info Alert
  (primary-soft, icon of the purpose). Button stack (lg, 56): iOS Apple (`bg-foreground`, system button),
  Google (outline, Google mark), email (outline, `mail`). A muted note under the buttons. Terms line pinned at
  the bottom (`text-body-sm`, two links).
- **Email sign-in** (`S03-email`): back AppBar; `text-title-1` title; Input Email (`type=email`,
  `autocomplete=email`); Input Password with show/hide icon button (`autocomplete=current-password`);
  "Forgot password?" link right-aligned; primary lg "Sign in"; footer "New to SwipeSort? Create an account".
- **Create account** (`S03-sign-up`): Name (helper "Shown to members of lists you share."), Email,
  Password (`new-password`, shown as text while focused by default on Android) + **PasswordRules** (Proposed:
  list of rules with `circle` → `circle-check`, failure `circle-alert` destructive), primary "Create account",
  footer link to sign in.
- **Account errors**: error Alert above the fields with a specific action button (secondary, 48).
- **Web desktop** (`S03-web-desktop`): desktop frame, phone column; brand header (mark + wordmark); title
  "Sign in to join"; inviter card (group surface: Deniz's avatar, "Deniz Yılmaz invited you to", list name,
  item count); Google and email buttons; note; terms.

## 4. States

| Frame | Trigger |
| --- | --- |
| `S03-default` | Opened from S02 or S06 |
| `S03-context-share` / `S03-context-backup` | Opened from S05 (share / backup) via "Continue with email" |
| `S03-email` | "Continue with email" |
| `S03-signing-in` | "Sign in" pressed; fields and links stay visible, button busy |
| `S03-sign-up` | "Create an account"; rules update per keystroke |
| `S03-creating` | "Create account" pressed with valid input |
| `S03-error-wrong-password` | Server: wrong password |
| `S03-error-invalid-email` | Client validation on submit (not while typing) |
| `S03-error-account-exists` | Create account with an email that has an account |
| `S03-error-uses-google` | Email sign-in for an account that only has Google (no password) |
| `S03-error-weak-password` | Create account submitted with an unmet rule |
| `S03-error-locked` | 5 wrong passwords within 15 minutes |
| `S03-error-no-connection` | Request failed: no network |
| `S03-google-busy` | Returned from the Google chooser, exchanging the token |
| `S03-google-cancelled` | Person closed the Google chooser |
| `S03-google-failed` | Google returned an error or timed out (10 s) |
| `S03-offline` | Opened while offline (or connection lost on the chooser) |
| `S03-email-offline` | Offline on the email form |
| `S03-large-text` | Font scale ≥ 150% |
| `S03-ios`, `S03-ios-context-share`, `S03-ios-email` | iOS |
| `S03-web` | Mobile browser |
| `S03-web-desktop`, `S03-web-desktop-email` | Desktop browser, invited member joining (flow 3) |

## 5. Interactions, gestures and transitions

- Provider buttons open the native flows (`expo-auth-session`/Google Sign-In, `expo-apple-authentication`).
  While waiting for the result, the tapped button shows "Signing in…" and the others are disabled.
- Email: "Sign in" validates the email format first (inline error), then calls the server. Errors keep the
  typed values; focus moves to the first field with an error.
- Password field: eye button toggles visibility (label switches "Show password" / "Hide password").
- Password rules (sign-up and S04): at least 8 characters; at least one number or symbol. Rules turn
  checked live; unmet rules turn into errors only on submit.
- Account exists → "Sign in instead" opens `S03-email` with the email prefilled.
- Uses Google → the inline Google button starts Google sign-in.
- Locked → "Reset password" opens S04; sign-in re-enables after 15 minutes.
- Success: success haptic; the modal closes (or hands off to S05 moving / S33 join). On Android the
  password manager (Autofill / Credential Manager) is offered to save the new credentials.
- Push transitions inside the auth stack: shared axis X 300 ms; reduced motion: fade 150 ms.
- Snackbar on cancel: 4 s, polite.

## 6. Copy

| Element | String |
| --- | --- |
| Close / back labels | "Close"; "Back" (iOS "Cancel", back chevron "Sign in") |
| Chooser title | "Sign in to SwipeSort" |
| Chooser body | "Back up your lists, use them on other devices and decide together with others." |
| Context heading | "Sign in or create an account" |
| Context share | "Sign in to share “Wedding guests”" / "Members sort the same list on their own phones. Your 4 lists on this phone move to your account." (pattern: list name and count are live) |
| Context backup | "Sign in to back up your lists" / "Your 4 lists move to your account, so they are safe if you lose this phone." |
| Buttons | "Continue with Apple", "Continue with Google", "Continue with email" |
| Note | "Signing in is optional. Without an account, lists stay on this phone." |
| Offline banner | "You're offline. Signing in needs a connection." |
| Offline note | "Your lists stay on this phone. Try again when you're online." |
| Terms | "By continuing, you agree to the Terms of Service and Privacy Policy." |
| Email title | "Sign in with email" |
| Labels | "Email", "Password", "Name", "New password" (S04) |
| Name helper | "Shown to members of lists you share." |
| Links | "Forgot password?", "New to SwipeSort? Create an account", "Already have an account? Sign in" |
| Sign in button | "Sign in" → "Signing in…" |
| Create title / button | "Create an account"; "Create account" → "Creating account…" |
| Password rules | "At least 8 characters", "A number or symbol"; screen reader suffixes ", done" / ", missing" |
| Show password | "Show password" / "Hide password" |
| Wrong password | "Wrong password. Try again or reset it." |
| Invalid email | "Enter a full email address, like name@example.com." |
| Empty email (on submit) | "Enter your email address." |
| Empty password (on submit) | "Enter your password." |
| Empty name (on submit) | "Enter your name." |
| Account exists | "An account with this email already exists" / "Sign in instead. If you forgot the password, you can reset it." / "Sign in instead" |
| Uses Google | "This email signs in with Google" / "Continue with Google to open your account. You can add a password later in Profile." / "Continue with Google" |
| Uses Apple (iOS, same pattern) | "This email signs in with Apple" / "Continue with Apple to open your account." / "Continue with Apple" |
| Weak password | "Add a number or symbol to your password." (too short: "Use at least 8 characters.") |
| Locked | "Too many attempts" / "For your security, sign-in is paused for 15 minutes. You can reset your password now." / "Reset password" |
| No connection | "Couldn't sign in" / "No connection. Check your connection and try again. Your lists stay on this phone." |
| Google busy | "Signing in…" |
| Google cancelled (snackbar) | "Google sign-in cancelled. Choose a way to continue." |
| Google failed | "Google sign-in didn't work" / "Check your connection and try again, or continue with email." |
| Apple failed (iOS) | "Apple sign-in didn't work" / "Try again, or continue with Google or email." |
| Success snackbar (on origin) | "Signed in as deniz.yilmaz@example.com" |
| Web join title | "Sign in to join" |
| Web join body | "No app needed. You can sort right here in your browser." |
| Inviter card | "Deniz Yılmaz invited you to" / "Wedding guests" / "100 items" |
| Web join note | "Next, you'll see the list and your role before joining." |

## 7. Accessibility

- Focus order: Close, (context alert), heading, provider buttons top to bottom, note, terms links. Form:
  Back, heading, alert (if any), Email, Password, Show password, Forgot password?, Sign in, Create an account.
- Inputs have visible labels, `autocomplete` and `type` for autofill and password managers.
- Errors: `aria-invalid` + `aria-describedby` pointing to the message (icon + text, never color alone);
  account-level alerts use `role="alert"` and receive focus.
- Busy buttons set `aria-busy` and announce "Signing in…".
- Provider marks are decorative; the button label names the provider.
- Large text (`S03-large-text`): mark hidden, buttons grow to 64+ and wrap; terms grow too.
- Touch targets: all buttons ≥ 48; inline links are 48 high.

## 8. iOS and web differences

- **iOS**: page sheet with "Cancel"; **Sign in with Apple first** (App Store Review Guideline 4.8, HIG), as
  the system `AppleAuthenticationButton` (black in light mode, white in dark mode, "Continue with Apple").
  Hide My Email relay addresses are accepted and shown as-is in S07. Back chevron in the email form.
- **Web**: Google uses the Google Identity Services popup; no Apple button (Apple is iOS-only by brief).
  Mobile browsers use the Android layout without system bars. Desktop browsers show the phone column;
  in flow 3 the invited member signs in here and goes straight to S33.
- **Provider marks**: the mockups use stand-ins (a "G" in a circle, Lucide `apple`). Implementation must use
  the official multicolor Google "G" per Google Identity branding guidelines and the native Apple button;
  these brand assets are the only allowed non-token colors.

## 9. Edge cases

- **Signing in with lists on this device**: always moved to the account (S05 moving); nothing is
  replaced or merged item-by-item; lists keep their names (duplicates get " (2)" only if the account already
  has a list with the same name).
- **Same email on Google and email/password**: accounts are linked by verified email; signing in with
  either opens the same account.
- **Email typos**: whitespace trimmed; email compared case-insensitively.
- **Very long names** (Name field): 60 characters max; shown truncated in rows, full in S07.
- **Password managers / passkeys**: autofill is supported; passkeys are out of scope for v1.
- **Offline mid-request**: `S03-error-no-connection`; nothing changes on the device.
- **Session expiry later**: handled by S07 re-authentication, not here.
- **Invite link + already signed in on web**: S03 is skipped; S32 goes straight to S33.
