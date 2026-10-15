-- Esport Warzone SQL practice queries
USE esport_warzone;

-- 1. READ: display all teams
SELECT * FROM teams ORDER BY game_name, team_name;

-- 2. READ: find teams for a particular game
SELECT * FROM teams WHERE game_name = 'Free Fire';

-- 3. LOGICAL operators: AND / OR / NOT
SELECT * FROM teams
WHERE (game_name = 'BGMI' OR game_name = 'Free Fire')
  AND NOT department = 'Cancelled';

-- 4. JOIN: show players with their teams
SELECT p.player_name, p.game_uid, p.role, t.team_name, t.game_name
FROM players p JOIN teams t ON t.id = p.team_id
ORDER BY t.team_name, p.player_name;

-- 5. INSERT example (use unique team name and game UID)
-- INSERT INTO teams (team_name, game_name, captain_name, contact, department)
-- VALUES ('Demo Squad', 'Free Fire', 'Captain Name', '9876543210', 'ECE');

-- 6. UPDATE example
-- UPDATE teams SET department = 'Computer Engineering' WHERE team_name = 'Demo Squad';

-- 7. DELETE example (related players/results are removed via ON DELETE CASCADE)
-- DELETE FROM teams WHERE team_name = 'Demo Squad';

-- 8. Aggregate functions: leaderboard
SELECT t.team_name, t.game_name, SUM(r.points) AS total_points,
       SUM(r.kills) AS total_kills, COUNT(r.id) AS matches_played
FROM results r JOIN teams t ON t.id = r.team_id
GROUP BY t.id, t.team_name, t.game_name
ORDER BY total_points DESC, total_kills DESC;

-- 9. GROUP BY: number of registered teams per game
SELECT game_name, COUNT(*) AS team_count
FROM teams GROUP BY game_name ORDER BY team_count DESC;

-- 10. HAVING: games with at least one team
SELECT game_name, COUNT(*) AS team_count
FROM teams GROUP BY game_name HAVING COUNT(*) >= 1;

-- 11. Indexes (also created by schema.sql)
CREATE INDEX idx_teams_game_name ON teams(game_name);
CREATE INDEX idx_matches_status ON matches(status);
-- To inspect:
SHOW INDEX FROM teams;

-- 12. Upsert a match result (match_id and team_id must exist)
-- INSERT INTO results (match_id, team_id, placement, kills, points)
-- VALUES (1, 1, 1, 8, 20)
-- ON DUPLICATE KEY UPDATE placement=VALUES(placement), kills=VALUES(kills), points=VALUES(points);

-- 13. Data validation examples
SELECT * FROM teams WHERE contact IS NULL OR contact = '';
SELECT game_uid, COUNT(*) FROM players GROUP BY game_uid HAVING COUNT(*) > 1;

-- 14. Tournament timetable in chronological order
SELECT match_name, game_name, arena, start_at, end_at, status
FROM matches ORDER BY (start_at IS NULL), start_at, id;

-- 15. Public tournament announcements
SELECT title, body, category, created_at
FROM announcements WHERE published = 1 ORDER BY created_at DESC;

-- 16. Announcements in a category
SELECT * FROM announcements
WHERE published = 1 AND category IN ('Registration', 'Schedule')
ORDER BY created_at DESC;

-- 17. Add a tournament announcement (run manually if desired)
-- INSERT INTO announcements (title, body, category, published)
-- VALUES ('Registration deadline', 'Registration closes before the first match.', 'Registration', 1);

-- 18. Set a match schedule (change match ID and times to your event)
-- UPDATE matches SET start_at='2026-11-02 10:00:00', end_at='2026-11-02 11:00:00'
-- WHERE id=1;
