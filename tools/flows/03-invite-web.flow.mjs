// Flow 3 (navigation-map §6, DEL-24, SUC-05): invite a partner → sign-in prompt → partner opens the link in
// the desktop web app → sorts with the keyboard in the live demo (Mert's undecided items) → Decision Maker
// overview → conflicts → bulk resolve → export to Google Sheets.
import { helpers, demoState, waitIndex } from '../qa/flow-helpers.mjs';

export default {
  name: 'Flow 3: invite → web join → keyboard sort → bulk resolve → export',
  async run({ page, open, assert, shot }) {
    const h = helpers({ page, assert });
    const before = [
      ['S09-guest-wedding', 'share'], ['S05-share', 'continue-google'], ['S05-moving', 'next'],
      ['S05-moved', 'continue'], ['S31-default', 'copy-link'], ['S31-link-copied', 'partner-opens-link'],
      ['S32-web-desktop', 'sign-in-to-join'], ['S03-web-desktop', 'continue-google'],
      ['S33-web-desktop', 'start-sorting'],
    ];
    const after = [
      ['S09-shared-decision-maker', 'review-conflicts'], ['S36-default', 'resolve-all'], ['S37-confirm', 'confirm-resolve'],
      ['S37-summary', 'export'], ['S39-shared', 'format-google'], ['S39-shared-google-destination', 'continue'],
      ['S39-shared-google-confirm', 'confirm-write'],
    ];
    const step = async (i, id, action) => {
      if (i) await h.frame(id);
      if (/web-desktop/.test(id)) {
        // Desktop web frames: phone column centred in a desktop browser frame (PLT-04), no install needed.
        assert.ok(await page.locator(`[data-frame="${id}"] .desktop`).count() > 0, `${id} is not a desktop browser frame`);
        await shot(`${id}`);
      }
      if (action) await h.tap(id, action);
    };
    await h.start(open, before[0][0]);
    for (let i = 0; i < before.length; i++) await step(i, ...before[i]);

    // Mert sorts on the desktop web: keyboard hints shown (PLT-05/06), Close goes to the list overview.
    await step(1, 'S25-web-desktop');
    const hints = await page.locator('[data-frame="S25-web-desktop"] kbd').allTextContents();
    for (const k of ['←', '↑', '→', 'Z']) assert.ok(hints.includes(k), `missing keyboard hint ${k}`);
    assert.match(await page.locator('[data-frame="S25-web-desktop"] [data-action="finish"]').getAttribute('href'), /S09-list-overview\.html#S09-shared-decision-maker$/);
    await h.tap('S25-web-desktop', 'accept');
    await page.waitForURL(/04-prototype\/swipe-demo\.html\?deck=mert/);
    await page.locator('[data-testid="card"]').first().waitFor({ state: 'visible' });
    const s0 = await demoState(page);
    assert.equal(s0.base, 85); assert.equal(s0.total, 100);
    assert.deepEqual(s0.counts, { accept: 50, reject: 21, maybe: 14 });
    assert.equal(await page.locator('#progress-label').innerText(), '85 / 100 decided');
    h.log.push(`swipe-demo deck=mert (${s0.total - s0.base} items, keyboard)`);
    const keys = ['ArrowRight', 'ArrowLeft', 'ArrowUp'];
    const n = (await page.evaluate(() => window.__swipeDemo.state())).total - s0.base;
    for (let i = 0; i < n; i++) { await page.keyboard.press(keys[i % 3]); await waitIndex(page, i + 1); }
    assert.equal(await page.locator('#progress-label').innerText(), '100 / 100 decided');
    await shot('S25-live-keyboard-done');

    for (let i = 0; i < after.length; i++) await step(i + 1, ...after[i]);
    await h.frame('S39-success-shared');
    await shot('99-exported');
    console.log(`    flow 3 path: ${h.log.join(' → ')} (${h.taps} taps)`);
    h.done();
  },
};
