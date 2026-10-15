# Esport Warzone — Python + MySQL Workbench

A multi-game tournament registration and leaderboard website for the SPPU ECE DBMS project. The site uses Python Flask for the backend, HTML/CSS/JavaScript for the frontend, and MySQL Server for persistent data. **MySQL Workbench is the GUI used to run SQL and inspect the database; MySQL Server must also be installed and running.**

## Included games
Free Fire, BGMI, Candy Crush Saga, Subway Surfers, Temple Run, Mobile Legends: Bang Bang, Dr. Driving, Angry Birds, Bubble Shooter.

## Features
- Interactive homepage with stats, match cards, and published announcements
- Admin-managed timetable with start/end date and time for every match
- Public schedule and news page at `/schedule`
- Admin announcement center for registration notices, schedule changes, rules, and results
- Register a team and player roster
- Browse teams and player counts; delete a team
- Record or update match results
- Leaderboard using SQL JOIN, SUM, GROUP BY, and ORDER BY
- DBMS examples for CRUD, logical operators, joins, aggregation, indexes, and validation
- `schema.sql` for creating the database/tables in MySQL Workbench
- Project report and testing guide

## Setup: MySQL Workbench connection

1. Install **MySQL Server 8.x** and **MySQL Workbench**. Workbench alone is only a client; the MySQL Server service must be running.
2. Open MySQL Workbench and connect to your local instance (commonly `localhost`, port `3306`, user `root`).
3. Open `schema.sql` in Workbench, click the lightning bolt **Execute** button, and confirm the `esport_warzone` schema and six tables appear in the Schemas panel. The script creates six tables and adds a sample timetable plus a welcome announcement only when those tables are empty.
4. Set your MySQL credentials for the Flask app. On Windows Command Prompt, in the project folder:
   ```bat
   set MYSQL_HOST=127.0.0.1
   set MYSQL_PORT=3306
   set MYSQL_USER=root
   set MYSQL_PASSWORD=YOUR_MYSQL_PASSWORD
   set MYSQL_DATABASE=esport_warzone
   ```
   If your local root account has no password, set `MYSQL_PASSWORD=`. Do not share your password or commit it to source control.
5. Install Python 3.10+ and dependencies:
   ```bat
   py -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
6. Run:
   ```bat
   python app.py
   ```
7. Open `http://127.0.0.1:5000`.

The app creates tables and seeds a sample timetable plus a welcome announcement when it starts on an empty database. Change sample dates/times from the Admin dashboard to match your real event. You can also run `mysql_examples.sql` in Workbench to demonstrate SQL concepts.

## Common connection errors
- **Access denied for user 'root'**: set `MYSQL_PASSWORD` to the password used by your local MySQL account, or create a separate app user.
- **Can't connect to MySQL server**: start the MySQL80 service in Windows Services, check port 3306, and test the connection in Workbench.
- **Unknown database**: run `schema.sql` in Workbench or check `MYSQL_DATABASE`.
- **No results on leaderboard**: register a team, then visit `/admin/results` to enter scores.

## Important
This is an academic demo. Admin result-entry, match management, announcements, and delete routes require the admin session. Before public deployment, add CSRF protection, rate limiting, secure cookie settings, and deployment hardening.

## Enhanced player portal and admin control center

- **Player registration:** `/player/register` — individual accounts with password hashing, email uniqueness, selected game, and gamer tag.
- **Player login:** `/player/login` — player dashboard shows the schedule and published scores for the player's selected game.
- **Admin sign-in:** `/admin/login` — protected administrator dashboard at `/admin`.
- **Admin tools:** create matches/tournament rounds, set match status to Upcoming/Live/Completed, enter or update team results, review player signups, and audit saved scores.
- Admin score entry is protected by a session-based login. Set `ADMIN_USERNAME` and `ADMIN_PASSWORD` environment variables to replace the academic demo defaults (`admin` / `Warzone@2026`). Also set a unique `FLASK_SECRET_KEY` before deployment.

On Windows Command Prompt, before `python app.py`, you can set:

```bat
set ADMIN_USERNAME=your_admin_name
set ADMIN_PASSWORD=use_a_strong_unique_password
set FLASK_SECRET_KEY=use_a_long_random_secret
```

This is an academic demonstration, not a production-ready public service. Before deploying publicly, add CSRF protection, rate limiting, email verification, secure cookie settings, audit logging, and stronger role/permission controls. Player accounts are separate from team roster entries: players can register individually, while competitive team results are currently attached to registered teams.
