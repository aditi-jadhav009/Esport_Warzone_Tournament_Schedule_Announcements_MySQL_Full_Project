# Esport Warzone — Project Report

## 1. Title
**Esport Warzone: Multi-Game Tournament Management System using Python and MySQL**

## 2. Abstract
Esport Warzone is a web-based tournament portal for nine games. Users can register teams and players, view registered teams, record match scores, and see leaderboard rankings. Python Flask handles the web routes and validation, while MySQL stores relational data. MySQL Workbench is used to create, inspect, and query the database.

## 3. Objectives
- Build a simple multi-game tournament website.
- Store teams, players, matches, and scores in related database tables.
- Demonstrate CRUD operations, logical operators, joins, aggregate functions, indexes, and data validation.
- Apply SDLC stages including requirements, design, implementation, and testing.

## 4. Software and Hardware
Software: Python 3.10+, Flask, `mysql-connector-python`, MySQL Server 8.x, MySQL Workbench, VS Code, web browser. A computer capable of running these applications is sufficient.

## 5. Functional Requirements
1. Show the nine games and sample matches.
2. Register a team with captain/contact details and at least two players.
3. View registered teams and roster counts.
4. Enter or update match placement, kills, and points.
5. Display a leaderboard ranked by total points and kills.
6. Persist data in MySQL.

## 6. Database Design
Database name: `esport_warzone`.

| Table | Purpose | Key fields |
|---|---|---|
| `teams` | Team details | `id` primary key; `team_name` unique |
| `players` | Team roster | `id` primary key; `team_id` foreign key |
| `matches` | Tournament events | `id` primary key |
| `results` | Team score per match | `id` primary key; foreign keys `match_id`, `team_id`; unique match/team pair |

Relationships: one team can have many players; one team can have many result records; one match can have many result records. Foreign keys with `ON DELETE CASCADE` remove related roster and score rows when a team is deleted.

## 7. ER Model (text description)
`TEAMS (1) ─── (many) PLAYERS`
`TEAMS (1) ─── (many) RESULTS (many) ─── (1) MATCHES`

## 8. Normalization
The tables separate team, player, match, and result details. Each table has a primary key; non-key attributes describe the row identified by that key. Unique constraints prevent duplicate team names, player IDs, and duplicate result entries for the same match/team pair. This structure reduces unnecessary repetition and supports referential integrity.

## 9. Architecture
Browser (HTML/CSS/JavaScript) → Flask routes (Python validation and application logic) → `mysql-connector-python` → MySQL Server database. MySQL Workbench is used by the developer to execute SQL scripts and inspect the tables.

## 10. Implementation
- `app.py`: Flask routes, connection settings, schema initialization, registration, result entry, and leaderboard queries.
- `templates/`: page templates.
- `static/`: CSS, JavaScript, and game thumbnails.
- `schema.sql`: database and table creation script.
- `mysql_examples.sql`: SQL practice queries.
- `TESTING.md`: manual test cases.

## 11. DBMS Concepts Demonstrated
- CRUD: `INSERT`, `SELECT`, `UPDATE`, `DELETE`.
- Logical operators: `AND`, `OR`, `NOT`.
- Joins: teams with players; results with teams and matches.
- Aggregate functions: `SUM`, `COUNT`.
- Grouping and sorting: `GROUP BY`, `HAVING`, `ORDER BY`.
- Indexes: team/game, match status, and score indexes.
- Validation: required fields, allowed games, minimum roster size, unique keys, and foreign keys.

## 12. Testing
Use the manual test cases in `TESTING.md`. Confirm that the app starts with MySQL running, a team can be registered, duplicate values are rejected, scores can be saved, and the leaderboard reflects those scores. Actual runtime testing requires MySQL Server credentials on the machine running the app.

## 13. Limitations and Future Scope
This is a student demonstration. Add admin login, CSRF protection, email/OTP verification, pagination, and deployment security before public release. Sample games and matches are illustrative.

## 14. Conclusion
Esport Warzone demonstrates a complete Python Flask web application connected to a MySQL relational database. It combines a multi-game registration workflow with score management and SQL concepts required for a DBMS application project.
