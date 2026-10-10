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
      ['S36-default', 'resolve-all'], ['S37-confirm', 'confirm-resolve'],
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
    await page.waitForURL(/04-prototype\/swipe-demo\.html\?deck=mert&count=3/);
    await page.locator('[data-testid="card"]').first().waitFor({ state: 'visible' });
    const s0 = await demoState(page);
    assert.equal(s0.base, 85); assert.equal(s0.total, 100);
    assert.deepEqual(s0.counts, { accept: 50, reject: 21, maybe: 14 });
    assert.equal(await page.locator('#progress-label').innerText(), '85 / 100 decided');
    assert.match(await page.locator('#close').getAttribute('href'), /S09-list-overview\.html#S09-shared-decision-maker$/);
    // Mert's deck holds only items he never decided and that are not open conflicts (c089–c100).
    const first = await page.locator('[data-testid="card"]').first().getAttribute('data-id');
    assert.ok(/^c(089|09\d|100)$/.test(first), `unexpected first card ${first}`);
    h.log.push(`swipe-demo deck=mert&count=3 (keyboard)`);
    for (const [i, key] of [[1, 'ArrowRight'], [2, 'ArrowLeft'], [3, 'ArrowUp']]) { await page.keyboard.press(key); await waitIndex(page, i); }
    assert.equal(await page.locator('#progress-label').innerText(), '88 / 100 decided');
    await page.locator('#done').waitFor({ state: 'visible' });
    assert.match(await page.locator('#done').innerText(), /Done for now[\s\S]*88 of 100 decided\. The prototype skips the rest of the round, and the next screens show the list as it was before this session\./);
    await shot('S25-live-keyboard-done');
    // Lands on the Decision Maker overview, shown as it was before this session (85 / 100).
    await h.frame('S09-shared-decision-maker');
    assert.match(await page.locator('[data-frame="S09-shared-decision-maker"]').innerText(), /85 \/ 100 decided/);
    await h.tap('S09-shared-decision-maker', 'review-conflicts');
    for (let i = 0; i < after.length; i++) await step(1, ...after[i]);
    await h.frame('S39-success-shared');
    await shot('99-exported');
    console.log(`    flow 3 path: ${h.log.join(' → ')} (${h.taps} taps)`);
    h.done();
  },
};
