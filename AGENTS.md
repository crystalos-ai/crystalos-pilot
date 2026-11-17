# Notes for coding agents

- Python 3 standard library only. Do not add third-party packages.
- Run the tests from the repository root: `python3 -m unittest discover -s tests`.
- Keep changes small, and cover each fix with a test.
- Never commit secrets. A config names the environment variable that holds a
  password; it never holds the password itself.
- Production changes (production configuration or production data) go
  through change management. See `CONTRIBUTING.md`.
