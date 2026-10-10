// Flow 2 (navigation-map §6, DEL-23): re-sort the Maybe pile → results → export to Google Sheets.
import { helpers, demoState, waitIndex } from '../qa/flow-helpers.mjs';

export default {
  name: 'Flow 2: re-sort Maybe → results → Google Sheets',
  async run({ page, open, assert, shot }) {
    const h = helpers({ page, assert });
    await h.start(open, 'S09-solo-round-done');
    await h.tap('S09-solo-round-done', 'resort-maybe');
    await h.frame('S24-maybe');
    await h.tap('S24-maybe', 'start-round');
    await page.waitForURL(/04-prototype\/swipe-demo\.html\?deck=desk-maybe&next=S27-desk-round-2$/);
    await page.locator('[data-testid="card"]').first().waitFor({ state: 'visible' });
    const s0 = await demoState(page);
    assert.ok(s0.total > 0, 'Maybe deck is empty');
    h.log.push(`swipe-demo desk-maybe (${s0.total} items)`);
    await shot('01-maybe-deck');
    // Re-sort with the visible buttons (button equivalents of the gestures).
    const order = ['accept', 'reject', 'maybe'];
    for (let i = 0; i < s0.total; i++) {
      await page.locator(`#btn-${order[i % 3]}`).click();
      await waitIndex(page, i + 1);
    }
    await h.frame('S27-desk-round-2');
    await shot('02-round-2-summary');
    await h.tap('S27-desk-round-2', 'review-results');
    await h.frame('S28-default');
    await h.tap('S28-default', 'export');
    await h.frame('S39-default');
    await h.tap('S39-default', 'format-google');
    await h.frame('S39-google-destination');
    await h.tap('S39-google-destination', 'continue');
    await h.frame('S39-google-confirm');
    await shot('03-google-confirm');
    await h.tap('S39-google-confirm', 'confirm-write');
    await h.frame('S39-success-google');
    await shot('04-exported');
    console.log(`    flow 2 path: ${h.log.join(' → ')} (${h.taps} taps)`);
    h.done();
  },
};
