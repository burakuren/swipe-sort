// Flow 7 (D-18, A-153–A-155): contacts on iOS and Android 17+ come from the system contact picker (not drawn),
// then our review list; no permission explainer. Android 16 and lower keep flow 1's S12 → S13 path.
import { helpers } from '../qa/flow-helpers.mjs';

export default {
  name: 'Flow 7: contacts through the system picker → review → field mapping',
  async run({ page, open, assert, shot }) {
    const h = helpers({ page, assert });
    const steps = [['S11-ios', 'source-contacts'], ['S13-picker-intro-ios', 'open-picker']];
    await h.start(open, steps[0][0]);
    for (let i = 0; i < steps.length; i++) {
      const [id, action] = steps[i];
      if (i) await h.frame(id);
      await h.tap(id, action);
    }
    await h.frame('S13-picked-ios');
    await shot('S13-picked-ios');
    // Android 17+: the same path from the intro.
    await h.start(open, 'S13-picker-intro');
    await h.tap('S13-picker-intro', 'open-picker');
    await h.frame('S13-picked');
    await h.tap('S13-picked', 'continue');
    await h.frame('S19-contacts');
    await shot('S19-contacts');
    console.log(`    flow 7 path: ${h.log.join(' → ')} (${h.taps} taps)`);
    h.done();
  },
};
