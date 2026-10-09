// npm run build:data — design/02-data/sample-data.json → sample-data.js (window.SAMPLE) so that vanilla
// scripts in the prototype can read the sample data over file:// (fetch() of local JSON is blocked).
import { readFileSync, writeFileSync, renameSync } from 'node:fs';
import { join } from 'node:path';
import { DESIGN } from './lib.mjs';

const src = join(DESIGN, '02-data/sample-data.json');
const dest = join(DESIGN, '02-data/sample-data.js');
const json = JSON.stringify(JSON.parse(readFileSync(src, 'utf8')));
const tmp = `${dest}.${process.pid}.tmp`;
writeFileSync(tmp, `// Generated from sample-data.json by \`npm run build:data\` — do not edit.\nwindow.SAMPLE = ${json};\n`);
renameSync(tmp, dest);
console.log('build:data OK → design/02-data/sample-data.js');
