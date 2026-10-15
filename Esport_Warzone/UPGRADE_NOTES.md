# Esport Warzone — Interactive Portal Upgrade

## Separate portals
- Public website: `/`
- Individual player signup: `/player/register`
- Player sign in: `/player/login`
- Player dashboard: `/player/dashboard` (login required)
- Admin sign in: `/admin/login`
- Admin control center: `/admin` (admin session required)

## What administrators can do
1. Create matches/tournament rounds for any of the nine supported games.
2. Set each match to Upcoming, Live, or Completed.
3. Record placement, kills/score, and points for a registered team and match. Re-entering the same match/team pair updates the score.
4. Review individual player registrations and the score history.
5. Delete a match (including its results) or delete a team (including related players/results).

## Default local demo credentials
Username: `admin`
Password: `Warzone@2026`

Set `ADMIN_USERNAME`, `ADMIN_PASSWORD`, and `FLASK_SECRET_KEY` in the environment before sharing or deploying. This is a classroom demo; add CSRF protection, rate limiting, secure cookie settings, and audit logs before public production use.

## MySQL Workbench
Run `schema.sql` against the local MySQL Server. The app also creates missing tables on startup. Set `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, and `MYSQL_DATABASE` before running `python app.py`.
