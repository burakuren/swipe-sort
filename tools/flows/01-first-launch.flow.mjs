// Flow 1 (navigation-map §6, DEL-22, SUC-04): first launch → onboarding → import contacts as a guest →
// map fields → review duplicates → sort (live swipe demo) → round summary. Counts the taps from the empty
// home (S08-first-run) to the first decision.
import { helpers, dragCard, demoState, waitIndex } from '../qa/flow-helpers.mjs';

export default {
  name: 'Flow 1: first launch → first decision → round summary (guest)',
  async run({ page, open, assert, shot }) {
    const h = helpers({ page, assert });
    await h.start(open, 'S01-default');
    await h.tap('S01-default', 'next');
    await h.frame('S02-welcome');
    await h.tap('S02-welcome', 'next');
    await h.frame('S02-demo');
    await h.tap('S02-demo', 'next');
    await h.frame('S02-demo-done');
    await h.tap('S02-demo-done', 'get-started');
    await h.frame('S08-first-run');
    await shot('01-home-first-run');
    const tapsBefore = h.taps;
    const t0 = Date.now();
    // No account anywhere on this path (ACC-01): the home is the guest first-run state.
    await h.tap('S08-first-run', 'import-list');
    await h.frame('S11-default');
    await h.tap('S11-default', 'source-contacts');
    await h.frame('S12-contacts');
    await h.tap('S12-contacts', 'continue');
    await h.frame('S13-select-default');
    await h.tap('S13-select-default', 'continue');
    await h.frame('S19-contacts');
    await h.tap('S19-contacts', 'continue');
    await h.frame('S20-default');
    await h.tap('S20-default', 'continue');
    await h.frame('S22-import-pick');
    await shot('02-import-finish');
    await h.tap('S22-import-pick', 'start-sorting');
    await h.frame('S25-coach-1');
    for (const [from, to] of [['S25-coach-1', 'S25-coach-2'], ['S25-coach-2', 'S25-coach-3'], ['S25-coach-3', 'S25-coach-4']]) {
      await h.tap(from, 'next');
      await h.frame(to);
    }
    await h.tap('S25-coach-4', 'done');
    await page.waitForURL(/04-prototype\/swipe-demo\.html\?deck=wedding&count=6&next=S27-default$/);
    await page.locator('[data-testid="card"]').first().waitFor({ state: 'visible' });
    const s0 = await demoState(page);
    assert.equal(s0.index, 0);
    assert.equal(s0.total, 6);
    // First decision: a real drag to the right.
    await dragCard(page, 220, 10);
    await waitIndex(page, 1);
    const tapsToFirstDecision = h.taps - tapsBefore + 1; // + the swipe itself
    h.log.push(`SUC-04: ${tapsToFirstDecision} interactions from S08-first-run to the first decision (${h.taps - tapsBefore} taps + 1 swipe), ${Date.now() - t0} ms of automated time; ${h.taps + 1} interactions from cold start`);
    assert.ok(tapsToFirstDecision <= 15, `first decision needs ${tapsToFirstDecision} interactions`);
    await shot('03-first-decision');
    // Sort the rest: drag left, drag up, keyboard.
    await dragCard(page, -220, 10); await waitIndex(page, 2);
    await dragCard(page, 0, -300); await waitIndex(page, 3);
    for (const [i, key] of [[4, 'ArrowRight'], [5, 'ArrowLeft'], [6, 'ArrowUp']]) {
      await page.keyboard.press(key);
      await waitIndex(page, i);
    }
    const s = await demoState(page);
    assert.deepEqual(s.counts, { accept: 2, reject: 2, maybe: 2 });
    // The demo moves on to the round summary by itself.
    await h.frame('S27-default');
    await shot('04-round-summary');
    console.log(`    flow 1 path: ${h.log.join(' → ')}`);
    h.done();
  },
};
