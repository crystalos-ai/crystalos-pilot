# Contributing

## Code style

- Python 3, standard library only.
- Follow PEP 8. Keep functions short, and give each module a docstring that
  says what it is for.
- Money is an integer number of minor units (pence). Never use floats for
  amounts.

## Tests

- Run `python3 -m unittest discover -s tests` before you open a pull request.
- Every bug fix comes with a test that fails before the fix and passes after it.
- Do not skip or delete a failing test to get a green run. Fix the cause, or
  raise it with the owning team.

## Secrets

- Never commit a password, token or key. Configs reference environment
  variables by name (for example `PAYMENTS_DB_PASSWORD`).
- Local databases and reports (`var/`, `out/`) are ignored by git.

## Change management

- Production configuration (`services/payments/db.production.conf`) and
  production data belong to the platform team. Any change to them needs an
  approved change request and a second approver.
- Screening thresholds in `screening/rules.py` are set by Financial Crime
  Compliance. Change them only with a signed-off compliance ticket.
- Local and test data can be changed freely.
