// Swipe demo (DEL-16, PRC-02, SRT-02–SRT-08, PLT-05, PLT-17): mouse drags right, left and up, a short drag
// that snaps back, a down drag that never decides, Undo (button and Z), arrow-key decisions, and
// ?reduced=1. Fails on any console error or failed request.
import { helpers, dragCard, demoState, waitIndex } from '../qa/flow-helpers.mjs';

export default {
  name: 'Swipe demo: drags, snap back, undo, keyboard, reduced motion',
  async run({ page, open, assert, shot }) {
    const h = helpers({ page, assert });
    await open('04-prototype/swipe-demo.html');
    const base = page.url().split('?')[0];
    await page.goto(`${base}?deck=desk`);
    const card = () => page.locator('[data-testid="card"]').first();
    await card().waitFor({ state: 'visible' });
    let s = await demoState(page);
    assert.equal(s.index, 0);
    assert.deepEqual(s.counts, { accept: 0, reject: 0, maybe: 0 });
    assert.equal(await page.locator('#progress-label').innerText(), `0 / ${s.total} decided`);

    // 1. Drag right: while dragging past the threshold the card tilts, tints and shows the Accept stamp.
    const b = await card().boundingBox();
    const cx = b.x + b.width / 2, cy = b.y + b.height / 2;
    await page.mouse.move(cx, cy);
    await page.mouse.down();
    for (let i = 1; i <= 12; i++) await page.mouse.move(cx + (180 * i) / 12, cy + 4);
    const fb = await page.evaluate(() => {
      const el = document.querySelector('[data-testid="card"]');
      return { transform: el.style.transform, stamp: el.querySelector('[data-stamp]').textContent.trim(), stampOpacity: +el.querySelector('[data-stamp]').style.opacity, tint: +el.querySelector('[data-tint]').style.opacity };
    });
    assert.match(fb.transform, /rotate\((?!0deg)/, `no tilt while dragging: ${fb.transform}`);
    assert.equal(fb.stamp, 'Accept');
    assert.ok(fb.stampOpacity > 0.9 && fb.tint > 0, `feedback not armed: ${JSON.stringify(fb)}`);
    await shot('01-drag-accept-armed');
    await page.mouse.up();
    await waitIndex(page, 1);
    s = await demoState(page);
    assert.deepEqual(s.counts, { accept: 1, reject: 0, maybe: 0 });

    // 2. Drag left → Reject. 3. Drag up → Maybe.
    await dragCard(page, -220, 6); await waitIndex(page, 2);
    await dragCard(page, 10, -320); await waitIndex(page, 3);
    s = await demoState(page);
    assert.deepEqual(s.counts, { accept: 1, reject: 1, maybe: 1 });
    assert.equal(await page.locator('#progress-label').innerText(), `3 / ${s.total} decided`);
    // Button counts follow the state.
    for (const d of ['accept', 'reject', 'maybe']) assert.equal(await page.locator(`#btn-${d} [data-count]`).innerText(), '1');

    // 4. Short, slow drag (below threshold and fling velocity) snaps back.
    await dragCard(page, 40, 0, { steps: 8, slow: true });
    await page.waitForTimeout(450);
    s = await demoState(page);
    assert.equal(s.index, 3, 'short drag must not decide');
    assert.match(await card().evaluate((el) => el.style.transform), /translate\(0px, 0px\)/);
    // 5. Dragging down never decides (A-30).
    await dragCard(page, 0, 300); await page.waitForTimeout(450);
    assert.equal((await demoState(page)).index, 3, 'down drag must not decide');

    // 6. Undo with the button, then with Z: steps back in order.
    await page.locator('#btn-undo').click();
    await waitIndex(page, 2);
    assert.match(await page.locator('#snackbar').innerText(), /^Undid Maybe on /);
    await page.keyboard.press('z');
    await waitIndex(page, 1);
    s = await demoState(page);
    assert.deepEqual(s.counts, { accept: 1, reject: 0, maybe: 0 });
    assert.match(await page.locator('#snackbar').innerText(), /^Undid Reject on /);

    // 7. Arrow keys decide (PLT-05).
    for (const [key, n] of [['ArrowRight', 2], ['ArrowLeft', 3], ['ArrowUp', 4]]) { await page.keyboard.press(key); await waitIndex(page, n); }
    s = await demoState(page);
    assert.deepEqual(s.counts, { accept: 2, reject: 1, maybe: 1 });
    assert.equal(s.history, 4);
    await shot('02-after-keyboard');

    // 8. Reduced motion: no tilt while dragging, decisions cross-fade, keyboard still works.
    await page.goto(`${base}?deck=desk&reduced=1`);
    await card().waitFor({ state: 'visible' });
    const b2 = await card().boundingBox();
    await page.mouse.move(b2.x + b2.width / 2, b2.y + b2.height / 2);
    await page.mouse.down();
    for (let i = 1; i <= 12; i++) await page.mouse.move(b2.x + b2.width / 2 + (200 * i) / 12, b2.y + b2.height / 2);
    const t = await card().evaluate((el) => el.style.transform);
    assert.ok(!/rotate|scale/.test(t), `reduced motion should not tilt or scale: ${t}`);
    await page.mouse.up();
    await waitIndex(page, 1);
    await page.keyboard.press('ArrowUp'); await waitIndex(page, 2);
    await page.locator('#btn-reject').click(); await waitIndex(page, 3);
    await page.keyboard.press('Z'); await waitIndex(page, 2);
    s = await demoState(page);
    assert.deepEqual(s.counts, { accept: 1, reject: 0, maybe: 1 });
    await shot('03-reduced-motion');

    // 9. Finishing a deck shows the end state and its link (no next= → stays).
    await page.goto(`${base}?deck=desk&count=2`);
    await card().waitFor({ state: 'visible' });
    await page.keyboard.press('ArrowRight'); await waitIndex(page, 1);
    await page.keyboard.press('ArrowLeft'); await waitIndex(page, 2);
    await page.locator('#done').waitFor({ state: 'visible' });
    assert.match(await page.locator('#done-text').innerText(), /1 accepted, 0 maybe, 1 rejected/);
    h.done();
  },
};
