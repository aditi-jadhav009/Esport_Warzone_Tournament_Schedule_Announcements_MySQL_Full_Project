# Testing checklist — Esport Warzone

## Before testing
- Start MySQL Server and connect to it using MySQL Workbench.
- Execute `schema.sql` in Workbench.
- Set `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, and `MYSQL_DATABASE` for Flask.
- Run `pip install -r requirements.txt`, then `python app.py`.

## Player and public pages
- Open `/` and confirm game cards, stats, sample match timetable, and published announcements load.
- Open `/schedule` and confirm matches appear chronologically with date, time, arena, and status.
- Register an individual player at `/player/register`, sign in at `/player/login`, and confirm the dashboard shows the player's game matches and results.
- Register a team at `/register`; confirm it appears on `/teams`.
- Confirm `/leaderboard` displays saved results after an admin enters scores.

## Administrator
- Sign in at `/admin/login` using the credentials configured in environment variables.
- Create a match with start/end times; confirm it appears on the public timetable.
- Change its status to Live and then Completed; confirm the status updates publicly.
- Publish a General, Registration, Schedule, Results, or Rules announcement; confirm it appears on the home page and `/schedule`.
- Save a score for a registered team and match; confirm the leaderboard and score audit update.
- Delete a test announcement and test match; confirm they disappear.
- Sign out and verify protected admin POST actions redirect to admin login.

## SQL practicals
Run `mysql_examples.sql` in Workbench to demonstrate SELECT, INSERT/UPDATE/DELETE examples, logical operators, JOIN, aggregation, GROUP BY, HAVING, indexes, timetable queries, and announcements.

## Scope note
Python syntax compilation is a static check only. Run the checklist against your own MySQL Server to verify credentials, permissions, schema state, and browser behavior. This academic project should receive CSRF protection, rate limiting, secure cookies, and deployment hardening before being exposed publicly.
