// Flow 3 (navigation-map §6, DEL-24, SUC-05): invite a partner → sign-in prompt → partner opens the link in
// the desktop web app → both sort → conflicts → Decision Maker bulk resolves → export to Google Sheets.
import { helpers } from '../qa/flow-helpers.mjs';

export default {
  name: 'Flow 3: invite → web join → conflicts → bulk resolve → export',
  async run({ page, open, assert, shot }) {
    const h = helpers({ page, assert });
    const steps = [
      ['S09-guest-wedding', 'share'], ['S05-share', 'continue-google'], ['S05-moving', 'next'],
      ['S05-moved', 'continue'], ['S31-default', 'copy-link'], ['S31-link-copied', 'partner-opens-link'],
      ['S32-web-desktop', 'sign-in-to-join'], ['S03-web-desktop', 'continue-google'],
      ['S33-web-desktop', 'start-sorting'], ['S25-web-desktop', 'finish'], ['S27-shared', 'review-conflicts'],
      ['S36-default', 'resolve-all'], ['S37-confirm', 'confirm-resolve'], ['S37-summary', 'export'],
      ['S39-shared', 'format-google'], ['S39-shared-google-destination', 'continue'],
      ['S39-shared-google-confirm', 'confirm-write'],
    ];
    await h.start(open, steps[0][0]);
    for (let i = 0; i < steps.length; i++) {
      const [id, action] = steps[i];
      if (i) await h.frame(id);
      if (/web-desktop/.test(id)) {
        // Desktop web frames: phone column centred in a desktop browser frame (PLT-04), no install needed.
        const desk = await page.locator(`[data-frame="${id}"] .desktop`).count();
        assert.ok(desk > 0, `${id} is not a desktop browser frame`);
        await shot(`${String(i).padStart(2, '0')}-${id}`);
      }
      if (id === 'S25-web-desktop') {
        // Keyboard hints are visible on the desktop sorting frame (PLT-05/06).
        const hints = await page.locator(`[data-frame="${id}"] kbd`).allTextContents();
        for (const k of ['←', '↑', '→', 'Z']) assert.ok(hints.includes(k), `missing keyboard hint ${k}`);
      }
      await h.tap(id, action);
    }
    await h.frame('S39-success-shared');
    await shot('99-exported');
    console.log(`    flow 3 path: ${h.log.join(' → ')} (${h.taps} taps)`);
    h.done();
  },
};
