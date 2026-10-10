// Shared helpers for tools/flows/*.flow.mjs (QA, Phase 4).
// - frame(id): waits until the URL is <file>#<id> and asserts that frame is the only visible frame
//   (prototype mode) and is inside the viewport.
// - tap(id, action): clicks `#<id> [data-action="<action>"]` scoped to the visible frame; counts taps.
//   Visually hidden prototype shortcuts (sr-only) are activated with the keyboard (focus + Enter), as a
//   keyboard user would; this is logged.
// - Fails on console errors and failed local requests (missing images, CSS, fonts).
import { readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { SCREENS } from '../lib.mjs';

const frameFile = new Map();
for (const f of readdirSync(SCREENS).filter((x) => x.endsWith('.html'))) {
  for (const m of readFileSync(join(SCREENS, f), 'utf8').matchAll(/\sdata-frame="([^"]+)"/g)) frameFile.set(m[1], f);
}

export function helpers({ page, assert }) {
  const problems = [];
  const log = [];
  let taps = 0;
  page.on('console', (m) => { if (m.type() === 'error') problems.push(`console.error: ${m.text()}`); });
  page.on('requestfailed', (r) => problems.push(`request failed: ${r.url()} (${r.failure()?.errorText})`));

  async function frame(id, { file } = {}) {
    const f = file ?? frameFile.get(id);
    assert.ok(f, `unknown frame ${id}`);
    try {
      await page.waitForURL((u) => decodeURIComponent(u.pathname).endsWith(`/${f}`) && u.hash === `#${id}`, { timeout: 8000 });
    } catch {
      assert.fail(`expected ${f}#${id}, got ${page.url()}`);
    }
    const loc = page.locator(`[data-frame="${id}"]`);
    await loc.waitFor({ state: 'visible', timeout: 5000 });
    const visibleFrames = await page.$$eval('[data-frame]', (els) => els.filter((e) => e.getBoundingClientRect().height > 0 && getComputedStyle(e).display !== 'none').map((e) => e.dataset.frame));
    assert.deepEqual(visibleFrames, [id], `prototype mode should show only ${id}, visible: ${visibleFrames.join(', ')}`);
    log.push(id);
    return loc;
  }

  async function tap(id, action) {
    const target = page.locator(`[data-frame="${id}"] [data-action="${action}"]`).first();
    const n = await page.locator(`[data-frame="${id}"] [data-action="${action}"]`).count();
    assert.ok(n > 0, `${id}: no [data-action="${action}"]`);
    const box = await target.boundingBox();
    taps++;
    if (!box || box.width <= 2 || box.height <= 2) {
      log.push(`(${id} [${action}] is a visually hidden prototype shortcut: activated with the keyboard)`);
      await target.focus();
      await page.keyboard.press('Enter');
    } else {
      await target.click({ timeout: 5000 });
    }
  }

  /** Open a frame in prototype mode: open(file) then go to file#id (open() encodes '#'). */
  async function start(open, id) {
    const f = frameFile.get(id);
    await open(`03-screens/${f}`);
    await page.goto(`${page.url().split('#')[0]}#${id}`);
    return frame(id);
  }

  function done() {
    assert.deepEqual(problems, [], problems.join('\n'));
  }

  return { start, frame, tap, done, log, get taps() { return taps; }, problems };
}

/** Drag the top card on swipe-demo.html with the mouse. dx/dy in px; slow=true keeps velocity low. */
export async function dragCard(page, dx, dy, { steps = 12, slow = false } = {}) {
  const card = page.locator('[data-testid="card"]').first();
  const b = await card.boundingBox();
  const x = b.x + b.width / 2, y = b.y + b.height / 2;
  await page.mouse.move(x, y);
  await page.mouse.down();
  for (let i = 1; i <= steps; i++) {
    await page.mouse.move(x + (dx * i) / steps, y + (dy * i) / steps);
    if (slow) await page.waitForTimeout(40);
  }
  if (slow) await page.waitForTimeout(150);
  await page.mouse.up();
}

export const demoState = (page) => page.evaluate(() => window.__swipeDemo.state());

/** Wait until the demo is idle and the decided index equals n. */
export async function waitIndex(page, n) {
  await page.waitForFunction((k) => window.__swipeDemo && window.__swipeDemo.state().index === k, n, { timeout: 5000 });
  await page.waitForTimeout(80);
}
