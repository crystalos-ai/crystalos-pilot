'use strict';

const fs = require('node:fs');
const path = require('node:path');

// The pilot input is committed for each governed read/write demonstration.
const input = fs.readFileSync(path.join(__dirname, 'demo', 'input.txt'), 'utf8');
process.stdout.write(input);
