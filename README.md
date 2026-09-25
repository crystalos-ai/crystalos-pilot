# CrystalOS pilot repository

A harmless test repository for the CrystalOS two-Mac governed-Claude pilot.
Each hero run commits a fresh random nonce under demo/ and asks the governed
remote Claude to read it back.

The root Node project lets CrystalOS recognize the repository build provider.
It has no external dependencies. `npm run build` checks syntax, and `npm start`
prints the current committed pilot input. The managed Claude demonstration still
reads the input and publishes its result through the governed file tools.
