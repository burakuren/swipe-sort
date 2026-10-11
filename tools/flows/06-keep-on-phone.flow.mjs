// Flow 6 (D-33, A-132–A-139): per-list backup. A signed-in Owner turns backup off for a solo list (confirm →
// "on this phone only" with Undo), then shares a list that is on this phone only: it is backed up first.
// Also checks the sign-in "Choose lists" path (A-135, A-142): one list stays on this phone.
import { helpers } from '../qa/flow-helpers.mjs';

export default {
  name: 'Flow 6: keep a list on this phone only → share needs backup → choose lists at sign-in',
  async run({ page, open, assert, shot }) {
    const h = helpers({ page, assert });
    const run = async (steps, end) => {
      await h.start(open, steps[0][0]);
      for (let i = 0; i < steps.length; i++) {
        const [id, action] = steps[i];
        if (i) await h.frame(id);
        await h.tap(id, action);
      }
      await h.frame(end);
      await shot(end);
    };
    // Turn backup off: the switch asks first, because the account copy is deleted.
    await run([['S09-default', 'toggle-backup'], ['S10-backup-off', 'confirm-backup-off']], 'S10-backup-off-done');
    assert.match(await page.locator('[data-frame="S10-backup-off-done"]').innerText(), /is on this phone only/);
    // Sharing a list kept on this phone only backs it up first, then opens Invite.
    await run([['S09-device-only', 'share'], ['S10-share-backup', 'back-up-and-share']], 'S31-default');
    // Sign-in with "Choose lists": one list stays on this phone.
    await run([['S05-share', 'choose-lists'], ['S05-choose-lists', 'done'], ['S05-share-chosen', 'continue-google'],
      ['S05-moving-some-kept', 'next'], ['S05-moved-some-kept', 'continue']], 'S31-default');
    console.log(`    flow 6 path: ${h.log.join(' → ')} (${h.taps} taps)`);
    h.done();
  },
};
