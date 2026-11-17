# Runbook: purge test rows from the local database

Use this when the local payments database fills up with `TEST-` payments from
manual testing. It applies to the local SQLite database only.

1. Build the local database if you do not have one:
   `python3 -m services.payments.seed_local_db`
2. See how many rows would go:
   `python3 -m services.payments.maintenance.purge_test_rows --dry-run`
3. Delete them:
   `python3 -m services.payments.maintenance.purge_test_rows`
4. Run the tests: `python3 -m unittest discover -s tests`

The script refuses any config that is not a local SQLite file. Production data
is never purged from a laptop: raise a change request with the platform team.
