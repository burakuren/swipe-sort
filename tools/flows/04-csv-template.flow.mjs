// Flow 4 (navigation-map §6, DEL-25): create a list from CSV with a custom card template. Since the design
// update the candidate CVs are kept on this phone only at the import finish (D-33, A-168).
import { helpers } from '../qa/flow-helpers.mjs';

export default {
  name: 'Flow 4: list from CSV with a custom template',
  async run({ page, open, assert, shot }) {
    const h = helpers({ page, assert });
    const steps = [
      ['S08-default', 'new-list'], ['S11-default', 'source-csv'], ['S14-default', 'choose-file'],
      ['S14-csv-preview', 'continue'], ['S19-csv', 'continue'], ['S20-none', 'continue'],
      ['S22-import-pick-csv', 'toggle-backup'], ['S22-import-pick-device-only', 'customize-template'], ['S23-default', 'save-template'], ['S23-save', 'confirm-save'],
      ['S22-import-pick-custom', 'start-sorting'],
    ];
    await h.start(open, steps[0][0]);
    for (let i = 0; i < steps.length; i++) {
      const [id, action] = steps[i];
      if (i) await h.frame(id);
      await h.tap(id, action);
    }
    await h.frame('S25-candidate');
    await shot('01-sorting-candidates');
    // The custom template is applied: the sorting frame shows the progress and decision buttons.
    const text = await page.locator('[data-frame="S25-candidate"]').innerText();
    assert.match(text, /\d+ \/ \d+ decided/);
    for (const label of ['Reject', 'Maybe', 'Accept', 'Undo']) assert.ok(text.includes(label), `S25-candidate lacks ${label}`);
    console.log(`    flow 4 path: ${h.log.join(' → ')} (${h.taps} taps)`);
    h.done();
  },
};
